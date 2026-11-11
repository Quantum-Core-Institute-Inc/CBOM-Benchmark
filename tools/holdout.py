#!/usr/bin/env python3
"""Holdout sets: fresh, seeded variants of the Tier 1-2 patterns, scored apart from the published corpus.

The published corpus is public, and a scanner team that works from its scorecard will fix the exact
lines it misses. That's the point of a scorecard, but after a few releases the published score stops
predicting how the scanner does on code it hasn't seen. A holdout set measures that directly:

  python tools/holdout.py generate --seed 8410375 --out holdout-run     # files + answer key
  qci-pqc scan holdout-run/corpus --out holdout-run/scan                 # any scanner
  python tools/holdout.py score holdout-run/scan/cbom.json --dir holdout-run [--published report.json]

Every generated file executes (Python with `cryptography`, Java on the JDK; ML-KEM/ML-DSA need a
24+ runtime, as in the published corpus). Variation is combinatorial: which API spelling, how the
algorithm or parameter reaches the call (literal, module constant, config map, default argument,
class attribute, enum, overload), how modules are imported (plain, aliased, from-import, fully
qualified), identifier names, filler code and file order. Negative files carry algorithm names in
log messages and constants only, including post-quantum claims.

Keep the seed private and generate per run (the CI template uses a secret). Anyone can read this
generator, and covering everything it emits is fine: that's a broad slice of real API usage, which
is what the corpus is for. What it prevents is fitting to a particular set of files.

The overfit gap compares recall on the published Tier 1-2 cases with recall on the holdout, family
by family, weighted by the holdout's family mix. Positive means the published score flatters the
scanner. A bootstrap interval says whether the gap is bigger than this holdout's sampling noise.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cbomlib import FAMILIES, functions_for, load_json, make_bom, make_component, oid_for  # noqa: E402
from holdout_common import DOCS, VERBS, WORDS, Names, spec, sub  # noqa: E402,F401

ROOT = Path(__file__).resolve().parent.parent
GENERATOR_VERSION = "1.2"  # 1.1: certificates, keys, keystores, configs, compiled artifacts
#                            1.2: C#, Apache/HAProxy/IPsec configs, LMS/XMSS policies, minified JS, native binaries

# ----------------------------------------------------------------------------------------------
# Names. Domain words only: identifiers never name the algorithm (a grep for "md5" shouldn't win
# because a variable was called md5_digest).
# ----------------------------------------------------------------------------------------------
# Specs. Each returns one finding's code: placeholders are <<S>> (the slot that indirection may
# hoist), <<d>> (input bytes), <<x1>>.. (locals) and module refs (<<hashlib>>). Lines starting
# with "@" are anchor lines. "ret" is the returned expression. Spec functions get the rng.

def mods_py():
    return {
        "hashlib": [("import hashlib", "hashlib"), ("import hashlib as {a}", "{a}")],
        "hmac": [("import hmac", "hmac"), ("import hmac as {a}", "{a}")],
        "os": [("import os", "os"), ("import os as {a}", "{a}")],
        "hashes": [("from cryptography.hazmat.primitives import hashes", "hashes"),
                   ("from cryptography.hazmat.primitives import hashes as {a}", "{a}")],
        "chmac": [("from cryptography.hazmat.primitives import hmac as {a}", "{a}")],
        "Cipher": [("from cryptography.hazmat.primitives.ciphers import Cipher", "Cipher"),
                   ("from cryptography.hazmat.primitives import ciphers as {a}", "{a}.Cipher")],
        "algorithms": [("from cryptography.hazmat.primitives.ciphers import algorithms", "algorithms"),
                       ("from cryptography.hazmat.primitives.ciphers import algorithms as {a}", "{a}")],
        "modes": [("from cryptography.hazmat.primitives.ciphers import modes", "modes"),
                  ("from cryptography.hazmat.primitives.ciphers import modes as {a}", "{a}")],
        "AESGCM": [("from cryptography.hazmat.primitives.ciphers.aead import AESGCM", "AESGCM"),
                   ("from cryptography.hazmat.primitives.ciphers import aead", "aead.AESGCM"),
                   ("from cryptography.hazmat.primitives.ciphers.aead import AESGCM as {A}", "{A}")],
        "CCP": [("from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305", "ChaCha20Poly1305"),
                ("from cryptography.hazmat.primitives.ciphers import aead", "aead.ChaCha20Poly1305"),
                ("from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 as {A}", "{A}")],
        "TripleDES": [("from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES", "TripleDES"),
                      ("from cryptography.hazmat.decrepit.ciphers import algorithms as {a}", "{a}.TripleDES")],
        "PBKDF2HMAC": [("from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC", "PBKDF2HMAC"),
                       ("from cryptography.hazmat.primitives.kdf import pbkdf2", "pbkdf2.PBKDF2HMAC")],
        "rsa_gen": [("from cryptography.hazmat.primitives.asymmetric import rsa", "rsa.generate_private_key"),
                    ("from cryptography.hazmat.primitives.asymmetric import rsa as {a}", "{a}.generate_private_key"),
                    ("from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key", "generate_private_key"),
                    ("from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key as {a}", "{a}")],
        "dsa_gen": [("from cryptography.hazmat.primitives.asymmetric import dsa", "dsa.generate_private_key"),
                    ("from cryptography.hazmat.primitives.asymmetric import dsa as {a}", "{a}.generate_private_key")],
        "ec": [("from cryptography.hazmat.primitives.asymmetric import ec", "ec"),
               ("from cryptography.hazmat.primitives.asymmetric import ec as {a}", "{a}")],
        "dh": [("from cryptography.hazmat.primitives.asymmetric import dh", "dh"),
               ("from cryptography.hazmat.primitives.asymmetric import dh as {a}", "{a}")],
        "Ed": [("from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey", "Ed25519PrivateKey"),
               ("from cryptography.hazmat.primitives.asymmetric import ed25519", "ed25519.Ed25519PrivateKey"),
               ("from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey as {A}", "{A}")],
        "X": [("from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey", "X25519PrivateKey"),
              ("from cryptography.hazmat.primitives.asymmetric import x25519", "x25519.X25519PrivateKey"),
              ("from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey as {A}", "{A}")],
        "mlkem": [("from cryptography.hazmat.primitives.asymmetric import mlkem", "mlkem"),
                  ("from cryptography.hazmat.primitives.asymmetric import mlkem as {a}", "{a}")],
        "mldsa": [("from cryptography.hazmat.primitives.asymmetric import mldsa", "mldsa"),
                  ("from cryptography.hazmat.primitives.asymmetric import mldsa as {a}", "{a}")],
    }


HASH_PY = {"MD5": ("md5", "MD5"), "SHA-1": ("sha1", "SHA1"), "SHA-256": ("sha256", "SHA256"),
           "SHA-512": ("sha512", "SHA512"), "SHA3-256": ("sha3_256", "SHA3_256")}


def py_specs():
    def hashlib_attr(r, m=False):
        fam = r.choice(list(HASH_PY))
        return spec(fam, {}, ["@<<x1>> = <<S>>(<<d>>).hexdigest()"], "<<x1>>", f"<<hashlib>>.{HASH_PY[fam][0]}",
                    api="hashlib.<name>", carries_family=True)

    def hashlib_new(r, m=False):
        fam = r.choice(list(HASH_PY))
        name = HASH_PY[fam][0]
        name = name.upper() if r.random() < 0.3 and "3" not in name else name
        return spec(fam, {}, ["@<<x1>> = <<hashlib>>.new(<<S>>, <<d>>).hexdigest()"], "<<x1>>", f'"{name}"', "str",
                    api="hashlib.new", carries_family=True)

    def pyca_hash(r, m=False):
        fam = r.choice(list(HASH_PY))
        return spec(fam, {}, ["@<<x1>> = <<hashes>>.Hash(<<S>>())", "<<x1>>.update(<<d>>)"], "<<x1>>.finalize()",
                    f"<<hashes>>.{HASH_PY[fam][1]}", api="hashes.Hash", carries_family=True)

    def hmac_new(r, m=False):
        fam = r.choice(["SHA-1", "SHA-256"] if m else ["SHA-1", "SHA-256", "SHA-512", "MD5"])
        slot = f'"{HASH_PY[fam][0]}"' if r.random() < 0.5 else f"<<hashlib>>.{HASH_PY[fam][0]}"
        return spec("HMAC", {"hash": fam}, ['@<<x1>> = <<hmac>>.new(b"svc-<<w>>", <<d>>, <<S>>).hexdigest()'], "<<x1>>",
                    slot, "str" if slot.startswith('"') else "expr", also_ok=[fam], api="hmac.new")

    def pyca_hmac(r, m=False):
        fam = r.choice(["SHA-1", "SHA-256", "SHA-512"])
        return spec("HMAC", {"hash": fam}, ['@<<x1>> = <<chmac>>.HMAC(b"svc-<<w>>", <<S>>())', "<<x1>>.update(<<d>>)"],
                    "<<x1>>.finalize()", f"<<hashes>>.{HASH_PY[fam][1]}", also_ok=[fam], api="cryptography HMAC")

    def pbkdf2_stdlib(r, m=False):
        fam = r.choice(["SHA-1", "SHA-256", "SHA-512"])
        return spec("PBKDF2", {"hash": fam}, ['@<<x1>> = <<hashlib>>.pbkdf2_hmac(<<S>>, <<d>>, b"salt-<<w>>", 1000)'],
                    "<<x1>>", f'"{HASH_PY[fam][0]}"', "str", also_ok=[fam, "HMAC"], api="hashlib.pbkdf2_hmac")

    def pbkdf2_pyca(r, m=False):
        fam = "SHA-256" if m else r.choice(["SHA-1", "SHA-256", "SHA-512"])
        return spec("PBKDF2", {"hash": fam},
                    ['@<<x1>> = <<PBKDF2HMAC>>(algorithm=<<S>>(), length=32, salt=b"salt-<<w>>", iterations=1000)'],
                    "<<x1>>.derive(<<d>>)", f"<<hashes>>.{HASH_PY[fam][1]}", also_ok=[fam, "HMAC"], api="PBKDF2HMAC")

    def aes_cipher(r, m=False):
        nbytes = r.choice([16, 24, 32])
        mode = r.choice(["CBC", "ECB"] if m else ["CBC", "ECB", "CTR", "GCM"])
        arg = {"CBC": "<<os>>.urandom(16)", "CTR": "<<os>>.urandom(16)", "GCM": "<<os>>.urandom(12)", "ECB": ""}[mode]
        if m == 2:
            body = [f"@<<x2>> = <<os>>.urandom({nbytes})",
                    f"@<<x1>> = <<Cipher>>(<<S>>(<<x2>>), <<modes>>.{mode}({arg})).encryptor()"]
            return spec("AES", {"key_size": nbytes * 8, "mode": mode}, body, "<<x1>>.update(<<d32>>) + <<x1>>.finalize()",
                        "<<algorithms>>.AES", api=f"Cipher(AES, {mode})", carries_family=True)
        hide_mode = r.random() < 0.5
        mode_expr = "<<S>>" if hide_mode else f"<<modes>>.{mode}"
        size_expr = str(nbytes) if hide_mode else "<<S>>"
        body = [f"@<<x2>> = <<os>>.urandom({size_expr})",
                f"@<<x1>> = <<Cipher>>(<<algorithms>>.AES(<<x2>>), {mode_expr}({arg})).encryptor()"]
        return spec("AES", {"key_size": nbytes * 8, "mode": mode}, body, "<<x1>>.update(<<d32>>) + <<x1>>.finalize()",
                    f"<<modes>>.{mode}" if hide_mode else str(nbytes), "expr" if hide_mode else "num",
                    api=f"Cipher(AES, {mode})")

    def aesgcm(r, m=False):
        bits = r.choice([128, 192, 256])
        return spec("AES", {"key_size": bits, "mode": "GCM"},
                    ["@<<x2>> = <<AESGCM>>.generate_key(bit_length=<<S>>)", "@<<x1>> = <<AESGCM>>(<<x2>>)"],
                    "<<x1>>.encrypt(<<os>>.urandom(12), <<d>>, None)", str(bits), "num", api="AESGCM")

    def tdes(r, m=False):
        mode = "CBC" if m else r.choice(["CBC", "ECB"])
        arg = "<<os>>.urandom(8)" if mode == "CBC" else ""
        return spec("3DES", {"mode": mode},
                    [f"@<<x1>> = <<Cipher>>(<<TripleDES>>(<<os>>.urandom(24)), <<S>>({arg})).encryptor()"],
                    "<<x1>>.update(<<d32>>) + <<x1>>.finalize()", f"<<modes>>.{mode}", api="TripleDES")

    def chacha(r, m=False):
        return spec("ChaCha20-Poly1305", {}, ["@<<x1>> = <<S>>(<<S>>.generate_key())"],
                    "<<x1>>.encrypt(<<os>>.urandom(12), <<d>>, None)", "<<CCP>>", api="ChaCha20Poly1305",
                    carries_family=True)

    def rsa(r, m=False):
        bits = r.choice([1024, 2048, 3072, 4096])
        return spec("RSA", {"key_size": bits}, ["@<<x1>> = <<rsa_gen>>(public_exponent=65537, key_size=<<S>>)"],
                    "<<x1>>.public_key().public_numbers().n", str(bits), "num", api="rsa.generate_private_key")

    def dsa(r, m=False):
        bits = r.choice([1024, 2048])
        return spec("DSA", {"key_size": bits}, ["@<<x1>> = <<dsa_gen>>(key_size=<<S>>)"],
                    "<<x1>>.public_key().public_numbers().y", str(bits), "num", api="dsa.generate_private_key")

    def ec_key(r, m=False):
        curve, cls = r.choice([("P-256", "SECP256R1"), ("P-384", "SECP384R1"), ("P-521", "SECP521R1")])
        sign = r.random() < 0.5
        body = ["@<<x1>> = <<ec>>.generate_private_key(<<S>>())"]
        ret = "<<x1>>.public_key().public_numbers().x"
        if sign:
            ret = "<<x1>>.sign(<<d>>, <<ec>>.ECDSA(<<hashes>>.SHA256()))"
        return spec("EC", {"curve": curve}, body, ret, f"<<ec>>.{cls}", also_ok=["SHA-256"] if sign else [],
                    api="ec.generate_private_key" + (" + ECDSA" if sign else ""))

    def ed(r, m=False):
        return spec("Ed25519", {}, ["@<<x1>> = <<S>>.generate()"], "<<x1>>.sign(<<d>>)", "<<Ed>>", api="Ed25519PrivateKey",
                    carries_family=True)

    def x(r, m=False):
        return spec("X25519", {}, ["@<<x1>> = <<S>>.generate()", "@<<x2>> = <<S>>.generate()"],
                    "<<x1>>.exchange(<<x2>>.public_key())", "<<X>>", api="X25519PrivateKey",
                    carries_family=True)

    def dh(r, m=False):
        bits = r.choice([512, 1024])
        return spec("DH", {"key_size": bits}, ["@<<x1>> = <<dh>>.generate_parameters(generator=2, key_size=<<S>>)"],
                    "<<x1>>.generate_private_key().public_key().public_numbers().y", str(bits), "num",
                    api="dh.generate_parameters")

    def mlkem(r, m=False):
        ps = r.choice(["768", "1024"])
        return spec("ML-KEM", {"param_set": ps}, ["@<<x1>> = <<S>>.generate()"],
                    "<<x1>>.public_key().encapsulate()[1]", f"<<mlkem>>.MLKEM{ps}PrivateKey", api="mlkem")

    def mldsa(r, m=False):
        ps = r.choice(["44", "65", "87"])
        return spec("ML-DSA", {"param_set": ps}, ["@<<x1>> = <<S>>.generate()"], "<<x1>>.sign(<<d>>)",
                    f"<<mldsa>>.MLDSA{ps}PrivateKey", api="mldsa")

    t1 = [hashlib_attr, hmac_new, pbkdf2_pyca, aes_cipher, aesgcm, tdes, chacha, rsa, dsa, ec_key, ed, x, dh]
    t2 = t1 + [hashlib_new, pyca_hash]  # the published corpus uses these only behind indirection
    return t1, t2, t2 + [pyca_hmac, pbkdf2_stdlib, mlkem, mldsa]


def mods_java():
    def j(pkg, cls):
        return [(f"import {pkg}.{cls};", cls), (f"import {pkg}.*;", cls), ("", f"{pkg}.{cls}")]
    return {
        "MessageDigest": j("java.security", "MessageDigest"),
        "KeyPairGenerator": j("java.security", "KeyPairGenerator"),
        "Signature": j("java.security", "Signature"),
        "KeyPair": j("java.security", "KeyPair"),
        "Mac": j("javax.crypto", "Mac"),
        "Cipher": j("javax.crypto", "Cipher"),
        "KeyGenerator": j("javax.crypto", "KeyGenerator"),
        "KeyAgreement": j("javax.crypto", "KeyAgreement"),
        "SecretKeyFactory": j("javax.crypto", "SecretKeyFactory"),
        "KEM": j("javax.crypto", "KEM"),
        "SecretKeySpec": j("javax.crypto.spec", "SecretKeySpec"),
        "PBEKeySpec": j("javax.crypto.spec", "PBEKeySpec"),
        "IvParameterSpec": j("javax.crypto.spec", "IvParameterSpec"),
        "ECGenParameterSpec": j("java.security.spec", "ECGenParameterSpec"),
    }


def java_specs():
    def md(r, m=False):
        names = [("MD5", "MD5"), ("SHA-1", "SHA-1"), ("SHA-256", "SHA-256"), ("SHA-512", "SHA-512"), ("SHA3-256", "SHA3-256")]
        fam, name = r.choice(names if m else names + [("SHA-1", "SHA1"), ("SHA-1", "SHA")])
        return spec(fam, {}, ["@byte[] <<x1>> = <<MessageDigest>>.getInstance(<<S>>).digest(<<d>>);"], "<<x1>>",
                    f'"{name}"', "str", api="MessageDigest", carries_family=True)

    def mac(r, m=False):
        fam = "SHA-256" if m else r.choice(["MD5", "SHA-1", "SHA-256", "SHA-512"])
        name = "Hmac" + fam.replace("-", "")
        return spec("HMAC", {"hash": fam},
                    ["@<<Mac>> <<x1>> = <<Mac>>.getInstance(<<S>>);",
                     '<<x1>>.init(new <<SecretKeySpec>>("svc-<<w>>".getBytes(), <<x1>>.getAlgorithm()));'],
                    "<<x1>>.doFinal(<<d>>)", f'"{name}"', "str", also_ok=[fam], api="Mac",
                    carries_family=True)

    def pbkdf2(r, m=False):
        fam = "SHA-256" if m else r.choice(["SHA-1", "SHA-256", "SHA-512"])
        return spec("PBKDF2", {"hash": fam},
                    ["@<<SecretKeyFactory>> <<x1>> = <<SecretKeyFactory>>.getInstance(<<S>>);",
                     '<<PBEKeySpec>> <<x2>> = new <<PBEKeySpec>>("pw-<<w>>".toCharArray(), <<d>>, 1000, 256);'],
                    "<<x1>>.generateSecret(<<x2>>).getEncoded()", f'"PBKDF2WithHmac{fam.replace("-", "")}"', "str",
                    also_ok=[fam, "HMAC"], api="SecretKeyFactory PBKDF2", carries_family=True)

    def aes(r, m=False):
        bits = r.choice([128, 192, 256])
        published = [("ECB", "AES/ECB/PKCS5Padding"), ("GCM", "AES/GCM/NoPadding")]
        mode, transform = r.choice(published if m else
                                   published + [("CBC", "AES/CBC/PKCS5Padding"), ("CTR", "AES/CTR/NoPadding"), ("ECB", "AES")])
        hide_size = False if m == 2 else r.random() < 0.4
        cipher_arg = '"' + transform + '"' if hide_size else "<<S>>"
        body = ['@<<KeyGenerator>> <<x1>> = <<KeyGenerator>>.getInstance("AES");',
                f"@<<x1>>.init({'<<S>>' if hide_size else bits});",
                f"@<<Cipher>> <<x2>> = <<Cipher>>.getInstance({cipher_arg});",
                "<<x2>>.init(<<Cipher>>.ENCRYPT_MODE, <<x1>>.generateKey());"]
        return spec("AES", {"key_size": bits, "mode": mode}, body, "<<x2>>.doFinal(<<d>>)",
                    str(bits) if hide_size else f'"{transform}"', "num" if hide_size else "str",
                    api=f"Cipher {transform}", carries_family=not hide_size)

    def tdes(r, m=False):
        mode = "CBC" if m else r.choice(["CBC", "ECB"])
        body = ['<<KeyGenerator>> <<x1>> = <<KeyGenerator>>.getInstance("DESede");',
                "@<<Cipher>> <<x2>> = <<Cipher>>.getInstance(<<S>>);",
                "<<x2>>.init(<<Cipher>>.ENCRYPT_MODE, <<x1>>.generateKey());"]
        return spec("3DES", {"mode": mode}, body, "<<x2>>.doFinal(<<d>>)", f'"DESede/{mode}/PKCS5Padding"', "str",
                    api="Cipher DESede", carries_family=True)

    def chacha(r, m=False):
        body = ['<<KeyGenerator>> <<x1>> = <<KeyGenerator>>.getInstance("ChaCha20");',
                "@<<Cipher>> <<x2>> = <<Cipher>>.getInstance(<<S>>);",
                "<<x2>>.init(<<Cipher>>.ENCRYPT_MODE, <<x1>>.generateKey(), new <<IvParameterSpec>>(new byte[12]));"]
        return spec("ChaCha20-Poly1305", {}, body, "<<x2>>.doFinal(<<d>>)", '"ChaCha20-Poly1305"', "str",
                    api="Cipher ChaCha20-Poly1305")

    def kpg(family, alg, sizes, api, partner=None):
        def f(r, m=False):
            bits = r.choice(sizes)
            hide_size = False if m == 2 else r.random() < 0.5
            alg_arg = '"' + alg + '"' if hide_size else "<<S>>"
            body = [f"@<<KeyPairGenerator>> <<x1>> = <<KeyPairGenerator>>.getInstance({alg_arg});",
                    f"@<<x1>>.initialize({'<<S>>' if hide_size else bits});"]
            also = []
            if m and partner:  # the published cases pair key generation with its use
                body.append(f'@<<{partner[0]}>> <<x3>> = <<{partner[0]}>>.getInstance("{partner[1]}");')
                also = partner[2]
            return spec(family, {"key_size": bits}, body, "<<x1>>.generateKeyPair().getPublic().getEncoded()",
                        str(bits) if hide_size else f'"{alg}"', "num" if hide_size else "str", also_ok=also, api=api,
                        carries_family=not hide_size)
        return f

    def ec(r, m=False):
        curve, name = r.choice([("P-256", "secp256r1"), ("P-384", "secp384r1"), ("P-521", "secp521r1")])
        body = ['@<<KeyPairGenerator>> <<x1>> = <<KeyPairGenerator>>.getInstance("EC");',
                "@<<x1>>.initialize(new <<ECGenParameterSpec>>(<<S>>));"]
        also = []
        if m:
            body.append('@<<Signature>> <<x3>> = <<Signature>>.getInstance("SHA256withECDSA");')
            also = ["SHA-256"]
        return spec("EC", {"curve": curve}, body, "<<x1>>.generateKeyPair().getPublic().getEncoded()",
                    f'"{name}"', "str", also_ok=also, api="KeyPairGenerator EC")

    def named(family, names, tail, api, literal):
        def f(r, m=False):
            alg = r.choice(names)
            # matched: the published cases name the algorithm again where it's used ("Ed25519", "X25519");
            # broad: the use site asks the key for its algorithm instead
            use = tail[0].replace("<<x1>>.getPrivate().getAlgorithm()", f'"{literal}"') if m else tail[0]
            body = ["@<<KeyPair>> <<x1>> = <<KeyPairGenerator>>.getInstance(<<S>>).generateKeyPair();",
                    ("@" if m else "") + use] + tail[1:]
            return spec(family, {}, body, "<<x2>>", f'"{alg}"', "str", api=api, carries_family=True)
        return f

    ed = named("Ed25519", ["Ed25519"],
               ["<<Signature>> <<x3>> = <<Signature>>.getInstance(<<x1>>.getPrivate().getAlgorithm());",
                "<<x3>>.initSign(<<x1>>.getPrivate());", "<<x3>>.update(<<d>>);", "byte[] <<x2>> = <<x3>>.sign();"],
               "KeyPairGenerator Ed25519", "Ed25519")
    xdh = named("X25519", ["X25519"],
                ["<<KeyAgreement>> <<x3>> = <<KeyAgreement>>.getInstance(<<x1>>.getPrivate().getAlgorithm());",
                 "<<x3>>.init(<<x1>>.getPrivate());", "<<x3>>.doPhase(<<x1>>.getPublic(), true);",
                 "byte[] <<x2>> = <<x3>>.generateSecret();"], "KeyPairGenerator X25519", "X25519")

    def mlkem(r, m=False):
        ps = r.choice(["512", "768", "1024"])
        body = ["@<<KeyPair>> <<x1>> = <<KeyPairGenerator>>.getInstance(<<S>>).generateKeyPair();",
                "<<KEM>> <<x3>> = <<KEM>>.getInstance(<<x1>>.getPublic().getAlgorithm());"]
        return spec("ML-KEM", {"param_set": ps}, body,
                    "<<x3>>.newEncapsulator(<<x1>>.getPublic()).encapsulate().encapsulation()", f'"ML-KEM-{ps}"', "str",
                    api="KeyPairGenerator ML-KEM")

    def mldsa(r, m=False):
        ps = r.choice(["44", "65", "87"])
        body = ["@<<KeyPair>> <<x1>> = <<KeyPairGenerator>>.getInstance(<<S>>).generateKeyPair();",
                "<<Signature>> <<x3>> = <<Signature>>.getInstance(<<x1>>.getPrivate().getAlgorithm());",
                "<<x3>>.initSign(<<x1>>.getPrivate());", "<<x3>>.update(<<d>>);"]
        return spec("ML-DSA", {"param_set": ps}, body, "<<x3>>.sign()", f'"ML-DSA-{ps}"', "str",
                    api="KeyPairGenerator ML-DSA")

    rsa = kpg("RSA", "RSA", [1024, 2048, 3072], "KeyPairGenerator RSA", ("Signature", "SHA256withRSA", ["SHA-256"]))
    dsa = kpg("DSA", "DSA", [1024, 2048], "KeyPairGenerator DSA", ("Signature", "SHA256withDSA", ["SHA-256"]))
    dh = kpg("DH", "DH", [2048, 3072], "KeyPairGenerator DH", ("KeyAgreement", "DH", []))
    t1 = [md, mac, pbkdf2, aes, tdes, rsa, dsa, dh, ec, ed, xdh]
    return t1, t1, t1 + [chacha, mlkem, mldsa]


# ----------------------------------------------------------------------------------------------
# Assembly

FILLER_PY = [
    ["def <<f>>(items):", "    return sorted(set(items))[:<<n>>]"],
    ["def <<f>>(text):", "    return \" \".join(part.capitalize() for part in text.split(\"_\"))"],
    ["def <<f>>(rows):", "    total = 0", "    for row in rows:", "        total += len(str(row))", "    return total"],
    ["def <<f>>(value, low=<<n>>, high=<<m>>):", "    return max(low, min(high, value))"],
]
FILLER_JAVA = [
    ["    static int <<f>>(int[] xs) {", "        int t = 0;", "        for (int x : xs) t += x;", "        return t % <<n>>;", "    }"],
    ["    static String <<f>>(String s) {", "        return s.trim().toLowerCase().replace(' ', '-');", "    }"],
    ["    static int <<f>>(int v) {", "        return Math.max(<<n>>, Math.min(<<m>>, v));", "    }"],
]
NEG_PHRASES = ["SHA-1 fingerprints shown for legacy devices only", "AES-256-GCM is the default for new tenants",
               "X25519MLKEM768 negotiated where the client supports it", "3DES PIN blocks retired in Q3",
               "DSA signing keys revoked", "ChaCha20-Poly1305 preferred on mobile", "ML-KEM-1024 pilot for the archive tier",
               "SHA3-256 checksums in the export manifest", "DH group 14 disabled on the bastion",
               "legacy MD5 fingerprints were removed in v3", "rotate RSA-2048 signing keys before the 2030 cutoff",
               "ML-KEM-768 rollout approved for all tenants", "AES/ECB/PKCS5Padding is rejected by the linter",
               "column sha1_checksum is deprecated", "TLS_RSA_WITH_3DES_EDE_CBC_SHA disabled at the edge",
               "quantum-safe: ML-DSA-65 signatures (FIPS 204)", "HmacSHA256 webhook check moved to the gateway",
               "ECDSA P-256 certificates expire in March", "Ed25519 deploy keys only", "PBKDF2 iterations raised"]


class FileBuilder:
    """Collects one generated file's findings, applying an indirection style to each."""

    def __init__(self, lang, rng, names, imports="canonical"):
        """imports: 'canonical' (how the published corpus imports), 'alias' (renamed modules, a Tier 2
        indirection) or 'any'."""
        self.lang, self.rng, self.names, self.import_mode = lang, rng, names, imports
        self.imports, self.refs = set(), {}
        self.top, self.funcs, self.mains = [], [], []  # lists of (text, anchor_id|None)
        self.fset = set()

    def ref(self, mod):
        if mod not in self.refs:
            opts = (mods_py() if self.lang == "python" else mods_java())[mod]
            if self.import_mode == "canonical":
                opts = opts[:1]
            elif self.import_mode == "alias" and len(opts) > 1:
                opts = opts[1:]
            imp, ref = self.rng.choice(opts)
            a, A = self.names.alias(), self.names.cap()
            imp, ref = imp.format(a=a, A=A), ref.format(a=a, A=A)
            if imp:
                self.imports.add(imp)
            self.refs[mod] = ref
        return self.refs[mod]

    def mapping(self, text_parts):
        m = {}
        for t in text_parts:
            for name in re.findall(r"<<(\w+)>>", t):
                if name in m or name in ("S", "d", "d32", "w") or re.fullmatch(r"x\d", name):
                    continue
                m[name] = self.ref(name)
        return m

    def add(self, sp, style, fid):
        rng, nm = self.rng, self.names
        parts = sp["body"] + [sp["ret"], sp["slot"] or ""]
        m = self.mapping(parts)
        m.update({f"x{i}": nm.var() for i in range(1, 5)}, w=rng.choice(WORDS))
        slot = sub(sp["slot"], m) if sp["slot"] else None
        fn = nm.snake() if self.lang == "python" else nm.camel()
        py = self.lang == "python"
        if py:
            m["d"], m["d32"] = f'b"{rng.choice(WORDS)}-{rng.randint(100, 999)}"', 'b"0123456789abcdef0123456789abcdef"'
        else:
            m["d"] = f'"{rng.choice(WORDS)}-{rng.randint(100, 999)}".getBytes()'
        jtype = {"str": "String", "num": "int"}.get(sp["kind"])
        params_sig, call_args = "", ""
        if style in ("inline", "alias"):  # alias: the indirection is in the imports
            m["S"] = slot
        elif style == "const":
            c = nm.const()
            self.top.append((f"{c} = {slot}" if py else f"    private static final {jtype} {c} = {slot};", fid))
            m["S"] = c
        elif style == "config":
            c, k = nm.const(), nm.key()
            if py:
                self.top.append((f'{c} = {{"service": "{rng.choice(WORDS)}", "{k}": {slot}, "retries": 3}}', fid))
            else:
                other = f'"region", "{rng.choice(WORDS)}"' if jtype == "String" else '"retries", 3'
                box = "String" if jtype == "String" else "Integer"
                self.top.append((f"    private static final java.util.Map<String, {box}> {c} = "
                                 f'java.util.Map.of({other}, "{k}", {slot});', fid))
            m["S"] = f'{c}["{k}"]' if py else f'{c}.get("{k}")'
        elif style == "default":  # python only
            p = nm.key()
            params_sig = f"{p}={slot}"
            m["S"] = p
        elif style == "classattr":  # python only
            c, a = nm.cap(), nm.const()
            self.top += [(f"class {c}:", None), (f"    {a} = {slot}", fid), ("", None)]
            m["S"] = f"{c}.{a}"
        elif style == "enum":  # java only
            e, k = nm.cap(), rng.choice(["LEGACY", "DEFAULT", "STANDARD", "PRIMARY", "FALLBACK"])
            self.top.append((f"    enum {e} {{ {k}({slot}); final {jtype} v; {e}({jtype} v) {{ this.v = v; }} }}", fid))
            m["S"] = f"{e}.{k}.v"
        elif style == "overload":  # java only
            p = nm.key().replace("_", "")
            params_sig, call_args = f"{jtype} {p}", slot
            m["S"] = p
        else:
            raise ValueError(style)

        out = []
        if py:
            if params_sig:
                out.append((f"def {fn}({params_sig}):", fid))
            else:
                out.append((f"def {fn}():", None))
            for line in sp["body"]:
                out.append(("    " + sub(line.lstrip("@"), m), fid if line.startswith("@") else None))
            out += [("    return " + sub(sp["ret"], m), None), ("", None), ("", None)]
            self.mains.append(f"    print(\"{fn}\", len(repr({fn}())))")
        else:
            if style == "overload":
                out.append((f"    static Object {fn}() throws Exception {{ return {fn}({call_args}); }}", fid))
            out.append((f"    static Object {fn}({params_sig}) throws Exception {{", None))
            for line in sp["body"]:
                out.append(("        " + sub(line.lstrip("@"), m), fid if line.startswith("@") else None))
            out += [("        return " + sub(sp["ret"], m) + ";", None), ("    }", None), ("", None)]
            self.mains.append(f"        System.out.println(\"{fn} \" + String.valueOf({fn}()).length());")
        self.funcs.append(out)

    def filler(self):
        tpl = self.rng.choice(FILLER_PY if self.lang == "python" else FILLER_JAVA)
        f = self.names.snake() if self.lang == "python" else self.names.camel()
        n, mm = self.rng.randint(2, 9), self.rng.randint(10, 99)
        body = [(sub(t, {"f": f, "n": str(n), "m": str(mm)}), None) for t in tpl] + [("", None)] + ([("", None)] if self.lang == "python" else [])
        self.funcs.append(body)

    def render(self, cls=None):
        self.rng.shuffle(self.funcs)
        imps = sorted(self.imports, key=lambda s: (not s.startswith("import "), s))
        if self.lang == "python":
            w = self.rng.choice(WORDS)
            doc = self.rng.choice(DOCS).format(w=w, W=w.capitalize())
            lines = [(f'"""{doc}"""', None)] + [(i, None) for i in imps] + [("", None), ("", None)]
            if self.top:
                lines += self.top + [("", None), ("", None)]
            for fbody in self.funcs:
                lines += fbody
            lines += [("def main():", None)] + [(x, None) for x in self.mains] + [("", None), ("", None),
                                                                                    ('if __name__ == "__main__":', None),
                                                                                    ("    main()", None)]
        else:
            lines = [(i, None) for i in imps] + ([("", None)] if imps else []) + [(f"public class {cls} {{", None)]
            lines += self.top + ([("", None)] if self.top else [])
            for fbody in self.funcs:
                lines += fbody
            lines += [("    public static void main(String[] args) throws Exception {", None)]
            lines += [(x, None) for x in self.mains] + [("    }", None), ("}", None)]
        text = "\n".join(t for t, _ in lines) + "\n"
        anchors = defaultdict(list)
        for i, (_, fid) in enumerate(lines, 1):
            if fid:
                anchors[fid].append(i)
        return text, anchors


