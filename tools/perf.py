"""The large-repository fixture: can a scanner finish an estate-sized tree inside a time budget, and
does it still look at the last file?

A generated tree (public seed; nothing here is secret) of ordinary code in five languages, a few
large data files, and a small number of planted crypto uses spread evenly through it. The planted
uses are literal, Tier 1 calls: any scanner finds them in a small file. What this measures is
whether it finds them at file 4,000 of 5,000, how long that took, and how much memory it needed.

  generate(seed, out, size)   -> writes out/corpus/... and out/truth.json
  score_perf(bom, out)        -> recall on the planted uses, overall and by position in the tree,
                                 false positives in the noise, and whether coverage fell off
"""
from __future__ import annotations

import json
import random
from pathlib import Path

from cbomlib import iter_crypto_findings_ctx, norm_path, same_file

SIZES = {"small": (600, 24), "medium": (3000, 60), "large": (12000, 120)}  # (code files, planted uses)
LANGS = ["python", "java", "go", "javascript", "c"]
EXT = {"python": ".py", "java": ".java", "go": ".go", "javascript": ".js", "c": ".c"}
FAMILIES = ["MD5", "SHA-1", "RSA", "3DES"]

PLANT = {  # (imports, statement) per language and family; {v} is a fresh variable name
    ("python", "MD5"): ("import hashlib", "{v} = hashlib.md5(b'payload').hexdigest()"),
    ("python", "SHA-1"): ("import hashlib", "{v} = hashlib.sha1(b'payload').hexdigest()"),
    ("python", "RSA"): ("from cryptography.hazmat.primitives.asymmetric import rsa",
                        "{v} = rsa.generate_private_key(public_exponent=65537, key_size=2048)"),
    ("python", "3DES"): ("from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES",
                         "{v} = TripleDES(b'k' * 24)"),
    ("java", "MD5"): ("import java.security.MessageDigest;", "MessageDigest {v} = MessageDigest.getInstance(\"MD5\");"),
    ("java", "SHA-1"): ("import java.security.MessageDigest;", "MessageDigest {v} = MessageDigest.getInstance(\"SHA-1\");"),
    ("java", "RSA"): ("import java.security.KeyPairGenerator;",
                      "KeyPairGenerator {v} = KeyPairGenerator.getInstance(\"RSA\"); {v}.initialize(2048);"),
    ("java", "3DES"): ("import javax.crypto.Cipher;", "Cipher {v} = Cipher.getInstance(\"DESede/CBC/PKCS5Padding\");"),
    ("go", "MD5"): ("\"crypto/md5\"", "{v} := md5.Sum([]byte(\"payload\"))"),
    ("go", "SHA-1"): ("\"crypto/sha1\"", "{v} := sha1.Sum([]byte(\"payload\"))"),
    ("go", "RSA"): ("\"crypto/rand\"\n\t\"crypto/rsa\"", "{v}, _ := rsa.GenerateKey(rand.Reader, 2048)"),
    ("go", "3DES"): ("\"crypto/des\"", "{v}, _ := des.NewTripleDESCipher(make([]byte, 24))"),
    ("javascript", "MD5"): ("const crypto = require(\"node:crypto\");", "const {v} = crypto.createHash(\"md5\");"),
    ("javascript", "SHA-1"): ("const crypto = require(\"node:crypto\");", "const {v} = crypto.createHash(\"sha1\");"),
    ("javascript", "RSA"): ("const crypto = require(\"node:crypto\");",
                            "const {v} = crypto.generateKeyPairSync(\"rsa\", {{ modulusLength: 2048 }});"),
    ("javascript", "3DES"): ("const crypto = require(\"node:crypto\");",
                             "const {v} = crypto.createCipheriv(\"des-ede3-cbc\", Buffer.alloc(24), Buffer.alloc(8));"),
    ("c", "MD5"): ("#include <openssl/md5.h>", "unsigned char {v}[16]; MD5((const unsigned char *)\"p\", 1, {v});"),
    ("c", "SHA-1"): ("#include <openssl/evp.h>", "const EVP_MD *{v} = EVP_sha1();"),
    ("c", "RSA"): ("#include <openssl/rsa.h>", "RSA *{v} = RSA_new(); RSA_generate_key_ex({v}, 2048, NULL, NULL);"),
    ("c", "3DES"): ("#include <openssl/evp.h>", "const EVP_CIPHER *{v} = EVP_des_ede3_cbc();"),
}
WORDS = ("order invoice ledger account route batch report member shipment payment session record queue "
         "tenant metric profile catalog window bucket cursor").split()


