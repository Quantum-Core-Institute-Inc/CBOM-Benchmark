#!/usr/bin/env python3
"""Holdout generator and overfit-gap checks. Run: python tools/test_holdout.py [--quick]

--quick skips executing the generated files (the slow part: a few hundred Python and Java runs)."""
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import holdout as ho  # noqa: E402
from cbomlib import FAMILIES, load_json  # noqa: E402
from score import score  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ALGO_WORDS = re.compile(r"\b\w*(md5|sha1|sha256|rsa|aes|hmac|ecdsa|ed25519|x25519|pbkdf|kyber|mlkem|mldsa)\w*\s*=", re.I)


def main() -> int:
    quick = "--quick" in sys.argv
    bad = []
    with tempfile.TemporaryDirectory() as tmp:
        a, b, c = Path(tmp) / "a", Path(tmp) / "b", Path(tmp) / "c"
        ta, tb, tc = ho.generate(4242, a, 40, 20), ho.generate(4242, b, 40, 20), ho.generate(4243, c, 40, 20)

        # 1. Deterministic for a seed, different across seeds.
        # Key material and compiled artifacts carry fresh random bytes (keys) or timestamps (.pyc); their
        # answer key is still identical. Everything else must match byte for byte.
        fresh = ("corpus/holdout-t4/", "corpus/holdout-t5/")
        same = all((a / f["file"]).read_bytes() == (b / f["file"]).read_bytes() for f in ta["findings"]
                   if not f["file"].startswith(fresh) or f["file"].endswith((".conf", ".cnf", ".yml", "_sshd_config")))
        if ta["findings"] != tb["findings"] or not same:
            bad.append("same seed produced different output")
        if [f["file"] for f in ta["findings"]] == [f["file"] for f in tc["findings"]]:
            bad.append("different seeds produced the same files")

        # 2. Answer key is well formed: known families, a line per finding, one finding per (file, family)
        # except site findings in mixed files, which must sit in holdout-mixed.
        keys = [(f["file"], f["family"], f["id"] if f.get("site") else None) for f in ta["findings"]]
        if len(keys) != len(set(keys)):
            bad.append("duplicate (file, family) in the answer key")
        for f in ta["findings"]:
            if f.get("site") and f["tier"] != "holdout-mixed":
                bad.append(f"{f['id']}: site finding outside holdout-mixed")
            file_level = f["file"].startswith(("corpus/holdout-t4/", "corpus/holdout-t5/"))
            if f["family"] not in FAMILIES or (not f["lines"] and not file_level):
                bad.append(f"{f['id']}: unknown family or no anchor line")
        tiers = {f["tier"] for f in ta["findings"]}
        if not set(ho.HOLDOUT_TIERS) | {"holdout-broad"} <= tiers:  # incl. holdout-mixed
            bad.append(f"missing a holdout tier: {tiers}")
        langs = {f["lang"] for f in ta["findings"]}
        if not {"python", "java", "go", "c"} <= langs or not langs & {"javascript", "typescript"}:
            bad.append(f"missing a language: {langs}")
        # Generator 1.2: C#, more config formats, stateful-signature policies, minified and native artifacts.
        if "csharp" not in langs:
            bad.append("no C# cases")
        files = {f["file"] for f in ta["findings"]}
        for what, hit in (("HAProxy config", lambda x: x.endswith(".cfg")), ("IPsec config", lambda x: "/ipsec/" in x),
                          ("firmware signing policy", lambda x: "/firmware/" in x), ("minified JavaScript", lambda x: x.endswith(".min.js")),
                          ("native binary", lambda x: "/c/bin/" in x)):
            if not any(hit(x) for x in files):
                bad.append(f"no {what} in the set")
        if not {"LMS", "XMSS"} <= {f["family"] for f in ta["findings"]}:
            bad.append("no LMS or XMSS finding in the set")
        for cs in sorted(x for x in files if x.endswith(".cs")):
            if not (a / cs).with_name(Path(cs).parent.name + ".csproj").exists():
                bad.append(f"{cs}: no project file beside it")
        libs = json.loads((a / "libraries.json").read_text())
        if not libs.get("libraries") or any(not (a / x["file"]).exists() for x in libs["libraries"]):
            bad.append("no dependency manifests, or a library points at a missing file")

        # 3. No answer leaks: no comments past the one-line file header, no identifiers named after
        # algorithms, no seed in the files. Dependency manifests are allowed comments (decoys live there).
        for p in (a / "corpus").rglob("*"):
            if not p.is_file():
                continue
            if p.suffix in (".der", ".p12", ".pyc", ".jar"):
                continue  # binary
            text = p.read_text(errors="ignore")
            if "4242" in text and "BEGIN" not in text and "tls.crt" not in text:
                bad.append(f"{p.name}: contains the seed")
            if p.suffix not in ho.CODE_EXT or "/deps/" in p.as_posix():
                continue
            code = [ln for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith(('"""', "public class"))][1:]
            if p.suffix == ".c":
                code = [ln for ln in code if not ln.startswith(("#include", "#define", "#if", "#endif"))]
            # negatives carry algorithm names in comments and strings on purpose: they're the trap
            if "/negatives/" not in p.as_posix() and any(ln.lstrip().startswith(("#", "//", "/*")) for ln in code):
                bad.append(f"{p.name}: has a comment")
            if "negatives" not in str(p) and ALGO_WORDS.search(text):
                bad.append(f"{p.name}: identifier names an algorithm: {ALGO_WORDS.search(text).group(0)}")

        # 4. Matched tiers use only the published (tier, language, family) cells.
        pub = ho.published_families()
        for f in ta["findings"]:
            t = ho.HOLDOUT_TIERS.get(f["tier"])
            if t is not None and f["family"] not in pub.get((t, f["lang"]), ()):
                bad.append(f"{f['id']}: {f['family']} isn't in published Tier {t} {f['lang']}")

        # 5. The metric at its two extremes: the reference CBOM has no gap; a memorizer has the maximum.
        ref_pub = score(load_json(ROOT / "expected" / "expected.cdx.json"), custom="exclude")
        own = ho.score_holdout(load_json(a / "expected.cdx.json"), a)
        g = ho.overfit_gap(ref_pub, own)
        if own["summary"]["all/all"]["recall"] != 100.0 or g["gap"] != 0.0 or g["significant"]:
            bad.append(f"reference: holdout recall {own['summary']['all/all']['recall']}, gap {g['gap']}")
        memo = ho.score_holdout(load_json(ROOT / "expected" / "expected.cdx.json"), a)
        g = ho.overfit_gap(ref_pub, memo)
        if g["gap"] != 100.0 or not g["significant"]:
            bad.append(f"memorizer: gap {g['gap']} {g['gap_ci95']}, should be +100 and significant")
        if g["gap_ci95"][0] > g["gap"] or g["gap_ci95"][1] < g["gap"] - 1e-9 and g["gap"] != 100.0:
            bad.append("interval doesn't contain the point estimate")

        # 5b. Negative-control gap: no false positives anywhere -> 0.
        n = ho.negative_gap(ref_pub, own, a)
        if n["gap_per_file"] != 0 or n["holdout_files"] == 0:
            bad.append(f"negative gap for the reference should be 0 over >0 files: {n}")

        # 5c. Library gap at its extremes: the holdout's own answer key reads 0, the published one +100.
        pub_lib = ref_pub.get("libraries")
        lg = ho.library_gap(pub_lib, load_json(a / "expected.cdx.json"), a)
        lm = ho.library_gap(pub_lib, load_json(ROOT / "expected" / "expected.cdx.json"), a)
        if not lg or lg["gap"] != 0 or lg["holdout"] != 100.0:
            bad.append(f"library gap for the holdout's answer key should be 0: {lg}")
        if not lm or lm["holdout"] != 0.0 or lm["gap"] <= 0:
            bad.append(f"library gap for a memorizer should be large: {lm}")

        # 6. Negatives contain no crypto API use, in any language.
        negs = [q for q in (a / "corpus" / "negatives").rglob("*") if q.is_file()]
        if {q.suffix for q in negs} < {".py", ".java", ".go", ".c"}:
            bad.append(f"negatives don't cover every language: {sorted({q.suffix for q in negs})}")
        for p in negs:
            if re.search(r"getInstance|import (hashlib|hmac)|cryptography|\"crypto/|crypto['\"]|openssl/", p.read_text()):
                bad.append(f"{p.name}: negative control uses crypto")

        # 7. Everything runs.
        if not quick:
            bad += [f"does not run: {x}" for x in ho.verify(a)]

    for x in bad:
        print("FAIL", x)
    print(f"holdout checks: {'all pass' if not bad else f'{len(bad)} failures'}" + (" (quick)" if quick else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