FAMILY_MENU = {lang: ["MD5", "SHA-1", "SHA-256", "SHA-512", "SHA3-256", "HMAC", "PBKDF2", "AES", "3DES",
                       "ChaCha20-Poly1305", "RSA", "DSA", "EC", "Ed25519", "X25519", "DH", "ML-KEM", "ML-DSA"]
               for lang in ("python", "java")}


def draw(spec_fns, family, rng, matched, tries=60):
    """Families are drawn uniformly, then an API spelling that produces it. Without this, the five
    hash families share a few spec functions and come up a fifth as often as RSA."""
    for _ in range(tries):
        sp = rng.choice(spec_fns)(rng, matched)
        if sp["family"] == family:
            return sp
    return None


STYLES = {"python": ["const", "config", "default", "classattr", "alias"], "java": ["const", "config", "enum", "overload"]}


def mixed_pool(lang):
    """Spec pool for mixed files: every spelling the generator knows in that language."""
    if lang in ("python", "java"):
        return (py_specs() if lang == "python" else java_specs())[2]
    sets = _new_specs(lang)
    return sets["broad"] + sets.get("pqc", [])


def build_mixed_file(lang, rng, names, new_fid, n_sites=None, target_lines=None, allowed=None):
    """One realistic-size file with several crypto sites in ordinary code (see tools/mixed.py).
    -> (text, [(fid, spec, style, anchor_lines)], java_class_or_None)"""
    import mixed
    n_sites = n_sites or rng.randint(3, 5)
    target_lines = target_lines or rng.randint(220, 520)
    chosen = mixed.pick_specs(mixed_pool(lang), rng, draw, n_sites, allowed)
    if lang in ("python", "java"):
        builder = FileBuilder(lang, rng, names, "canonical")
        styles = [rng.choice(["inline", "inline"] + [x for x in STYLES[lang] if x != "alias"]) if sp["slot"] else "inline"
                  for sp in chosen]
    else:
        builder = _new_builder(lang, rng, names, "canonical")
        styles = [rng.choice(["inline", "inline"] + builder.styles_for(sp)) if sp["slot"] else "inline" for sp in chosen]
    sites = []
    for sp, style in zip(chosen, styles):
        fid = new_fid()
        builder.add(sp, style, fid)
        sites.append((fid, sp, style))
    mixed.add_filler(lang, builder, rng, names, {sp["family"] for sp in chosen}, target_lines,
                     lambda: mixed.funcs_lines(builder))
    cls = None
    if lang in ("python", "java"):
        cls = f"{names.cap()}Module" if lang == "java" else None
        text, anchors = builder.render(cls)
    else:
        text, anchors = _lines_to_text(builder.render())
    return text, [(fid, sp, style, sorted(anchors[fid])) for fid, sp, style in sites], cls


