#!/usr/bin/env python3
"""Scorer self-tests: the reference must score perfectly, and specific mistakes must be penalized.

Run: python tools/test_scorer.py   (after tools/build_expected.py)
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cbomlib import load_json, make_component  # noqa: E402
from score import score  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
REF = load_json(ROOT / "expected" / "expected.cdx.json")
B = "corpus/tier4/assets/"


def result(rep, fid):
    return next(r for r in rep["results"] if r["id"] == fid)


def by_file_family(file, family):
    gt = load_json(ROOT / "expected" / "ground_truth.json")
    return next(f["id"] for f in gt["findings"] if f["file"] == B + file and f["family"] == family)


def check(name, cond):
    print(f"[{'ok ' if cond else 'FAIL'}] {name}")
    return cond


def main() -> int:
    ok = True

    rep = score(REF)
    a = rep["summary"]["all/all"]
    ok &= check("reference: 100% recall, params, lines; 0 FP",
                a["recall"] == 100 and a["params_accuracy"] == 100 and a["line_accuracy"] == 100
                and a["false_positives"] == 0)

    # Certificate reported as a bare container (no key / signature refs): its findings are missed.
    bom = copy.deepcopy(REF)
    for c in bom["components"]:
        if c["bom-ref"] == "M-cert-payments":
            c["cryptoProperties"]["certificateProperties"] = {"certificateFormat": "X.509"}
    rep = score(bom)
    ok &= check("cert without refs -> RSA and SHA-1 missed",
                not result(rep, by_file_family("certs/payments_legacy.crt", "RSA"))["detected"]
                and not result(rep, by_file_family("certs/payments_legacy.crt", "SHA-1"))["detected"])

    # Wrong key size on the legacy cert: detected, params wrong.
    bom = copy.deepcopy(REF)
    for c in bom["components"]:
        if c["bom-ref"] == "M-cert-payments-key":
            c["name"] = "RSA-2048"
            c["cryptoProperties"]["algorithmProperties"]["parameterSetIdentifier"] = "2048"
    r = result(score(bom), by_file_family("certs/payments_legacy.crt", "RSA"))
    ok &= check("RSA-1024 reported as RSA-2048 -> params wrong", r["detected"] and r["params_ok"] is False)

    # Commented-out SSLv3 in nginx.conf reported as live: false positive.
    bom = copy.deepcopy(REF)
    bom["components"].append(make_component("x-ssl3", "SSL-3.0", {}, [{"location": B + "tls/nginx.conf", "line": 17}]))
    rep = score(bom)
    ok &= check("commented-out SSLv3 reported -> 1 FP",
                any(fp["family"] == "SSL-3.0" for fp in rep["false_positives"]))

    # Anything reported in the fake PEM: negative-control false positive.
    bom = copy.deepcopy(REF)
    bom["components"].append(make_component("x-fake", "RSA", {"key_size": 2048},
                                            [{"location": "corpus/negatives/assets/upload_validator_fake.pem"}]))
    rep = score(bom)
    ok &= check("algorithm invented for fake PEM -> negative-control FP", rep["summary"]["negatives"]["false_positives"] == 1)

    # OpenSSL-named suite in a protocol component still matches the IANA ground truth.
    bom = copy.deepcopy(REF)
    for c in bom["components"]:
        for cs in (c.get("cryptoProperties", {}).get("protocolProperties") or {}).get("cipherSuites", []):
            if cs["name"] == "TLS_RSA_WITH_3DES_EDE_CBC_SHA":
                cs["name"] = "DES-CBC3-SHA"
    r = result(score(bom), by_file_family("tls/nginx.conf", "TLS_RSA_WITH_3DES_EDE_CBC_SHA"))
    ok &= check("OpenSSL suite name DES-CBC3-SHA matches IANA ground truth", r["detected"])

    # Scanner that can't open the keystore: container findings yes, password-gated findings no.
    bom = copy.deepcopy(REF)
    bom["components"] = [c for c in bom["components"] if not c["bom-ref"].startswith("M-cert-orders")]
    rep = score(bom)
    ok &= check("keystore not opened -> AES/PBKDF2 found, RSA/SHA-256 missed",
                result(rep, by_file_family("keystores/orders_keystore.p12", "AES"))["detected"]
                and not result(rep, by_file_family("keystores/orders_keystore.p12", "RSA"))["detected"])

    # Bytecode scanners report classes inside the jar; that location still matches the jar.
    bom = copy.deepcopy(REF)
    bom["components"] = [c for c in bom["components"] if c["bom-ref"] != "T5-JV-06"]
    bom["components"].append(make_component("x-jar", "AES", {"key_size": 128, "mode": "CBC"}, [
        {"location": "jar:file:/scan/corpus/tier5/java/compiled/billing-core.jar!/com/acme/billing/Settlement.class"}]))
    r = result(score(bom), "T5-JV-06")
    ok &= check("finding inside jar!/Class path matches the jar", r["detected"] and r["params_ok"])

    # --- PQC -----------------------------------------------------------------------------------
    PQ = "corpus/pqc/"

    def drop(bom, ref):
        bom["components"] = [c for c in bom["components"] if c["bom-ref"] != ref]

    # Hybrid group reported as its classical half only: hybrid missed, no credit for migration.
    bom = copy.deepcopy(REF)
    drop(bom, "PQ-AS-09")
    rep = score(bom)
    ok &= check("hybrid X25519MLKEM768 reported as plain X25519 -> hybrid missed",
                not result(rep, "PQ-AS-09")["detected"] and result(rep, "PQ-AS-10")["detected"])

    # Believing the label: ML-KEM reported for the ECDH-only "quantum-safe" file is an over-claim.
    bom = copy.deepcopy(REF)
    bom["components"].append(make_component("x-wash", "ML-KEM", {"param_set": "768"},
                                            [{"location": PQ + "python/pq_washing.py", "line": 12}]))
    bom["components"].append(make_component("x-wash2", "X25519MLKEM768", {},
                                            [{"location": PQ + "assets/tls/nginx_pq_washing.conf", "line": 15}]))
    rep = score(bom)
    ok &= check("PQC-washing labels believed -> 2 PQC over-claims", rep["summary"]["pqc_overclaims"]["count"] == 2)

    # A scanner on a pre-PQC library sees only the OID; the scorer still recognizes ML-DSA-65.
    bom = copy.deepcopy(REF)
    for c in bom["components"]:
        if c["bom-ref"] in ("M-pq-root-key", "M-pq-root-sig"):
            c["name"] = "unknown-algorithm"
            c["cryptoProperties"]["oid"] = "2.16.840.1.101.3.4.3.18"
            c["cryptoProperties"]["algorithmProperties"].pop("parameterSetIdentifier", None)
    r = result(score(bom), "PQ-AS-01")
    ok &= check("ML-DSA cert reported only by OID -> detected, parameter set correct", r["detected"] and r["params_ok"])

    # Wrong parameter set: ML-KEM-512 reported for a 768 key.
    bom = copy.deepcopy(REF)
    for c in bom["components"]:
        if c["bom-ref"] == "PQ-PY-01":
            c["name"] = "ML-KEM-512"
            c["cryptoProperties"]["algorithmProperties"]["parameterSetIdentifier"] = "512"
    r = result(score(bom), "PQ-PY-01")
    ok &= check("ML-KEM-768 reported as ML-KEM-512 -> params wrong", r["detected"] and r["params_ok"] is False)

    # --- Actionability --------------------------------------------------------------------------
    rep = score(REF)
    ok &= check("reference: every detected finding ticket-ready, 100% field completeness",
                rep["actionability"]["ticket_ready_pct"] == 100 and rep["actionability"]["completeness_pct"] == 100)

    # A wrong expiry date is worse than none: it's checked against the real certificate.
    bom = copy.deepcopy(REF)
    for c in bom["components"]:
        if c["bom-ref"] == "M-cert-payments":
            c["cryptoProperties"]["certificateProperties"]["notValidAfter"] = "2029-02-28T00:00:00Z"
    r = result(score(bom), by_file_family("certs/payments_legacy.crt", "RSA"))
    ok &= check("certificate expiry reported wrong -> not ticket-ready",
                r["actionability"]["cert_expiry"] is False and not r["ticket_ready"])

    # No dependency graph: provenance fails, but it's a should-have, so tickets can still be opened.
    bom = copy.deepcopy(REF)
    bom.pop("dependencies")
    r = result(score(bom), "T1-PY-01")
    ok &= check("no library provenance -> should-have fails, still ticket-ready",
                r["actionability"]["provenance"] is False and r["ticket_ready"])

    # RSA with no stated use: is the replacement ML-KEM or ML-DSA? Not ticket-ready.
    bom = copy.deepcopy(REF)
    for c in bom["components"]:
        if c["bom-ref"] == "T1-JV-05":
            c["cryptoProperties"]["algorithmProperties"].pop("primitive")
    r = result(score(bom), "T1-JV-05")
    ok &= check("RSA without a primitive -> not ticket-ready", r["actionability"]["primitive"] is False
                and "primitive" in r["missing_must"])

    # Same recall, different usefulness: names and locations only.
    bom = copy.deepcopy(REF)
    bom.pop("dependencies")
    bom["components"] = [c for c in bom["components"] if c.get("type") != "library"]
    for c in bom["components"]:
        cp = c.get("cryptoProperties", {})
        cp.pop("oid", None)
        for k in ("cryptoFunctions", "nistQuantumSecurityLevel", "primitive"):
            (cp.get("algorithmProperties") or {}).pop(k, None)
        for k in ("subjectName", "issuerName", "notValidBefore", "notValidAfter"):
            (cp.get("certificateProperties") or {}).pop(k, None)
    rep = score(bom)
    ok &= check("names-only CBOM: 100% recall, far from 100% ticket-ready",
                rep["summary"]["all/all"]["recall"] == 100 and rep["actionability"]["ticket_ready_pct"] < 75
                and rep["actionability"]["completeness_pct"] < 40)

    # --- Calibration cases: scored apart, never in the headline -----------------------------------
    rep = score(REF, custom="exclude")
    cal = rep["calibration_results"]
    ok &= check("calibration cases: all detected by the reference, none in the headline",
                cal and all(r["detected"] for r in cal) and not any(r["id"].startswith("CAL-") for r in rep["results"]))
    bom = copy.deepcopy(REF)
    bom["components"].append(make_component("x-cal-fp", "MD5", {}, [{"location": cal[0]["file"], "line": 1}]))
    rep = score(bom, custom="exclude")
    ok &= check("false positive in a calibration file -> not counted in the headline",
                rep["summary"]["all/all"]["false_positives"] == 0 and len(rep["calibration_false_positives"]) == 1)

    # --- Mixed files: site findings -------------------------------------------------------------
    gt = load_json(ROOT / "expected" / "ground_truth.resolved.json")
    pairs = {}
    for f in gt["findings"]:
        if f.get("site"):
            pairs.setdefault((f["file"], f["family"]), []).append(f)
    pair = next(v for v in pairs.values() if len(v) == 2 and v[0]["params"] != v[1]["params"])
    a_id, b_id = pair[0]["id"], pair[1]["id"]
    ids = {a_id, b_id}

    # File-wide guess: one report for the family, at the first site, with the first site's params.
    bom = copy.deepcopy(REF)
    bom["components"] = [c for c in bom["components"] if c["bom-ref"] != b_id]
    rep = score(bom)
    ok &= check("mixed file, second site of a family not reported -> that site missed, no FP",
                result(rep, a_id)["detected"] and not result(rep, b_id)["detected"]
                and rep["summary"]["all/all"]["false_positives"] == 0)

    # Both sites reported, but with the first site's parameters copied to the second.
    bom = copy.deepcopy(REF)
    src = next(c for c in bom["components"] if c["bom-ref"] == a_id)
    for c in bom["components"]:
        if c["bom-ref"] == b_id:
            c["name"], c["cryptoProperties"] = src["name"], copy.deepcopy(src["cryptoProperties"])
    r = result(score(bom), b_id)
    ok &= check("mixed file, first site's params copied to the second -> detected, params wrong",
                r["detected"] and r["params_ok"] is False)

    # One occurrence 40 lines from any site of its family: it can't be placed, so nothing is detected.
    bom = copy.deepcopy(REF)
    for c in bom["components"]:
        if c["bom-ref"] in ids:
            for o in c["evidence"]["occurrences"]:
                o["line"] = max(pair[0]["lines"] + pair[1]["lines"]) + 40
    rep = score(bom)
    ok &= check("mixed file, occurrence far from every site -> both missed",
                not result(rep, a_id)["detected"] and not result(rep, b_id)["detected"])

    # --- Reviewer reproductions (v1.16.1 review) ---------------------------------------------------
    # An extra PBKDF2 occurrence at line 10,000 of a mixed file that does use PBKDF2: no site credit,
    # and it must cost precision.
    pb = next(f for f in gt["findings"] if f.get("site") and f["family"] == "PBKDF2")
    bom = copy.deepcopy(REF)
    bom["components"].append(make_component("x-far-pbkdf2", "PBKDF2", {"hash": "SHA-256"},
                                            [{"location": pb["file"], "line": 10000}]))
    rep = score(bom)
    fps = [x for x in rep["false_positives"] if x["file"] == pb["file"] and x["family"] == "PBKDF2"]
    ok &= check("extra same-family report far from every site -> one false positive, precision below 100%",
                len(fps) == 1 and fps[0].get("kind") == "unplaced" and rep["summary"]["all/all"]["precision"] < 100
                and result(rep, pb["id"])["detected"])

    # Occurrence-level judgement has two neutral cases: an import line names a module, not a use; and
    # a hash or MAC at another algorithm's site is that algorithm's internals (the per-site also_ok).
    # A wrong family at a site (DES reported at a 3DES site) is still a false positive.
    gw = "corpus/mixed/go/report_gateway/main.go"
    imp = next(i for i, t in enumerate((ROOT / gw).read_text().splitlines(), 1) if t.strip() == '"crypto/des"')
    s3 = next(f for f in gt["findings"] if f["file"] == gw and f["family"] == "3DES")
    res = {f["id"]: f for f in load_json(ROOT / "expected" / "ground_truth.resolved.json")["findings"]}
    s3_line = res[s3["id"]]["lines"][-1]
    pk = next(f for f in res.values() if f["file"] == "corpus/mixed/python/metric_service.py" and f["family"] == "PBKDF2")
    bom = copy.deepcopy(REF)
    bom["components"] += [make_component("x-imp-des", "DES", {}, [{"location": gw, "line": imp}]),
                          make_component("x-hmac-in-pbkdf2", "HMAC", {}, [{"location": pk["file"], "line": pk["lines"][0]}]),
                          make_component("x-des-at-3des", "DES", {}, [{"location": gw, "line": s3_line}])]
    rep = score(bom)
    des = [x for x in rep["false_positives"] if x["file"] == gw and x["family"] == "DES"]
    ok &= check("DES on its import line -> neutral; DES at a 3DES site -> one false positive",
                len(des) == 1 and des[0]["lines"] == [s3_line])
    ok &= check("HMAC reported at a pbkdf2_hmac site -> neutral",
                not any(x["file"] == pk["file"] and x["family"] == "HMAC" for x in rep["false_positives"]))

    # Excluding one certificate finding by id must not silence an unrelated false report on that file.
    from score import load_scope  # noqa: E402
    cert = next(f for f in gt["findings"] if f["file"].startswith("corpus/tier4/assets/certs/") and f["family"] == "RSA")
    scope = {"name": "test", "out_of_scope": [{"ids": [cert["id"]], "reason": "test exclusion"}]}
    bom = copy.deepcopy(REF)
    bom["components"].append(make_component("x-fake-mlkem", "ML-KEM", {"param_set": "768"}, [{"location": cert["file"]}]))
    rep = score(bom, scope=scope)
    ok &= check("finding excluded by id; false ML-KEM on the same certificate -> still a false positive (and a PQC over-claim)",
                any(x["file"] == cert["file"] and x["family"] == "ML-KEM" for x in rep["false_positives"])
                and rep["summary"]["pqc_overclaims"]["count"] == 1)

    # A file-level (glob) exclusion still removes the file's false positives: the scanner says it doesn't read it.
    scope = {"name": "test", "out_of_scope": [{"glob": Path(cert["file"]).name, "reason": "doesn't read this file"}]}
    rep = score(bom, scope=scope)
    ok &= check("file excluded by glob -> its false positives are not counted",
                not any(x["file"] == cert["file"] for x in rep["false_positives"]))

    # Rubric values, not presence (v2.1 review): a wrong issuer, start date or key format earns nothing.
    def act_of(bom, fid):
        return result(score(bom), fid)["actionability"]
    cert_id = by_file_family("certs/api_gateway.pem", "RSA")
    bom = copy.deepcopy(REF)
    for c in bom["components"]:
        if c["bom-ref"] == "M-cert-api":
            c["cryptoProperties"]["certificateProperties"].update(issuerName="CN=Somebody Else CA", notValidBefore="2019-05-05T00:00:00Z")
    a_ = act_of(bom, cert_id)
    ok &= check("certificate with the wrong issuer and start date -> both checks fail", a_["cert_issuer"] is False and a_["cert_validity_start"] is False)
    key_id = by_file_family("keys/billing_service.pem", "RSA")
    bom = copy.deepcopy(REF)
    for c in bom["components"]:
        if c["bom-ref"] == "M-key-billing":
            c["cryptoProperties"]["relatedCryptoMaterialProperties"]["format"] = "JWK"
    ok &= check("key reported in the wrong format -> key_format fails", act_of(bom, key_id)["key_format"] is False)
    for c in bom["components"]:
        if c["bom-ref"] == "M-key-billing":
            c["cryptoProperties"]["relatedCryptoMaterialProperties"]["format"] = "pkcs8-pem"
    ok &= check("same format, different spelling -> key_format passes", act_of(bom, key_id)["key_format"] is True)

    # Pre-standard names: discovery credit stays, the standard-name check fails.
    rep = score(REF)
    sn = rep["summary"]["pqc_standard_names"]
    ok &= check("reference: every detected PQC finding reported by its standard name",
                sn["detected"] > 0 and sn["accuracy"] == 100)
    bom = copy.deepcopy(REF)
    renamed = 0
    for c in bom["components"]:
        if c.get("name", "").upper().startswith("ML-KEM-"):
            c["name"] = "Kyber" + c["name"].split("-")[-1]
            c.get("cryptoProperties", {}).pop("oid", None)
            renamed += 1
    rep = score(bom)
    sn2 = rep["summary"]["pqc_standard_names"]
    kem = [r for r in rep["results"] if r["family"] == "ML-KEM"]
    ok &= check("ML-KEM reported as Kyber -> still detected, fails the standard-name check",
                renamed > 0 and all(r["detected"] for r in kem) and sn2["accuracy"] < 100
                and set(sn2["prestandard_only"]) >= {r["id"] for r in kem if r["detected"] and len(r["reported_params"]) == 1})

    print("\nAll scorer checks pass." if ok else "\nScorer checks FAILED.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