def _name(rng, sep="_"):
    return sep.join(rng.sample(WORDS, 2))


def _body(rng, lang: str, n_funcs: int) -> list[str]:
    """Ordinary code: arithmetic, string handling, loops. No crypto words."""
    out = []
    for i in range(n_funcs):
        f, a, b = f"{_name(rng)}_{i}", rng.randint(2, 97), rng.randint(3, 501)
        if lang == "python":
            out += [f"def {f}(items):", "    total = 0", "    for i, x in enumerate(items):",
                    f"        total += (x * {a}) % {b}", "        if total > 10000:", "            total //= 3",
                    f"    return str(total).rjust({a % 12 + 4}, '0')", ""]
        elif lang == "java":
            out += [f"    static String {f}(int[] items) {{", "        long total = 0;",
                    "        for (int i = 0; i < items.length; i++) {", f"            total += (items[i] * {a}L) % {b};",
                    "            if (total > 10000) total /= 3;", "        }", "        return Long.toString(total);", "    }", ""]
        elif lang == "go":
            out += [f"func {f}(items []int) string {{", "\ttotal := 0", "\tfor _, x := range items {",
                    f"\t\ttotal += (x * {a}) % {b}", "\t\tif total > 10000 {", "\t\t\ttotal /= 3", "\t\t}", "\t}",
                    "\treturn strconv.Itoa(total)", "}", ""]
        elif lang == "javascript":
            out += [f"function {f}(items) {{", "  let total = 0;", "  for (const x of items) {",
                    f"    total += (x * {a}) % {b};", "    if (total > 10000) total = Math.floor(total / 3);", "  }",
                    f"  return String(total).padStart({a % 12 + 4}, \"0\");", "}", ""]
        else:
            out += [f"long {f}(const int *items, int n) {{", "    long total = 0;", "    for (int i = 0; i < n; i++) {",
                    f"        total += (items[i] * {a}L) % {b};", "        if (total > 10000) total /= 3;", "    }",
                    "    return total;", "}", ""]
    return out


def _file(rng, lang: str, idx: int, plant: str | None) -> tuple[str, int | None]:
    """-> (text, planted line or None)"""
    funcs = _body(rng, lang, rng.randint(6, 18))
    imp, stmt = PLANT[(lang, plant)] if plant else ("", "")
    v = f"{_name(rng)}_{idx}"
    if lang == "python":
        head = [imp] if plant else []
        call = [f"def handle_{idx}():", "    " + stmt.format(v=v), f"    return {v}", ""] if plant else []
        lines = head + ([""] if head else []) + funcs + call
    elif lang == "java":
        cls = "".join(w.title() for w in _name(rng).split("_")) + str(idx)
        call = [f"    static Object handle{idx}() throws Exception {{", "        " + stmt.format(v=v), f"        return {v};",
                "    }"] if plant else []
        lines = ([imp, ""] if plant else []) + [f"public class {cls} {{"] + funcs + call + ["}"]
    elif lang == "go":
        imports = ["\t\"strconv\""] + ([f"\t{imp}"] if plant else [])
        call = [f"func handle{idx}() interface{{}} {{", "\t" + stmt.format(v=v), f"\treturn {v}", "}"] if plant else []
        lines = ["package main", "", "import ("] + imports + [")", ""] + funcs + call
    elif lang == "javascript":
        call = [f"function handle{idx}() {{", "  " + stmt.format(v=v), f"  return {v};", "}"] if plant else []
        lines = ([imp, ""] if plant else []) + funcs + call + ["", "module.exports = {};"]
    else:
        call = [f"void *handle{idx}(void) {{", "    " + stmt.format(v=v), f"    return (void *){v};", "}"] if plant else []
        lines = ([imp, ""] if plant else []) + ["#include <stdlib.h>", ""] + funcs + call
    text = "\n".join(lines) + "\n"
    line = None
    if plant:
        needle = stmt.format(v=v).split("\n")[0]
        line = next(i for i, ln in enumerate(lines, 1) if needle in ln)
    return text, line