def published_families() -> dict:
    """Families in the published corpus per (tier, language), plus per language for Tier 1-2: the matched
    holdout draws only from these, and holdout assets and artifacts feed the gap only where they match."""
    gt = load_json(ROOT / "expected" / "ground_truth.json")
    out = defaultdict(set)
    for f in gt["findings"]:
        if f["tier"] in (1, 2, 3, 4, 5, "pqc", "mixed"):
            if f["tier"] in (1, 2):
                out[f["lang"]].add(f["family"])
            out[(f["tier"], f["lang"])].add(f["family"])
    return out


NEW_LANGS = {"go", "javascript", "typescript", "c", "csharp"}
EXT = {"python": ".py", "java": ".java", "javascript": ".js", "typescript": ".ts", "c": ".c", "csharp": ".cs"}
UNCOVERED = ("TLS-", "TLS_")  # protocol versions and suites set in code: not generated yet


def _lines_to_text(lines):
    text = "\n".join(t for t, _ in lines) + "\n"
    anchors = defaultdict(list)
    for i, (_, fid) in enumerate(lines, 1):
        if fid:
            anchors[fid].append(i)
    return text, anchors


def _new_builder(lang, rng, names, imports):
    import holdout_langs as hl
    if lang == "go":
        return hl.GoBuilder(rng, names, imports)
    if lang in ("javascript", "typescript"):
        return hl.JsBuilder(rng, names, ts=lang == "typescript", imports=imports)
    if lang == "csharp":
        return hl.CsBuilder(rng, names, imports)
    return hl.CBuilder(rng, names, imports)


