#!/usr/bin/env python3
"""Resolve ground-truth anchors to line numbers and emit the reference CBOM (CycloneDX 1.6).

Outputs:
  expected/ground_truth.resolved.json   ground truth with line numbers filled in
  expected/expected.cdx.json            what a perfect scanner would produce

Tiers 1-3 are emitted as algorithm components. Tier 4 uses the asset types a good scanner
should produce: certificate (with subjectPublicKeyRef / signatureAlgorithmRef),
related-crypto-material (private / public keys), and protocol (TLS versions + cipher suites).
Scoring the reference therefore exercises every extraction path in the scorer.

Fails loudly if an anchor is missing or ambiguous, if two findings share a (file, family) key
(unless all of them are site findings in a mixed file), or if a finding isn't covered by the
reference output.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from truth import LIBRARIES, attach_facts, library_for, load_ground_truth  # noqa: E402
from cbomlib import (FAMILIES, SIGNATURE_FAMILIES, functions_for, make_bom, make_certificate,  # noqa: E402
                     make_component, make_key_material, make_protocols, normalize, oid_for)

ROOT = Path(__file__).resolve().parent.parent
GT = ROOT / "expected" / "ground_truth.json"


def resolve(file_rel: str, anchors: list[str], fid: str) -> list[int]:
    if not anchors:
        return []  # binary or whole-file assets (DER, PKCS#12, PEM): file-level only
    lines = (ROOT / file_rel).read_text(encoding="utf-8").splitlines()
    out = []
    for a in anchors:
        hits = [i + 1 for i, line in enumerate(lines) if a in line]
        if len(hits) != 1:
            raise SystemExit(f"{fid}: anchor {a!r} found {len(hits)} times in {file_rel} (need exactly 1)")
        out.append(hits[0])
    return out


def is_protocolish(family: str) -> bool:
    meta = FAMILIES.get(family, {})
    return bool(meta.get("protocol") or meta.get("suite"))


def reference_libraries() -> list[dict]:
    """One located library component per expected dependency (expected/libraries.json)."""
    from libraries import load_expected
    exp = load_expected()
    out = []
    for e in (exp or {}).get("libraries", []):
        first = e["package"].split(",")[0].strip()
        v = e.get("version")
        eco = e["ecosystem"]
        if eco == "maven":
            g, a = first.split(":")
            comp = {"group": g, "name": a, "purl": f"pkg:maven/{g}/{a}" + (f"@{v}" if v else "")}
        elif eco == "golang":
            comp = {"name": first, "purl": f"pkg:golang/{first}" + (f"@v{v}" if v else "")}
        elif eco == "npm":
            comp = {"name": first, "purl": f"pkg:npm/{first.replace('@', '%40', 1) if first.startswith('@') else first}" + (f"@{v}" if v else "")}
        else:
            comp = {"name": first, "purl": f"pkg:{eco}/{first.lower()}" + (f"@{v}" if v else "")}
        out.append({"type": "library", "bom-ref": e["id"], **comp, **({"version": v} if v else {}),
                    "evidence": {"occurrences": [{"location": e["file"]}]}})
    return out


def main() -> int:
    gt = load_ground_truth()  # shipped + confirmed BYOC cases
    seen = set()
    by_id = {}

    for f in gt["findings"]:
        key = (f["file"], f["family"], f["id"] if f.get("site") else None)
        if key in seen or (f.get("site") and (f["file"], f["family"], None) in seen):
            raise SystemExit(f"{f['id']}: duplicate (file, family) {key[:2]}")
        seen.add(key)
        if f["family"] not in FAMILIES:
            raise SystemExit(f"{f['id']}: unknown family {f['family']}")
        if not (ROOT / f["file"]).exists():
            raise SystemExit(f"{f['id']}: missing file {f['file']}")
        f["lines"] = resolve(f["file"], f.get("anchors", []), f["id"])
        for alt in f.get("alt_files", []):
            alt["lines"] = resolve(alt["file"], alt.get("anchors", []), f["id"])
        by_id[f["id"]] = f

    attach_facts(gt)
    components = []
    covered = set()  # (file, family) produced by certificate / key-material output
    provides = {}    # library bom-ref -> crypto component refs it provides

    for m in gt.get("materials", []):
        k = by_id[m["key"]]
        if k["file"] != m["file"]:
            raise SystemExit(f"material {m['id']}: key finding {m['key']} is in another file")
        if m["kind"] == "certificate":
            components += make_certificate(m["id"], m["file"], k["family"], k["params"], m["sig_alg"], m.get("facts"))
            sig_fam, sig_params = normalize(m["sig_alg"])
            covered.add((m["file"], sig_fam))
            if sig_fam in SIGNATURE_FAMILIES and sig_params.get("hash"):
                covered.add((m["file"], sig_params["hash"]))
        else:
            components += make_key_material(m["id"], m["file"], m["kind"], k["family"], k["params"], m.get("format"))
        covered.add((m["file"], k["family"]))

    proto_by_file = defaultdict(list)
    for f in gt["findings"]:
        if is_protocolish(f["family"]):
            proto_by_file[f["file"]].append(f)
            continue
        if (f["file"], f["family"]) in covered:
            continue
        occ = {"location": f["file"]}
        if f["lines"]:
            occ["line"] = f["lines"][0]
            text = (ROOT / f["file"]).read_text(encoding="utf-8").splitlines()[f["lines"][0] - 1].strip()
            occ["additionalContext"] = text[:200]
        prim = f.get("primitive") or FAMILIES[f["family"]]["primitive"]
        components.append(make_component(ref=f["id"], family=f["family"], params=f["params"],
                                         occurrences=[occ], primitive=prim, functions=functions_for(prim),
                                         oid=oid_for(f["family"], f["params"])))
        lib = library_for(f)
        if lib:
            provides.setdefault(lib, []).append(f["id"])

    for i, (file, fs) in enumerate(sorted(proto_by_file.items())):
        versions = [f["family"] for f in fs if FAMILIES[f["family"]].get("protocol")]
        suites = [f["family"] for f in fs if FAMILIES[f["family"]].get("suite")]
        lines = {f["family"]: f["lines"][0] for f in fs if f["lines"]}
        components += make_protocols(f"proto-{i}", file, versions, suites, lines)

    for entry in gt.get("also_ok", []):
        if not (ROOT / entry["file"]).exists():
            raise SystemExit(f"also_ok references missing file {entry['file']}")

    out_gt = ROOT / "expected" / "ground_truth.resolved.json"
    out_gt.write_text(json.dumps(gt, indent=2) + "\n", encoding="utf-8")

    components += reference_libraries()

    libs = [lib for lib in LIBRARIES if lib["bom-ref"] in provides]
    deps = [{"ref": ref, "provides": refs} for ref, refs in sorted(provides.items())]
    # Asset links (system fixture): the protocol names its certificate, the certificate its key file.
    def located(file):
        return [c["bom-ref"] for c in components
                if any(o.get("location") == file for o in (c.get("evidence") or {}).get("occurrences") or [])]
    for link in gt.get("links", []):
        src, dst = located(link["from"]), located(link["to"])
        if not src or not dst:
            raise SystemExit(f"link {link['id']}: no reference component in {link['from'] if not src else link['to']}")
        deps += [{"ref": r, "dependsOn": dst} for r in src]
    bom = make_bom(libs + components, "cbom-testbench reference", deps)
    out_bom = ROOT / "expected" / "expected.cdx.json"
    out_bom.write_text(json.dumps(bom, indent=2) + "\n", encoding="utf-8")

    by_tier = defaultdict(int)
    for f in gt["findings"]:
        by_tier[(f["tier"], f["lang"])] += 1
    print(f"Resolved {len(gt['findings'])} findings:")
    for (tier, lang), n in sorted(by_tier.items(), key=lambda kv: (not isinstance(kv[0][0], int), str(kv[0][0]), kv[0][1])):
        print(f"  Tier {tier} {lang:<7} {n}")
    print(f"Wrote {out_gt.relative_to(ROOT)} and {out_bom.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