def generate(seed: int, out: Path, size: str = "medium") -> dict:
    n_files, n_plant = SIZES[size]
    rng = random.Random(seed)
    root = Path(out) / "corpus"
    planted_at = set(rng.sample(range(n_files), n_plant))
    plants = {i: FAMILIES[k % len(FAMILIES)] for k, i in enumerate(sorted(planted_at))}
    truth, total_bytes = [], 0
    for i in range(n_files):
        lang = LANGS[i % len(LANGS)]
        d = root / f"svc{i // 400:02d}" / lang / f"pkg{(i // 25) % 16:02d}"
        d.mkdir(parents=True, exist_ok=True)
        stem = f"{_name(rng)}_{i:05d}"
        if lang == "java":
            stem = "".join(w.title() for w in stem.split("_"))
        text, line = _file(rng, lang, i, plants.get(i))
        if lang == "java":  # class name must match the file name
            cls = text.split("public class ", 1)[1].split(" ", 1)[0]
            stem = cls
        p = d / (stem + EXT[lang])
        p.write_text(text)
        total_bytes += len(text)
        if i in plants:
            truth.append({"file": str(p.relative_to(out)), "family": plants[i], "line": line, "order": i})
    for k in range(max(2, n_files // 2000)):  # big non-code files a scanner has to get through or skip
        data = root / f"svc{k:02d}" / "data" / f"export_{k}.csv"
        data.parent.mkdir(parents=True, exist_ok=True)
        rows = "\n".join(f"{j},{rng.randint(0, 10**9)},{_name(rng)},{rng.random():.6f}" for j in range(120000))
        data.write_text("id,amount,label,ratio\n" + rows + "\n")
        total_bytes += data.stat().st_size
    meta = {"seed": seed, "size": size, "code_files": n_files, "planted": len(truth), "bytes": total_bytes,
            "families": FAMILIES, "languages": LANGS}
    (Path(out) / "truth.json").write_text(json.dumps({"meta": meta, "planted": truth}, indent=2) + "\n")
    return meta


def score_perf(bom: dict, out: Path) -> dict:
    t = json.loads((Path(out) / "truth.json").read_text())
    planted, meta = t["planted"], t["meta"]
    reported = []  # (path, family)
    for family, _params, occ, _level, _ctx in iter_crypto_findings_ctx(bom):
        for loc, _line in occ:
            if loc:
                reported.append((norm_path(loc), family))
    by_file = {}
    for path, fam in reported:
        by_file.setdefault(path, set()).add(fam)
    found = []
    for p in planted:
        found.append(any(fam == p["family"] and same_file(path, p["file"]) for path, fams in by_file.items() for fam in fams))
    planted_files = [p["file"] for p in planted]
    fps = sum(1 for path, fams in by_file.items() if not any(same_file(path, pf) for pf in planted_files))
    n = len(planted)
    quart = []
    for q in range(4):
        lo, hi = q * meta["code_files"] / 4, (q + 1) * meta["code_files"] / 4
        sel = [f for p, f in zip(planted, found) if lo <= p["order"] < hi]
        quart.append(round(100 * sum(sel) / len(sel), 1) if sel else None)
    recall = round(100 * sum(found) / n, 1) if n else None
    first, last = quart[0], quart[-1]
    falloff = first is not None and last is not None and first - last >= 25
    return {"planted": n, "found": sum(found), "recall": recall, "recall_by_quartile": quart,
            "noise_files_reported": fps, "coverage_falloff": falloff,
            "missed": [p["file"] for p, f in zip(planted, found) if not f][:20]}