def _new_specs(lang):
    import holdout_langs as hl
    return {"go": hl.go_specs, "javascript": hl.js_specs, "typescript": hl.js_specs, "c": hl.c_specs,
            "csharp": hl.cs_specs}[lang]()


def _negative_py_java(rng, names, lang, phrases):
    """Several statement shapes per file, drawn at random, so no fixed shape can be filtered away."""
    if lang == "python":
        c, fn, err = names.const(), names.snake(), names.const()
        shapes = rng.sample([f'{c} = "{phrases[0]}"', f'{err} = ["{phrases[1]}", "{phrases[2]}"]',
                             f"# {phrases[3]}", f'NOTICE = {{"status": "{phrases[0]}"}}'], 3)
        body = [f"def {fn}(items):", f'    if not items:', f'        raise ValueError("{phrases[1]}")',
                f'    print(f"{phrases[2]}: {{len(items)}}")', f'    return {{"note": "{phrases[3]}", "count": len(items)}}']
        return "\n".join([f'"""{rng.choice(DOCS).format(w="ops", W="Ops")}"""'] + shapes + ["", ""] + body
                         + ["", "", 'if __name__ == "__main__":', f"    print({fn}([1, 2, 3]))", ""])
    cls = names.cap()
    members = rng.sample([f'    static final String NOTE = "{phrases[0]}";',
                          f'    static final String[] LABELS = {{"{phrases[1]}", "{phrases[2]}"}};',
                          f"    // {phrases[3]}", f'    private static final String STATUS = "{phrases[2]}";'], 3)
    return cls, "\n".join([f"public class {cls} {{"] + members + [
        "    static String describe(int n) {", f'        if (n < 0) throw new IllegalArgumentException("{phrases[1]}");',
        f'        return "{phrases[3]} " + n;', "    }", "    public static void main(String[] args) {",
        f'        System.out.println(describe(3) + " {phrases[0]}");', "    }", "}", ""])


def generate(seed: int, out: Path, n_files: int = 120, n_broad: int = 48, n_t3: int = 10, n_deps: int = 6,
             n_neg: int = 28, n_mixed: int = 12, assets: bool = True) -> dict:
    """Matched files mirror the published Tier 1, Tier 2 and PQC cases per language (Python, Java, Go,
    JavaScript/TypeScript, C); Tier 3 projects mirror the published cross-file kinds; broad files use
    every spelling the generator knows; dependency manifests and negative controls in every language."""
    import holdout_deps
    import holdout_t3
    rng = random.Random(seed)
    out = Path(out)
    if out.exists():
        shutil.rmtree(out)
    findings, also_ok, variants, projects = [], [], {}, []
    pub = published_families()
    counter = 0

    def tag(i):  # file names that don't reveal order or seed
        return hashlib.sha256(f"{seed}:{i}".encode()).hexdigest()[:6]

    def fid_for(lang):
        nonlocal counter
        counter += 1
        return f"H-{lang[:2].upper()}-{counter:03d}"

    def record(fid, sp, tier, lang, rel, lines, alt=None, style="inline", imports="canonical", site=False):
        f = {"id": fid, "tier": tier, "lang": lang, "file": rel, "family": sp["family"], "params": sp["params"],
             "lines": sorted(lines)}
        if site:
            f["site"] = True
        if alt:
            f["alt_files"] = alt
        findings.append(f)
        variants[fid] = {"api": sp["api"], "indirection": style, "imports": imports}
        extra = [x for x in sp["also_ok"] if x != sp["family"]]
        if extra:
            also_ok.append({"file": rel, "families": extra})

    def menu(tier, lang):
        return sorted(f for f in pub.get((tier, lang), set()) if not f.startswith(UNCOVERED))

    # Go programs get unique file names, not main.go. A scanner that de-duplicates on the basename
    # (QCI v0.7 does) loses more findings the more same-named files a scan holds, and a holdout with
    # 150 main.go files against the corpus's 40 would read that as overfitting.
    def write(rel, text):
        p = out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        if rel.endswith(".go"):
            mod = p.parent.parent / "go.mod"
            if not mod.exists():
                mod.write_text(f"module example.com/h{tag(len(rel))}\n\ngo 1.24\n")
        if rel.endswith(".cs"):  # one project per case, as in the published corpus
            import holdout_langs
            (p.parent / f"{p.parent.name}.csproj").write_text(holdout_langs.CSPROJ)

    weights = [("python", 22), ("java", 18), ("go", 20), ("javascript", 20), ("c", 20), ("csharp", 14)]
    pool = [l for l, w in weights for _ in range(w)]
    n_pqc = max(3, round(n_files * 0.08))
    jobs = [("matched", rng.choice(pool)) for _ in range(n_files - n_pqc)]
    jobs += [("pqc", rng.choice(["python", "java", "go"])) for _ in range(n_pqc)]
    jobs += [("broad", rng.choice(pool + ["typescript"] * 10)) for _ in range(n_broad)]

    for i, (kind, lang) in enumerate(jobs):
        names = Names(rng)
        h = tag(i)
        matched = kind in ("matched", "pqc")
        hidden = matched and rng.random() < (0.4 if kind == "pqc" else 0.6)
        if lang == "javascript" and hidden and kind == "matched":
            lang = "typescript"  # the published JavaScript is Tier 1; its Tier 2 is TypeScript
        k = 1 if rng.random() < 0.6 else 2
        if kind == "pqc":
            fams, mflag = ["ML-KEM", "ML-DSA"] if lang != "go" else ["ML-KEM"], 1
        elif matched:
            fams, mflag = menu(2 if hidden else 1, lang), (2 if hidden else 1)
        else:
            fams, mflag = (FAMILY_MENU["python"] + ["DES", "RC4"]), False
        if lang in ("python", "java"):
            t1_fns, t2_fns, everything = py_specs() if lang == "python" else java_specs()
            fns = everything if kind in ("broad", "pqc") else t2_fns if hidden else t1_fns
        else:
            sp_sets = _new_specs(lang)
            fns = sp_sets["broad"] if kind == "broad" else sp_sets["pqc"] if kind == "pqc" else sp_sets["t2" if hidden else "t1"]
        chosen, seen = [], set()
        for target in rng.sample(fams, len(fams)):
            sp = draw(fns, target, rng, mflag) if fns else None
            if sp is None or sp["family"] in seen:
                continue
            seen.add(sp["family"])
            chosen.append(sp)
            if len(chosen) == k:
                break
        if not chosen:
            continue
        if lang in ("python", "java"):
            if matched:
                styles = []
                for sp in chosen:
                    if not hidden or not sp["slot"]:
                        styles.append("inline")
                    elif sp["carries_family"] or sp["family"] == "EC" or lang == "java" or kind == "pqc":
                        styles.append(rng.choice([x for x in STYLES[lang] if x != "alias"]))
                    else:
                        styles.append("alias")
                imports = "alias" if "alias" in styles else "canonical"
            else:
                styles = [rng.choice(["inline"] + [x for x in STYLES[lang] if x != "alias"]) if sp["slot"] else "inline"
                          for sp in chosen]
                imports = "any"
            builder = FileBuilder(lang, rng, names, imports)
        else:
            imports = "canonical" if matched else "any"
            builder = _new_builder(lang, rng, names, imports)
            styles = [rng.choice(builder.styles_for(sp)) if (hidden or not matched) and sp["slot"] and
                      (matched or rng.random() < 0.7) else "inline" for sp in chosen]
        fids = []
        for sp, style in zip(chosen, styles):
            fid = fid_for(lang)
            builder.add(sp, style, fid)
            fids.append((fid, sp, style))
        for _ in range(rng.randint(1, 2)):
            builder.filler()
        tiername = ("holdout-pqc" if kind == "pqc" else "holdout-broad" if kind == "broad"
                    else "holdout-t2" if any(st != "inline" for st in styles) or imports == "alias" else "holdout-t1")
        if lang in ("python", "java"):
            cls = f"H{h.capitalize()}{names.cap()}"
            rel = f"corpus/{tiername}/{lang}/" + (f"h_{h}.py" if lang == "python" else f"{cls}.java")
            text, anchors = builder.render(cls)
        else:
            rel = (f"corpus/{tiername}/go/case_{h}/h_{h}.go" if lang == "go" else
                   f"corpus/{tiername}/csharp/H{h}/H{h}.cs" if lang == "csharp" else f"corpus/{tiername}/{lang}/h_{h}{EXT[lang]}")
            text, anchors = _lines_to_text(builder.render())
        write(rel, text)
        for fid, sp, style in fids:
            if kind == "pqc":
                ftier = "holdout-pqc"
            elif kind == "broad":
                ftier = "holdout-broad"
            else:
                ftier = "holdout-t1" if style == "inline" and imports != "alias" else "holdout-t2"
            record(fid, sp, ftier, lang, rel, anchors[fid], style=style, imports=imports)

    # Tier 3: multi-file projects
    for j in range(n_t3):
        lang = "python" if j % 2 == 0 else "java"
        names = Names(rng)
        pattern = rng.choice(["constant", "wrapper", "registry"])
        t1_fns = (py_specs() if lang == "python" else java_specs())[0]
        fams = menu(3, lang)
        need_slot = pattern != "registry"
        specs = []
        for target in rng.sample(fams, len(fams)):
            sp = draw(t1_fns, target, rng, 1)
            if sp and (sp["slot"] or not need_slot):
                specs.append(sp)
                break
        if not specs:
            continue
        if pattern == "wrapper":  # a second caller, same helper body, its own parameters
            for _ in range(30):
                sp2 = draw(t1_fns, specs[0]["family"], rng, 1)
                if sp2 and sp2["body"] == specs[0]["body"] and sp2["ret"] == specs[0]["ret"] and sp2["slot"]:
                    specs.append(sp2)
                    break
        elif pattern == "registry" and rng.random() < 0.6:
            for target in rng.sample(fams, len(fams)):
                sp2 = draw(t1_fns, target, rng, 1)
                if sp2 and sp2["family"] != specs[0]["family"]:
                    specs.append(sp2)
                    break
        mods = mods_py() if lang == "python" else mods_java()
        base = f"corpus/holdout-t3/{lang}/proj_{tag(5000 + j)}"
        if lang == "python":
            proj, finds = holdout_t3.python_project(rng, names, pattern, specs, mods)
            projects.append({"dir": base, "lang": "python", "run": "main.py"})
        else:
            proj, finds, main_cls = holdout_t3.java_project(rng, names, pattern, specs, mods)
            projects.append({"dir": base, "lang": "java", "main": main_cls})
        texts = {}
        for rel, lines in proj.files.items():
            text, anchors = _lines_to_text(lines)
            texts[rel] = anchors
            write(f"{base}/{rel}", text)
        seen_fam = set()
        for fd in finds:
            sp = fd["spec"]
            key = (fd["file"], sp["family"])
            if key in seen_fam:
                continue
            seen_fam.add(key)
            alt = [{"file": f"{base}/{af}", "lines": sorted(texts[af][at])} for af, at in fd["alt"]]
            record(fid_for(lang), sp, "holdout-t3", lang, f"{base}/{fd['file']}", texts[fd["file"]][fd["tag"]], alt,
                   style=pattern)

    # Mixed files: realistic-size modules, several sites each (tools/mixed.py)
    mixed_langs = ["python", "java", "go", "javascript", "typescript", "c"]
    for j in range(n_mixed):
        lang = mixed_langs[j % len(mixed_langs)] if j < len(mixed_langs) else rng.choice(mixed_langs)
        names = Names(rng)
        h = tag(20_000 + j)
        text, sites, cls = build_mixed_file(lang, rng, names, lambda: fid_for(lang), allowed=set(menu("mixed", lang)) or None)
        if lang == "java":
            rel = f"corpus/holdout-mixed/java/H{h.capitalize()}{cls}.java"
            text = text.replace(f"public class {cls} ", f"public class H{h.capitalize()}{cls} ")
        elif lang == "go":
            rel = f"corpus/holdout-mixed/go/mod_{h}/m_{h}.go"
        else:
            rel = f"corpus/holdout-mixed/{lang}/m_{h}{EXT[lang]}"
        write(rel, text)
        for fid, sp, style, lines in sites:
            record(fid, sp, "holdout-mixed", lang, rel, lines, style=style, site=True)

    # Dependency manifests
    libs = {"schema": "cbom-testbench libraries 1", "libraries": [], "also_ok": [], "decoys": [], "lookalikes": []}
    for j in range(n_deps):
        files, ls, ds, lk = holdout_deps.generate_app(rng, Names(rng), f"corpus/deps/app_{tag(7000 + j)}")
        for rel, text in files.items():
            write(rel, text)
        for n_, e in enumerate(ls):
            libs["libraries"].append({"id": f"HL-{j:02d}-{n_}", **e})
        libs["decoys"] += ds
        libs["lookalikes"] += lk

    # Negative controls in every language, several statement shapes each
    import holdout_langs as hl
    neg_langs = ["python", "java", "go", "javascript", "typescript", "c", "csharp"]
    for j in range(n_neg):
        lang = neg_langs[j % len(neg_langs)]
        names = Names(rng)
        h = tag(10_000 + j)
        phrases = rng.sample(NEG_PHRASES, 4)
        if lang == "python":
            write(f"corpus/negatives/python/hn_{h}.py", _negative_py_java(rng, names, "python", phrases))
        elif lang == "java":
            cls, text = _negative_py_java(rng, names, "java", phrases)
            write(f"corpus/negatives/java/{cls}.java", text)
        elif lang == "go":
            write(f"corpus/negatives/go/neg_{h}/n_{h}.go", hl.negative_go(rng, names, phrases))
        elif lang in ("javascript", "typescript"):
            write(f"corpus/negatives/{lang}/hn_{h}{EXT[lang]}", hl.negative_js(rng, names, phrases, ts=lang == "typescript"))
        elif lang == "csharp":
            write(f"corpus/negatives/csharp/Hn{h}/Hn{h}.cs", hl.negative_cs(rng, names, phrases))
        else:
            write(f"corpus/negatives/c/hn_{h}.c", hl.negative_c(rng, names, phrases))

    # Certificates, keys, keystores, TLS/SSH configs and compiled artifacts (holdout_assets.py). Its own
    # random stream, so adding it didn't change anything generated above for a given seed.
    asset_problems = []
    if assets:
        import holdout_assets
        ha = holdout_assets.generate(out, random.Random(f"{seed}:assets"), tag, fid_for, published=pub)
        findings += ha["findings"]
        also_ok += ha["also_ok"]
        asset_problems = ha["problems"]
    truth = {"schema": "cbom-testbench holdout truth", "generator": GENERATOR_VERSION, "asset_problems": asset_problems, "seed_sha256":
             hashlib.sha256(str(seed).encode()).hexdigest(), "findings": findings, "also_ok": also_ok,
             "decoys": {}, "materials": []}
    (out / "truth.json").write_text(json.dumps(truth, indent=2) + "\n")
    (out / "variants.json").write_text(json.dumps(variants, indent=2) + "\n")
    (out / "projects.json").write_text(json.dumps(projects, indent=2) + "\n")
    (out / "libraries.json").write_text(json.dumps(libs, indent=2) + "\n")
    comps = []
    for f in findings:
        prim = FAMILIES[f["family"]]["primitive"]
        line = f["lines"][0] if f["lines"] else None
        occ = {"location": f["file"]}
        if line:
            occ.update(line=line, additionalContext=(out / f["file"]).read_text().splitlines()[line - 1].strip()[:200])
        comps.append(make_component(f["id"], f["family"], f["params"], [occ],
                                    primitive=prim, functions=functions_for(prim), oid=oid_for(f["family"], f["params"])))
    for e in libs["libraries"]:
        comps.append({"type": "library", "bom-ref": e["id"], "name": e["package"].split(":")[-1], "version": e["version"],
                      **({"group": e["package"].split(":")[0]} if ":" in e["package"] else {}),
                      "evidence": {"occurrences": [{"location": e["file"]}]}})
    (out / "expected.cdx.json").write_text(json.dumps(make_bom(comps, "cbom-testbench holdout reference"), indent=2) + "\n")
    return truth


# ----------------------------------------------------------------------------------------------
# Verification: every generated program must build and run.

def verify(out: Path) -> list[str]:
    from verify_corpus import pq_java
    out = Path(out)
    fails = []
    # Generated code is ours, but this process holds the seed: don't hand it to child processes.
    env = {k: v for k, v in __import__("os").environ.items() if k != "CBOM_HOLDOUT_SEED"}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    projects = load_json(out / "projects.json") if (out / "projects.json").exists() else []
    t3 = [Path(p["dir"]) for p in projects]
    in_t3 = lambda p: any(str(p.relative_to(out)).startswith(str(d) + "/") for d in t3)  # noqa: E731

    def run(cmd, cwd=None, label=""):
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=300, env=env)
        if r.returncode:
            fails.append(f"{label}: {(r.stderr.strip().splitlines() or [str(r.returncode)])[-1][:200]}")
        return r

    for p in sorted((out / "corpus").rglob("*.py")):
        if not in_t3(p):
            run([sys.executable, str(p)], label=str(p.relative_to(out)))
    for proj in projects:
        if proj["lang"] == "python":
            run([sys.executable, "main.py"], cwd=out / proj["dir"], label=proj["dir"])
    javas = [j for j in sorted((out / "corpus").rglob("*.java")) if not in_t3(j)]
    if shutil.which("javac"):
        jrt = pq_java() or "java"
        with tempfile.TemporaryDirectory() as tmp:
            if javas:
                r = run(["javac", "-d", tmp] + [str(j) for j in javas], label="javac (single-file cases)")
                if r.returncode == 0:
                    for j in javas:
                        run([jrt, "-cp", tmp, j.stem], label=str(j.relative_to(out)))
            for proj in projects:
                if proj["lang"] == "java":
                    srcs = [str(x) for x in sorted((out / proj["dir"]).rglob("*.java"))]
                    pdir = Path(tmp) / proj["dir"].replace("/", "_")
                    r = run(["javac", "-d", str(pdir)] + srcs, label=f"javac {proj['dir']}")
                    if r.returncode == 0:
                        run([jrt, "-cp", str(pdir), proj["main"]], label=proj["dir"])
    elif javas or any(p["lang"] == "java" for p in projects):
        fails.append("javac not found: Java variants not verified")
    if shutil.which("go"):
        for mod in sorted(m for m in (out / "corpus").rglob("go.mod") if "deps" not in m.relative_to(out).parts):
            with tempfile.TemporaryDirectory() as tmp:
                r = run(["go", "build", "-o", tmp + "/", "./..."], cwd=mod.parent, label=f"go build {mod.parent.relative_to(out)}")
                if r.returncode == 0:
                    for exe in sorted(Path(tmp).iterdir()):
                        run([str(exe)], label=f"{mod.parent.relative_to(out)}/{exe.name}")
    if shutil.which("node"):
        for p in sorted(x for ext in ("*.js", "*.ts") for x in (out / "corpus").rglob(ext)):
            run(["node", p.name], cwd=p.parent, label=str(p.relative_to(out)))
    projects_cs = sorted((out / "corpus").rglob("*.csproj"))
    if projects_cs and shutil.which("dotnet"):
        with tempfile.TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "nuget.config"   # no package source: the cases use the base class library only
            cfg.write_text('<?xml version="1.0"?>\n<configuration><packageSources><clear/></packageSources></configuration>\n')
            denv = dict(env, DOTNET_CLI_TELEMETRY_OPTOUT="1", DOTNET_NOLOGO="1")
            for proj in projects_cs:
                name = proj.stem
                r = subprocess.run(["dotnet", "build", str(proj.parent), "--configfile", str(cfg), "--artifacts-path", f"{tmp}/{name}",
                                    "-p:UseAppHost=false", "-v", "q"], capture_output=True, text=True, timeout=300, env=denv)
                if r.returncode:
                    errs = [ln for ln in r.stdout.splitlines() if " error " in ln]
                    fails.append(f"dotnet build {proj.parent.relative_to(out)}: {(errs or [str(r.returncode)])[0][-220:]}")
                    continue
                r = subprocess.run(["dotnet", f"{tmp}/{name}/bin/{name}/debug/{name}.dll"], capture_output=True, text=True, timeout=120, env=denv)
                if r.returncode:
                    fails.append(f"{proj.parent.relative_to(out)}: {(r.stderr.strip().splitlines() or [str(r.returncode)])[-1][:200]}")
    elif projects_cs:
        fails.append("dotnet not found: C# variants not verified")
    cc = shutil.which("cc") or shutil.which("gcc")
    if cc:
        with tempfile.TemporaryDirectory() as tmp:
            for p in sorted((out / "corpus").rglob("*.c")):
                exe = str(Path(tmp) / p.stem)
                r = run([cc, "-Wall", "-Werror", str(p), "-o", exe, "-lssl", "-lcrypto"], label=f"cc {p.relative_to(out)}")
                if r.returncode == 0:
                    run([exe], label=str(p.relative_to(out)))
    import holdout_assets
    truth = load_json(out / "truth.json")
    fails += truth.get("asset_problems") or []
    fails += holdout_assets.verify(out, truth["findings"])
    return fails


# ----------------------------------------------------------------------------------------------
# Scoring and the overfit gap

def score_holdout(bom: dict, out: Path, policy: str = "nist", scope: dict | None = None) -> dict:
    from score import score
    truth = load_json(out / "truth.json")
    return score(bom, policy=policy, custom="exclude", scope=scope, truth=truth, corpus=out / "corpus")


HOLDOUT_TIERS = {"holdout-t1": 1, "holdout-t2": 2, "holdout-t3": 3, "holdout-t4": 4, "holdout-t5": 5,
                 "holdout-pqc": "pqc", "holdout-mixed": "mixed"}


def _cells(results, tier_map):
    out = defaultdict(list)
    for r in results:
        t = tier_map.get(r["tier"])
        if t:
            out[(t, r["lang"], r["family"])].append(1 if r["detected"] else 0)
    return out


def overfit_gap(published: dict, holdout: dict, boot: int = 2000, seed: int = 0) -> dict:
    """Published Tier 1-2 recall vs matched-holdout recall, compared cell by cell.

    A cell is (tier, language, family). Only cells present on both sides count, and each is weighted
    by its holdout size, so the two numbers describe the same mix of tiers, languages and families.
    The 95% interval draws each cell's rate from its Beta posterior on both sides. The published side
    has 1-5 cases per cell, so it contributes most of the width: a single published case is weak
    evidence, and the interval says so rather than treating 1/1 as certain."""
    # hand-written cases plus the generated calibration cases (build_calibration.py) in the same cells
    pub = _cells(published["results"] + published.get("calibration_results", []), {t: t for t in HOLDOUT_TIERS.values()})
    hold = _cells(holdout["results"], HOLDOUT_TIERS)
    common = sorted((c for c in hold if c in pub), key=str)
    if not common:
        return {"comparable_findings": 0, "gap": None}

    def gap_of(pub_c, hold_c):
        n = sum(len(hold_c[c]) for c in common)
        p = sum(len(hold_c[c]) / n * sum(pub_c[c]) / len(pub_c[c]) for c in common)
        h = sum(sum(hold_c[c]) for c in common) / n
        return 100 * p, 100 * h

    p, h = gap_of(pub, hold)
    rng = random.Random(seed)
    n_hold = sum(len(hold[c]) for c in common)
    gaps = []
    for _ in range(boot):  # each cell's true rate drawn from its Beta posterior (Jeffreys prior), both sides
        g = 0.0
        for c in common:
            pr = rng.betavariate(sum(pub[c]) + 0.5, len(pub[c]) - sum(pub[c]) + 0.5)
            hr = rng.betavariate(sum(hold[c]) + 0.5, len(hold[c]) - sum(hold[c]) + 0.5)
            g += len(hold[c]) / n_hold * (pr - hr)
        gaps.append(100 * g)
    # The prior pulls 1/1 and 0/n cells toward 50%, which shifts the draws toward zero. Keep their spread,
    # centered on the observed gap, so the interval contains the number it describes.
    center = sum(gaps) / len(gaps)
    gaps = sorted((g - center) + (p - h) for g in gaps)
    lo, hi = max(-100.0, gaps[int(0.025 * boot)]), min(100.0, gaps[int(0.975 * boot) - 1])
    fam = defaultdict(lambda: [0, 0, 0, 0])
    for (t, lang, f) in common:
        fam[f][0] += sum(pub[(t, lang, f)]); fam[f][1] += len(pub[(t, lang, f)])
        fam[f][2] += sum(hold[(t, lang, f)]); fam[f][3] += len(hold[(t, lang, f)])
    fam_rows = [{"family": f, "published": round(100 * v[0] / v[1], 1), "published_n": v[1],
                 "holdout": round(100 * v[2] / v[3], 1), "holdout_n": v[3],
                 "gap": round(100 * v[0] / v[1] - 100 * v[2] / v[3], 1)} for f, v in sorted(fam.items())]
    by_tier = {}
    for t in HOLDOUT_TIERS.values():
        cs = [c for c in common if c[0] == t]
        if cs:
            n = sum(len(hold[c]) for c in cs)
            by_tier[f"tier{t}"] = {"published": round(100 * sum(len(hold[c]) / n * sum(pub[c]) / len(pub[c]) for c in cs), 1),
                                   "holdout": round(100 * sum(sum(hold[c]) for c in cs) / n, 1), "holdout_n": n}
    return {"comparable_findings": sum(len(hold[c]) for c in common), "cells": len(common),
            "families": len({c[2] for c in common}),
            "published_matched": round(p, 1), "holdout": round(h, 1), "gap": round(p - h, 1),
            "gap_ci95": [round(lo, 1), round(hi, 1)], "significant": lo > 0,
            "by_tier": by_tier, "by_family": fam_rows}


NEG_LANGS = ("python", "java", "go", "javascript", "typescript", "c", "csharp")
CODE_EXT = {".py", ".java", ".go", ".js", ".mjs", ".ts", ".c", ".cs"}


def negative_gap(published: dict, holdout: dict, holdout_dir: Path, langs=NEG_LANGS) -> dict:
    """False positives per negative-control file: published negatives vs freshly generated ones.

    The recall gap can't see a scanner that has been tuned until the published negatives are clean.
    This can: the holdout negatives say the same kind of thing (algorithm names in log lines, string
    constants and returned values, post-quantum claims) in files the scanner has never seen. Only the
    languages the generator covers are compared."""
    def files(root: Path):
        return [p for lang in langs for p in (root / "corpus" / "negatives" / lang).rglob("*")
                if p.is_file() and p.suffix in CODE_EXT]
    pub_files = files(ROOT)
    hold_files = files(Path(holdout_dir))
    in_langs = lambda x: x["negative_control"] and x["file"].split("/")[2] in langs  # noqa: E731
    pub_fp = [x for x in published["false_positives"] if in_langs(x)]
    hold_fp = [x for x in holdout["false_positives"] if in_langs(x)]
    pq = lambda fps: sum(1 for x in fps if FAMILIES.get(x["family"], {}).get("pq"))  # noqa: E731
    pr = len(pub_fp) / len(pub_files) if pub_files else None
    hr = len(hold_fp) / len(hold_files) if hold_files else None
    return {"published_files": len(pub_files), "published_fps": len(pub_fp), "published_pqc_overclaims": pq(pub_fp),
            "holdout_files": len(hold_files), "holdout_fps": len(hold_fp), "holdout_pqc_overclaims": pq(hold_fp),
            "published_per_file": round(pr, 2) if pr is not None else None,
            "holdout_per_file": round(hr, 2) if hr is not None else None,
            "gap_per_file": round(hr - pr, 2) if pr is not None and hr is not None else None}


def library_gap(published_lib: dict | None, bom: dict, holdout_dir: Path) -> dict | None:
    """Crypto libraries found in the right manifest: published manifests vs generated ones, per ecosystem."""
    import libraries as libs
    path = Path(holdout_dir) / "libraries.json"
    if not published_lib or not path.exists():
        return None
    hold = libs.score_libraries(bom, json.loads(path.read_text()))
    rows = {}
    for side, rep in (("published", published_lib), ("holdout", hold)):
        for r in rep["results"]:
            if r["scope"] != "direct":
                continue
            row = rows.setdefault(r["ecosystem"], {"published": [0, 0], "holdout": [0, 0]})
            row[side][0] += r["found_in_manifest"]
            row[side][1] += 1
    pct = lambda a: round(100 * a[0] / a[1], 1) if a[1] else None  # noqa: E731
    common = [e for e, v in rows.items() if v["published"][1] and v["holdout"][1]]
    n = sum(rows[e]["holdout"][1] for e in common)
    p = sum(rows[e]["holdout"][1] / n * rows[e]["published"][0] / rows[e]["published"][1] for e in common) if n else None
    h = sum(rows[e]["holdout"][0] for e in common) / n if n else None
    return {"by_ecosystem": {e: {"published": pct(v["published"]), "published_n": v["published"][1],
                                 "holdout": pct(v["holdout"]), "holdout_n": v["holdout"][1]} for e, v in sorted(rows.items())},
            "published_matched": round(100 * p, 1) if p is not None else None, "holdout": round(100 * h, 1) if h is not None else None,
            "gap": round(100 * (p - h), 1) if n else None, "holdout_false_positives": len(hold["false_positives"]),
            "holdout_version_accuracy": hold["version_accuracy"]}


def library_markdown(g: dict | None) -> str:
    if not g or g.get("gap") is None:
        return ""
    out = ["", "### Crypto libraries, published vs generated manifests", "",
           f"Direct dependencies found in the right manifest: published {g['published_matched']}% (weighted to the holdout's "
           f"ecosystem mix), holdout {g['holdout']}%, gap **{g['gap']:+} points**. Holdout versions correct: "
           f"{g['holdout_version_accuracy']}%; false positives: {g['holdout_false_positives']}.", "",
           "| Ecosystem | Published | Holdout |", "|---|---|---|"]
    for e, v in g["by_ecosystem"].items():
        out.append(f"| {e} | {v['published']}% (n={v['published_n']}) | {v['holdout']}% (n={v['holdout_n']}) |")
    return "\n".join(out) + "\n"


def negative_markdown(n: dict) -> str:
    if n.get("gap_per_file") is None:
        return ""
    verdict = ("Unseen negatives fare markedly worse: false-positive suppression was fitted to the published files."
               if n["gap_per_file"] > NEG_GAP_LIMIT else "Within the expected range.")
    return "\n".join(["", "### Negative controls, published vs unseen", "",
                      "| | Files | False positives | per file | PQC over-claims |", "|---|---|---|---|---|",
                      f"| Published | {n['published_files']} | {n['published_fps']} | {n['published_per_file']} | {n['published_pqc_overclaims']} |",
                      f"| Holdout | {n['holdout_files']} | {n['holdout_fps']} | {n['holdout_per_file']} | {n['holdout_pqc_overclaims']} |",
                      "", f"Gap: **{n['gap_per_file']:+} false positives per file**. {verdict}", ""])


# Calibrated (24 negatives, six languages, five seeds): grep -0.01 to +0.24 and QCI 0.3.0 -0.27 to +0.15, neither
# tuned to the corpus; v0.7, whose filters match the published negatives' shapes, +0.72 to +1.18.

NEG_GAP_LIMIT = 0.5


def gap_markdown(g: dict, holdout: dict) -> str:
    s = holdout["summary"]
    out = ["## Holdout and overfit gap", ""]
    if not g.get("gap") and g.get("gap") != 0:
        return "\n".join(out + ["No comparable findings.", ""])
    out += [f"Holdout recall **{g['holdout']}%** on {g['comparable_findings']} findings across {g['families']} "
            f"families ({g['cells']} tier/language/family cells). The published cases in the same cells (hand-written plus calibration), "
            f"weighted the same way: **{g['published_matched']}%**.",
            "", f"Overfit gap: **{g['gap']:+} points** (95% interval {g['gap_ci95'][0]:+} to {g['gap_ci95'][1]:+}). "
            + ("The published score overstates this scanner on unseen code." if g["significant"] else
               "Within sampling noise: the published score generalizes."), "",
            "| | Published | Holdout | Holdout n |", "|---|---|---|---|"]
    for k, v in g["by_tier"].items():
        out.append(f"| {k.replace('tier', 'Tier ')} | {v['published']}% | {v['holdout']}% | {v['holdout_n']} |")
    out += ["", f"Holdout false positives: {s['all/all']['false_positives']} "
            f"({s['negatives']['false_positives']} in negative controls), PQC over-claims: {s['pqc_overclaims']['count']}.",
            "", "| Family | Published | Holdout | Gap |", "|---|---|---|---|"]
    for r in sorted(g["by_family"], key=lambda r: -r["gap"]):
        out.append(f"| {r['family']} | {r['published']}% (n={r['published_n']}) | {r['holdout']}% (n={r['holdout_n']}) | {r['gap']:+} |")
    broad = [r for r in holdout["results"] if r["tier"] == "holdout-broad"]
    if broad:
        bd = sum(r["detected"] for r in broad)
        out += ["", f"**Broad set:** {bd}/{len(broad)} ({round(100 * bd / len(broad), 1)}%) on API spellings, import "
                "styles and indirections the published corpus doesn't use. This measures coverage beyond the corpus; "
                "it isn't compared with anything."]
    un = sorted({r["family"] for r in holdout["results"] if r["family"].startswith(UNCOVERED)})
    out += ["", "Not generated yet, so outside the comparison: TLS protocol versions and cipher suites configured in code."]
    out += ["", "Per-family rows are small samples; read the overall gap and its interval first. Holdout files and "
            "per-finding results stay with whoever holds the seed.", ""]
    return "\n".join(out)


# ----------------------------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    g = sp.add_parser("generate", help="write a holdout set: corpus/, truth.json, expected.cdx.json")
    g.add_argument("--seed", type=int, help="keep it private; omitted = random, printed once")
    g.add_argument("--out", type=Path, required=True)
    g.add_argument("--files", type=int, default=120, help="matched files (default 120, as the runner uses)")
    g.add_argument("--negatives", type=int, default=28, help="negative-control files across seven languages (default 28)")
    g.add_argument("--broad", type=int, default=48, help="broad files (default 48)")
    g.add_argument("--no-verify", action="store_true")
    s = sp.add_parser("score", help="score a scanner's CBOM of <dir>/corpus, with the overfit gap")
    s.add_argument("cbom", type=Path)
    s.add_argument("--dir", type=Path, required=True)
    s.add_argument("--published", type=Path, help="the same scanner's published-corpus scorecard JSON (score.py output)")
    s.add_argument("--policy", default="nist")
    s.add_argument("--scope", type=Path)
    s.add_argument("--out", type=Path, help="report prefix (default <dir>/holdout-score)")
    a = ap.parse_args()

    if a.cmd == "generate":
        seed = a.seed if a.seed is not None else secrets.randbits(48)
        if a.seed is None:
            print(f"Seed: {seed}   (keep it private; needed to regenerate this exact set)")
        truth = generate(seed, a.out, a.files, a.broad, n_neg=a.negatives)
        by = defaultdict(int)
        for f in truth["findings"]:
            by[(f["tier"], f["lang"])] += 1
        print(f"Wrote {len(truth['findings'])} findings in {a.out}/corpus: "
              + ", ".join(f"{t} {l} {n}" for (t, l), n in sorted(by.items())))
        if not a.no_verify:
            fails = verify(a.out)
            if fails:
                print("Generated files that don't run:\n  " + "\n  ".join(fails))
                return 1
            print("Every generated file runs.")
        return 0

    from score import load_scope, to_markdown
    bom = load_json(a.cbom)
    rep = score_holdout(bom, a.dir, a.policy, load_scope(a.scope))
    prefix = a.out or a.dir / "holdout-score"
    md = to_markdown(f"{a.cbom.name} on holdout", rep)
    result = {"holdout": rep}
    if a.published:
        gap = overfit_gap(load_json(a.published), rep)
        result["overfit_gap"] = gap
        md += "\n" + gap_markdown(gap, rep)
        broad = [r for r in rep["results"] if r["tier"] == "holdout-broad"]
        bpct = round(100 * sum(r["detected"] for r in broad) / len(broad), 1) if broad else None
        pub_rep = load_json(a.published)
        neg = negative_gap(pub_rep, rep, a.dir)
        lib = library_gap(pub_rep.get("libraries"), bom, a.dir)
        result.update(negative_gap=neg, library_gap=lib)
        md += negative_markdown(neg) + library_markdown(lib)
        print(f"Matched holdout {gap['holdout']}%, published (same family mix) {gap['published_matched']}%, "
              f"gap {gap['gap']:+} [{gap['gap_ci95'][0]:+}, {gap['gap_ci95'][1]:+}]; broad {bpct}%; "
              f"negatives {neg['published_per_file']}->{neg['holdout_per_file']} per file (gap {neg['gap_per_file']:+}); "
              f"libraries " + (f"{lib['published_matched']}%->{lib['holdout']}% (gap {lib['gap']:+})" if lib and lib['gap'] is not None else "n/a"))
    else:
        print(f"Holdout recall {rep['summary']['all/all']['recall']}%")
    Path(f"{prefix}.md").write_text(md)
    Path(f"{prefix}.json").write_text(json.dumps(result, indent=2, default=str) + "\n")
    print(f"Wrote {prefix}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
