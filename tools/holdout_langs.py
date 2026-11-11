"""Holdout generation for Go, JavaScript/TypeScript and C (imported by holdout.py).

Same contract as the Python/Java generator: a spec returns one finding's code with placeholders
(<<S>> the slot indirection may hoist, <<d>> input bytes, <<x1>>.. locals, <<module>> refs); lines
starting with "@" are anchors. Matched specs reproduce the spellings and values the published
Tier 1/2/PQC cases use per language; broad specs add the rest.

Each language has its own builder because the rules differ: Go rejects unused variables and imports
and needs one program per directory; C compiles with -Wall -Werror; TypeScript has to survive Node's
type stripping (no enums, no namespaces).
"""
from __future__ import annotations

import re

from holdout_common import WORDS, Names, spec, sub

# =============================================================================================
# Go
# =============================================================================================
GO_PKGS = {"md5": "crypto/md5", "sha1": "crypto/sha1", "sha256": "crypto/sha256", "sha512": "crypto/sha512",
           "sha3": "crypto/sha3", "aes": "crypto/aes", "cipher": "crypto/cipher", "des": "crypto/des",
           "rc4": "crypto/rc4", "rsa": "crypto/rsa", "rand": "crypto/rand", "ecdsa": "crypto/ecdsa",
           "elliptic": "crypto/elliptic", "ed25519": "crypto/ed25519", "ecdh": "crypto/ecdh", "dsa": "crypto/dsa",
           "hmac": "crypto/hmac", "pbkdf2": "crypto/pbkdf2", "mlkem": "crypto/mlkem", "crypto": "crypto",
           "hash": "hash"}
GO_SUM = {"MD5": ("md5", "Sum", "[16]byte"), "SHA-1": ("sha1", "Sum", "[20]byte"),
          "SHA-256": ("sha256", "Sum256", "[32]byte"), "SHA3-256": ("sha3", "Sum256", "[32]byte"),
          "SHA-512": ("sha512", "Sum512", "[64]byte")}
GO_NEW = {"MD5": "md5", "SHA-1": "sha1", "SHA-256": "sha256", "SHA-512": "sha512"}
GO_HASH_ENUM = {"SHA-1": ("SHA1", "crypto/sha1"), "SHA-256": ("SHA256", "crypto/sha256"),
                "SHA-512": ("SHA512", "crypto/sha512"), "MD5": ("MD5", "crypto/md5")}
MUST = ["must(err)"]


def go_specs():
    def go_sum(r, m=False):
        fam = r.choice(["MD5", "SHA-1", "SHA-256", "SHA3-256"] + ([] if m else ["SHA-512"]))
        mod, fn, typ = GO_SUM[fam]
        return spec(fam, {}, ["@<<x1>> := <<S>>(<<d>>)"], "<<x1>>", f"<<{mod}>>.{fn}", "expr",
                    api=f"{mod}.{fn}", carries_family=True, gotype=f"func([]byte) {typ}")

    def go_hash_enum(r, m=False):
        fam = "SHA-1" if m else r.choice(list(GO_HASH_ENUM))
        name, pkg = GO_HASH_ENUM[fam]
        return spec(fam, {}, ["@<<x1>> := <<S>>.New()", "<<x1>>.Write(<<d>>)"], "<<x1>>.Sum(nil)", f"<<crypto>>.{name}",
                    "expr", api="crypto.Hash", carries_family=True, gotype="<<crypto>>.Hash", blank=[pkg])

    def go_aes(r, m=False):
        mode = r.choice({1: ["CBC", "GCM"], 2: ["CTR"]}.get(m, ["CBC", "GCM", "CTR"]))
        nb = r.choice([16, 24, 32])
        body = ["@<<x2>> := make([]byte, <<S>>)", "@<<x3>>, err := <<aes>>.NewCipher(<<x2>>)"] + MUST
        if mode == "GCM":
            body += ["@<<x1>>, err := <<cipher>>.NewGCM(<<x3>>)"] + MUST
            ret = "<<x1>>.Seal(nil, make([]byte, <<x1>>.NonceSize()), <<d>>, nil)"
        else:
            body += ["<<x1>> := make([]byte, 32)",
                     "@<<cipher>>." + ("NewCBCEncrypter" if mode == "CBC" else "NewCTR") + "(<<x3>>, make([]byte, 16))."
                     + ("CryptBlocks" if mode == "CBC" else "XORKeyStream") + "(<<x1>>, <<d32>>)"]
            ret = "<<x1>>"
        return spec("AES", {"key_size": nb * 8, "mode": mode}, body, ret, str(nb), "int", api=f"aes.NewCipher {mode}")

    def go_3des(r, m=False):
        body = ["<<x2>> := make([]byte, 24)", "@<<x3>>, err := <<S>>(<<x2>>)"] + MUST + [
            "<<x1>> := make([]byte, 16)", "@<<cipher>>.NewCBCEncrypter(<<x3>>, make([]byte, 8)).CryptBlocks(<<x1>>, <<d16>>)"]
        return spec("3DES", {"mode": "CBC"}, body, "<<x1>>", "<<des>>.NewTripleDESCipher", "expr",
                    api="des.NewTripleDESCipher", carries_family=True, gotype="func([]byte) (<<cipher>>.Block, error)")

    def go_des(r, m=False):
        body = ["@<<x3>>, err := <<des>>.NewCipher(make([]byte, 8))"] + MUST + [
            "<<x1>> := make([]byte, 16)", "@<<cipher>>.NewCBCEncrypter(<<x3>>, make([]byte, 8)).CryptBlocks(<<x1>>, <<d16>>)"]
        return spec("DES", {"mode": "CBC"}, body, "<<x1>>", api="des.NewCipher")

    def go_rc4(r, m=False):
        body = ['@<<x1>>, err := <<rc4>>.NewCipher([]byte("partner-key-<<w>>"))'] + MUST + [
            "<<x2>> := make([]byte, 8)", '<<x1>>.XORKeyStream(<<x2>>, []byte("payload8"))']
        return spec("RC4", {}, body, "<<x2>>", api="rc4.NewCipher")

    def go_rsa(r, m=False):
        bits = r.choice([1024, 2048])
        return spec("RSA", {"key_size": bits}, ["@<<x1>>, err := <<rsa>>.GenerateKey(<<rand>>.Reader, <<S>>)"] + MUST,
                    "<<x1>>.N.BitLen()", str(bits), "int", api="rsa.GenerateKey")

    def go_ecdsa(r, m=False):
        curve, fn = r.choice([("P-256", "P256"), ("P-384", "P384"), ("P-521", "P521")])
        return spec("EC", {"curve": curve}, ["@<<x1>>, err := <<ecdsa>>.GenerateKey(<<S>>(), <<rand>>.Reader)"] + MUST,
                    "<<x1>>.Curve.Params().BitSize", f"<<elliptic>>.{fn}", "expr", api="ecdsa.GenerateKey",
                    gotype="func() <<elliptic>>.Curve")

    def go_ed25519(r, m=False):
        return spec("Ed25519", {}, ["@_, <<x1>>, err := <<ed25519>>.GenerateKey(<<rand>>.Reader)"] + MUST,
                    "<<ed25519>>.Sign(<<x1>>, <<d>>)", api="ed25519.GenerateKey")

    def go_x25519(r, m=False):
        return spec("X25519", {}, ["@<<x2>> := <<S>>()", "<<x1>>, err := <<x2>>.GenerateKey(<<rand>>.Reader)"] + MUST,
                    "<<x1>>.PublicKey().Bytes()", "<<ecdh>>.X25519", "expr", api="ecdh.X25519", carries_family=True,
                    gotype="func() <<ecdh>>.Curve")

    def go_dsa(r, m=False):
        size, ps = r.choice([(1024, "L1024N160"), (1024, "L1024N160"), (2048, "L2048N256")])
        return spec("DSA", {"key_size": size}, ["var <<x1>> <<dsa>>.Parameters",
                                                f"@must(<<dsa>>.GenerateParameters(&<<x1>>, <<rand>>.Reader, <<dsa>>.{ps}))"],
                    "<<x1>>.P.BitLen()", api="dsa.GenerateParameters")

    def go_hmac(r, m=False):
        fam = {1: "SHA-256", 2: "MD5"}.get(m) or r.choice(list(GO_NEW))
        return spec("HMAC", {"hash": fam}, ['@<<x1>> := <<hmac>>.New(<<S>>, []byte("svc-<<w>>"))', "<<x1>>.Write(<<d>>)"],
                    "<<x1>>.Sum(nil)", f"<<{GO_NEW[fam]}>>.New", "expr", also_ok=[fam], api="hmac.New",
                    gotype="func() <<hash>>.Hash")

    def go_pbkdf2(r, m=False):
        fam = "SHA-512" if m else r.choice(["SHA-1", "SHA-256", "SHA-512"])
        return spec("PBKDF2", {"hash": fam}, ['@<<x1>>, err := <<pbkdf2>>.Key(<<S>>, "pw-<<w>>", []byte("salt"), 1000, 32)'] + MUST,
                    "<<x1>>", f"<<{GO_NEW[fam]}>>.New", "expr", also_ok=[fam, "HMAC"], api="pbkdf2.Key",
                    gotype="func() <<hash>>.Hash")

    def go_mlkem(r, m=False):
        # the published Go case calls GenerateKey1024; the other sizes belong to the broad set
        ps = "1024" if m else r.choice(["768", "1024"])
        return spec("ML-KEM", {"param_set": ps}, ["@<<x1>>, err := <<S>>()"] + MUST, "<<x1>>.EncapsulationKey().Bytes()",
                    f"<<mlkem>>.GenerateKey{ps}", "expr", api="mlkem.GenerateKey", carries_family=True)

    t1 = [go_sum, go_aes, go_des, go_rc4, go_rsa, go_ecdsa, go_ed25519, go_x25519, go_dsa, go_hmac, go_pbkdf2, go_3des]
    t2 = [go_hash_enum, go_rsa, go_ecdsa, go_hmac, go_aes, go_3des]
    pqc = [go_mlkem]
    broad = [go_sum, go_hash_enum, go_aes, go_3des, go_des, go_rc4, go_rsa, go_ecdsa, go_ed25519, go_x25519,
             go_hmac, go_pbkdf2, go_mlkem]
    return {"t1": t1, "t2": t2, "pqc": pqc, "broad": broad}


class GoBuilder:
    STYLES = ["const", "var", "map", "struct", "arg"]

    def __init__(self, rng, names, imports="canonical"):
        self.rng, self.names, self.mode = rng, names, imports
        self.imports, self.refs = {}, {}  # path -> alias ("" for none, "_" for blank)
        self.top, self.funcs, self.mains = [], [], []

    def ref(self, mod):
        if mod not in self.refs:
            path = GO_PKGS[mod]
            alias = ""
            if self.mode != "canonical" and mod not in ("crypto", "hash") and self.rng.random() < 0.5:
                alias = self.names.alias().strip("_").lower() + "x"
            self.imports[path] = alias
            self.refs[mod] = alias or path.split("/")[-1]
        return self.refs[mod]

    def styles_for(self, sp):
        ok = []
        for st in self.STYLES:
            if st == "const" and sp["kind"] not in ("str", "int"):
                continue
            if st in ("map", "struct", "arg") and sp["kind"] == "expr" and not sp.get("gotype"):
                continue
            ok.append(st)
        return ok

    def add(self, sp, style, fid):
        nm, rng = self.names, self.rng
        texts = sp["body"] + [sp["ret"], sp["slot"] or "", sp.get("gotype") or ""]
        m = {}
        for t in texts:
            for name in re.findall(r"<<(\w+)>>", t):
                if name not in m and name in GO_PKGS:
                    if name == "hash" and style not in ("map", "struct", "arg"):
                        continue
                    m[name] = self.ref(name)
        for pkg in sp.get("blank", []):
            if pkg not in self.imports:
                self.imports[pkg] = "_"
        m.update({f"x{i}": nm.var() for i in range(1, 6)}, w=rng.choice(WORDS),
                 d=f'[]byte("{rng.choice(WORDS)}-{rng.randint(100, 999)}")',
                 d16='[]byte("0123456789abcdef")', d32='[]byte("0123456789abcdef0123456789abcdef")')
        slot = sub(sp["slot"], m) if sp["slot"] else None
        typed = style in ("map", "struct", "arg")
        typ = ({"str": "string", "int": "int"}.get(sp["kind"]) or (sub(sp["gotype"], m) if sp.get("gotype") else None)) if typed else None
        fn = nm.camel()
        params, args = "", ""
        if style == "inline":
            m["S"] = slot
        elif style == "const":
            c = nm.camel()
            self.top.append((f"const {c} = {slot}", fid))
            m["S"] = c
        elif style == "var":
            c = nm.camel()
            self.top.append((f"var {c} = {slot}", fid))
            m["S"] = c
        elif style == "map":
            c, k = nm.camel(), nm.key()
            self.top += [(f"var {c} = map[string]{typ}{{", None), (f'\t"{k}": {slot},', fid), ("}", None)]
            m["S"] = f'{c}["{k}"]'
        elif style == "struct":
            c, f = nm.camel(), nm.cap()
            self.top.append((f"var {c} = struct{{ {f} {typ} }}{{{f}: {slot}}}", fid))
            m["S"] = f"{c}.{f}"
        elif style == "arg":
            p = nm.camel()
            params, args = f"{p} {typ}", slot
            m["S"] = p
        body = [(f"func {fn}({params}) any {{", None)]
        for line in sp["body"]:
            body.append(("\t" + sub(line.lstrip("@"), m), fid if line.startswith("@") else None))
        body += [("\treturn " + sub(sp["ret"], m), None), ("}", None), ("", None)]
        self.funcs.append(body)
        self.mains.append((f"\tfmt.Println(len(fmt.Sprint({fn}({args}))))", fid if style == "arg" else None))

    def filler(self):
        f = self.names.camel()
        n = self.rng.randint(2, 9)
        self.funcs.append([(f"func {f}(xs []int) int {{", None), ("\tt := 0", None), ("\tfor _, x := range xs {", None),
                           ("\t\tt += x", None), ("\t}", None), (f"\treturn t % {n}", None), ("}", None), ("", None)])

    def render(self):
        self.rng.shuffle(self.funcs)
        self.imports.setdefault("fmt", "")
        lines = [(f"// {self.rng.choice(['Batch worker', 'Service helpers', 'Sync task', 'Export job'])} for "
                  f"{self.rng.choice(WORDS)} records.", None), ("package main", None), ("", None), ("import (", None)]
        for path, alias in sorted(self.imports.items()):
            lines.append((f'\t{alias + " " if alias else ""}"{path}"', None))
        lines += [(")", None), ("", None)] + self.top + ([("", None)] if self.top else [])
        lines += [("func must(err error) {", None), ("\tif err != nil {", None), ("\t\tpanic(err)", None), ("\t}", None),
                  ("}", None), ("", None)]
        for f in self.funcs:
            lines += f
        lines += [("func main() {", None)] + self.mains + [("}", None)]
        return lines


# =============================================================================================
# JavaScript / TypeScript (Node)
# =============================================================================================
JS_HASH = {"MD5": "md5", "SHA-1": "sha1", "SHA-256": "sha256", "SHA3-256": "sha3-256", "SHA-512": "sha512"}
JS_CIPHERS = {  # name -> (family, params, key bytes, iv bytes or None, extra options)
    "aes-128-cbc": ("AES", {"key_size": 128, "mode": "CBC"}, 16, 16, ""),
    "aes-192-cbc": ("AES", {"key_size": 192, "mode": "CBC"}, 24, 16, ""),
    "aes-256-gcm": ("AES", {"key_size": 256, "mode": "GCM"}, 32, 12, ""),
    "aes-128-gcm": ("AES", {"key_size": 128, "mode": "GCM"}, 16, 12, ""),
    "aes-128-ecb": ("AES", {"key_size": 128, "mode": "ECB"}, 16, None, ""),
    "aes-256-ctr": ("AES", {"key_size": 256, "mode": "CTR"}, 32, 16, ""),
    "des-ede3-cbc": ("3DES", {"mode": "CBC"}, 24, 8, ""),
    "chacha20-poly1305": ("ChaCha20-Poly1305", {}, 32, 12, ", { authTagLength: 16 }"),
}


def js_specs():
    def js_hash(r, m=False):
        fam = {2: "SHA-1"}.get(m) or r.choice(["MD5", "SHA-1", "SHA-256", "SHA3-256"] + ([] if m else ["SHA-512"]))
        return spec(fam, {}, ["@const <<x1>> = <<createHash>>(<<S>>).update(<<d>>).digest(\"hex\");"], "<<x1>>",
                    f'"{JS_HASH[fam]}"', "str", api="createHash", carries_family=True)

    def js_cipher(r, m=False):
        name = r.choice({1: ["aes-128-cbc", "aes-256-gcm", "des-ede3-cbc", "chacha20-poly1305"],
                         2: ["des-ede3-cbc", "aes-128-ecb", "aes-256-gcm"]}.get(m, list(JS_CIPHERS)))
        fam, params, kl, iv, opt = JS_CIPHERS[name]
        ivx = f"<<randomBytes>>({iv})" if iv else "null"
        return spec(fam, params, [f"@const <<x1>> = <<createCipheriv>>(<<S>>, <<randomBytes>>({kl}), {ivx}{opt});"],
                    "Buffer.concat([<<x1>>.update(<<d>>), <<x1>>.final()])", f'"{name}"', "str", api="createCipheriv",
                    carries_family=True)

    def js_rsa(r, m=False):
        bits = r.choice([1024, 2048])
        return spec("RSA", {"key_size": bits}, ['@const { privateKey: <<x1>> } = <<generateKeyPairSync>>("rsa", { modulusLength: <<S>> });'],
                    '<<sign>>("sha256", Buffer.from(<<d>>), <<x1>>)', str(bits), "int", also_ok=["SHA-256"],
                    api="generateKeyPairSync rsa")

    def js_ec(r, m=False):
        curve, name = r.choice([("P-256", "prime256v1"), ("P-384", "secp384r1"), ("P-521", "secp521r1")])
        return spec("EC", {"curve": curve}, ['@const { privateKey: <<x1>> } = <<generateKeyPairSync>>("ec", { namedCurve: <<S>> });',
                                             '@const <<x2>> = <<createSign>>("SHA256");', "<<x2>>.update(<<d>>);"],
                    "<<x2>>.sign(<<x1>>)", f'"{name}"', "str", also_ok=["SHA-256"], api="generateKeyPairSync ec")

    def js_named(r, m=False):
        fam = r.choice(["Ed25519", "X25519"])
        return spec(fam, {}, ["@const <<x1>> = <<generateKeyPairSync>>(<<S>>);"],
                    '<<x1>>.publicKey.export({ type: "spki", format: "der" })', f'"{fam.lower()}"', "str",
                    api="generateKeyPairSync", carries_family=True)

    def js_dh(r, m=False):
        grp, bits = r.choice([("modp14", 2048), ("modp15", 3072)])
        return spec("DH", {"key_size": bits}, ["@const <<x1>> = <<getDiffieHellman>>(<<S>>);", "<<x1>>.generateKeys();"],
                    "<<x1>>.getPrime()", f'"{grp}"', "str", api="getDiffieHellman", carries_family=True)

    def js_hmac(r, m=False):
        fam = {1: "SHA-256", 2: "MD5"}.get(m) or r.choice(["MD5", "SHA-1", "SHA-256", "SHA-512"])
        return spec("HMAC", {"hash": fam}, ['@const <<x1>> = <<createHmac>>(<<S>>, "svc-<<w>>").update(<<d>>).digest("hex");'],
                    "<<x1>>", f'"{JS_HASH[fam]}"', "str", also_ok=[fam], api="createHmac")

    def js_pbkdf2(r, m=False):
        fam = "SHA-512" if m else r.choice(["SHA-1", "SHA-256", "SHA-512"])
        return spec("PBKDF2", {"hash": fam}, ['@const <<x1>> = <<pbkdf2Sync>>("pw-<<w>>", "salt", 1000, 32, <<S>>);'],
                    "<<x1>>", f'"{JS_HASH[fam]}"', "str", also_ok=[fam, "HMAC"], api="pbkdf2Sync")

    t1 = [js_hash, js_cipher, js_rsa, js_ec, js_named, js_dh, js_hmac, js_pbkdf2]
    t2 = [js_hash, js_cipher, js_rsa, js_ec, js_hmac]
    return {"t1": t1, "t2": t2, "pqc": [], "broad": t1}


class JsBuilder:
    """ts=True: ESM imports, type annotations (Node strips them). ts=False: CommonJS."""

    def __init__(self, rng, names, ts=False, imports="canonical"):
        self.rng, self.names, self.ts, self.mode = rng, names, ts, imports
        self.namespace = imports != "canonical" and rng.random() < 0.6
        self.ns = rng.choice(["crypto", "nodeCrypto", "cr"])
        self.spec_mod = '"node:crypto"' if imports == "canonical" or rng.random() < 0.5 else '"crypto"'
        self.used = set()
        self.top, self.funcs, self.mains = [], [], []

    def ref(self, fn):
        self.used.add(fn)
        return f"{self.ns}.{fn}" if self.namespace else fn

    def styles_for(self, sp):
        ok = ["const", "config", "default", "arg"]
        if self.ts:
            ok.append("table")
        if sp["kind"] == "str" and "-" in (sp["slot"] or ""):
            ok.append("template")
        return ok

    def add(self, sp, style, fid):
        nm, rng = self.names, self.rng
        m = {}
        for t in sp["body"] + [sp["ret"]]:
            for name in re.findall(r"<<(\w+)>>", t):
                if name[0].islower() and name not in m and not re.fullmatch(r"x\d|d|w|S", name):
                    m[name] = self.ref(name)
        m.update({f"x{i}": nm.camel() for i in range(1, 5)}, w=rng.choice(WORDS),
                 d=f'"{rng.choice(WORDS)}-{rng.randint(100, 999)}"')
        slot = sp["slot"]
        typ = {"str": "string", "int": "number"}[sp["kind"]] if sp["kind"] in ("str", "int") else None
        ann = lambda t: f": {t}" if self.ts and t else ""  # noqa: E731
        fn = nm.camel()
        params, args = "", ""
        if style == "inline":
            m["S"] = slot
        elif style == "const":
            c = nm.const()
            self.top.append((f"const {c}{ann(typ)} = {slot};", fid))
            m["S"] = c
        elif style == "config":
            c, k = nm.const(), nm.camel()
            self.top += [(f"const {c} = {{", None), (f"  {k}: {slot},", fid), ("}" + (" as const;" if self.ts else ";"), None)]
            m["S"] = f"{c}.{k}"
        elif style == "table":
            c, k = nm.const(), nm.key()
            self.top.append((f'const {c}: Record<string, {typ}> = {{ {k}: {slot} }};', fid))
            m["S"] = f'{c}["{k}"]'
        elif style == "default":
            p = nm.camel()
            params = f"{p}{ann(typ)} = {slot}"
            m["S"] = p
        elif style == "arg":
            p = nm.camel()
            params, args = f"{p}{ann(typ)}", slot
            m["S"] = p
        elif style == "template":
            head, tail = slot.strip('"').rsplit("-", 1)
            c = nm.camel()
            self.top.append((f'const {c} = "{tail}";', fid))
            m["S"] = f"`{head}-${{{c}}}`"
        line_fid = fid if style in ("default",) else None
        body = [(f"function {fn}({params}) {{", line_fid)]
        for line in sp["body"]:
            body.append(("  " + sub(line.lstrip("@"), m), fid if line.startswith("@") else None))
        body += [("  return " + sub(sp["ret"], m) + ";", None), ("}", None), ("", None)]
        self.funcs.append(body)
        self.mains.append((f"console.log(String({fn}({args})).length);", fid if style == "arg" else None))

    def filler(self):
        f = self.names.camel()
        n = self.rng.randint(2, 9)
        self.funcs.append([(f"function {f}(items{': number[]' if self.ts else ''}) {{", None),
                           (f"  return items.reduce((a, b) => a + b, 0) % {n};", None), ("}", None), ("", None)])

    def render(self):
        self.rng.shuffle(self.funcs)
        used = ", ".join(sorted(self.used))
        if self.ts:
            imp = f"import * as {self.ns} from {self.spec_mod};" if self.namespace else f"import {{ {used} }} from {self.spec_mod};"
        else:
            imp = (f"const {self.ns} = require({self.spec_mod});" if self.namespace
                   else f"const {{ {used} }} = require({self.spec_mod});")
        lines = [(f"// {self.rng.choice(['Partner API', 'Billing', 'Session', 'Export'])} helpers.", None), (imp, None), ("", None)]
        lines += self.top + ([("", None)] if self.top else [])
        for f in self.funcs:
            lines += f
        return lines + self.mains


# =============================================================================================
# C / OpenSSL 3
# =============================================================================================
C_MD = {"MD5": "EVP_md5", "SHA-1": "EVP_sha1", "SHA-256": "EVP_sha256", "SHA3-256": "EVP_sha3_256", "SHA-512": "EVP_sha512"}
C_MD_NAME = {"MD5": "MD5", "SHA-1": "SHA1", "SHA-256": "SHA256", "SHA-512": "SHA512"}
C_CIPHER = {  # ctor -> family, params
    "EVP_aes_128_ecb": ("AES", {"key_size": 128, "mode": "ECB"}), "EVP_aes_256_gcm": ("AES", {"key_size": 256, "mode": "GCM"}),
    "EVP_aes_192_cbc": ("AES", {"key_size": 192, "mode": "CBC"}), "EVP_aes_128_gcm": ("AES", {"key_size": 128, "mode": "GCM"}),
    "EVP_aes_256_ctr": ("AES", {"key_size": 256, "mode": "CTR"}), "EVP_des_ede3_cbc": ("3DES", {"mode": "CBC"}),
    "EVP_des_ede3_ecb": ("3DES", {"mode": "ECB"}), "EVP_chacha20_poly1305": ("ChaCha20-Poly1305", {}),
}
C_CIPHER_NAME = {"AES-192-CBC": ("AES", {"key_size": 192, "mode": "CBC"}), "AES-128-CBC": ("AES", {"key_size": 128, "mode": "CBC"}),
                 "AES-256-GCM": ("AES", {"key_size": 256, "mode": "GCM"}), "DES-EDE3-CBC": ("3DES", {"mode": "CBC"})}
CTX = ["EVP_CIPHER_CTX *<<x1>> = EVP_CIPHER_CTX_new();", "unsigned char <<x3>>[64] = {0};", "unsigned char <<x4>>[96];",
       "int <<x2>> = 0;"]
CTX_END = ['EVP_EncryptUpdate(<<x1>>, <<x4>>, &<<x2>>, (const unsigned char *)"0123456789abcdef", 16);',
           "EVP_CIPHER_CTX_free(<<x1>>);"]


def c_specs():
    def c_digest(r, m=False):
        fam = r.choice(["MD5", "SHA-1", "SHA-256", "SHA3-256"] + ([] if m else ["SHA-512"]))
        return spec(fam, {}, ["unsigned char <<x1>>[EVP_MAX_MD_SIZE];", "unsigned int <<x2>> = 0;",
                              "@EVP_Digest(<<d>>, <<dl>>, <<x1>>, &<<x2>>, <<S>>(), NULL);"], "(int)<<x2>>",
                    C_MD[fam], "md", api="EVP_Digest ctor", carries_family=True, includes=["openssl/evp.h"])

    def c_digest_name(r, m=False):
        fam = "SHA-1" if m else r.choice(list(C_MD_NAME))
        return spec(fam, {}, ["unsigned char <<x1>>[EVP_MAX_MD_SIZE];", "unsigned int <<x2>> = 0;",
                              "@const EVP_MD *<<x3>> = EVP_get_digestbyname(<<S>>);",
                              "@EVP_Digest(<<d>>, <<dl>>, <<x1>>, &<<x2>>, <<x3>>, NULL);"], "(int)<<x2>>",
                    f'"{C_MD_NAME[fam]}"', "str", api="EVP_get_digestbyname", carries_family=True, includes=["openssl/evp.h"])

    def c_cipher(r, m=False):
        ctor = r.choice({1: ["EVP_aes_128_ecb", "EVP_aes_256_gcm", "EVP_des_ede3_cbc", "EVP_chacha20_poly1305"],
                         2: ["EVP_des_ede3_ecb"]}.get(m, list(C_CIPHER)))
        fam, params = C_CIPHER[ctor]
        return spec(fam, params, CTX + ["@EVP_EncryptInit_ex(<<x1>>, <<S>>(), NULL, <<x3>>, <<x3>>);"] + CTX_END,
                    "<<x2>>", ctor, "cipher", api="EVP_EncryptInit_ex ctor", carries_family=True, includes=["openssl/evp.h"])

    def c_cipher_name(r, m=False):
        name = "AES-192-CBC" if m else r.choice(list(C_CIPHER_NAME))
        fam, params = C_CIPHER_NAME[name]
        return spec(fam, params, CTX + ["@EVP_CIPHER *<<x5>> = EVP_CIPHER_fetch(NULL, <<S>>, NULL);",
                                        "EVP_EncryptInit_ex2(<<x1>>, <<x5>>, <<x3>>, <<x3>>, NULL);"] + CTX_END
                    + ["EVP_CIPHER_free(<<x5>>);"], "<<x2>>", f'"{name}"', "str", api="EVP_CIPHER_fetch",
                    carries_family=True, includes=["openssl/evp.h"])

    def c_rsa_ctx(r, m=False):
        bits = r.choice([1024, 2048])
        return spec("RSA", {"key_size": bits}, ["EVP_PKEY *<<x2>> = NULL;", "@EVP_PKEY_CTX *<<x1>> = EVP_PKEY_CTX_new_id(EVP_PKEY_RSA, NULL);",
                                                "EVP_PKEY_keygen_init(<<x1>>);", "@EVP_PKEY_CTX_set_rsa_keygen_bits(<<x1>>, <<S>>);",
                                                "EVP_PKEY_keygen(<<x1>>, &<<x2>>);", "int <<x3>> = EVP_PKEY_get_bits(<<x2>>);",
                                                "EVP_PKEY_free(<<x2>>);", "EVP_PKEY_CTX_free(<<x1>>);"], "<<x3>>",
                    str(bits), "int", api="EVP_PKEY_CTX rsa bits", includes=["openssl/evp.h", "openssl/rsa.h"])

    def c_rsa_gen(r, m=False):
        bits = r.choice([1024, 2048])
        return spec("RSA", {"key_size": bits}, ["@EVP_PKEY *<<x2>> = EVP_RSA_gen(<<S>>);", "int <<x3>> = EVP_PKEY_get_bits(<<x2>>);",
                                                "EVP_PKEY_free(<<x2>>);"], "<<x3>>", str(bits), "int", api="EVP_RSA_gen",
                    includes=["openssl/evp.h", "openssl/rsa.h"])

    def c_rsa_legacy(r, m=False):
        bits = r.choice([1024, 2048])
        return spec("RSA", {"key_size": bits}, ["RSA *<<x1>> = RSA_new();", "BIGNUM *<<x2>> = BN_new();", "BN_set_word(<<x2>>, RSA_F4);",
                                                "@RSA_generate_key_ex(<<x1>>, <<S>>, <<x2>>, NULL);", "int <<x3>> = RSA_bits(<<x1>>);",
                                                "RSA_free(<<x1>>);", "BN_free(<<x2>>);"], "<<x3>>", str(bits), "int",
                    api="RSA_generate_key_ex", includes=["openssl/bn.h", "openssl/rsa.h"], legacy=True)

    def c_ec_nid(r, m=False):
        curve, nid = r.choice([("P-256", "NID_X9_62_prime256v1"), ("P-384", "NID_secp384r1"), ("P-521", "NID_secp521r1")])
        return spec("EC", {"curve": curve}, ["EVP_PKEY *<<x2>> = NULL;", "@EVP_PKEY_CTX *<<x1>> = EVP_PKEY_CTX_new_id(EVP_PKEY_EC, NULL);",
                                             "EVP_PKEY_keygen_init(<<x1>>);", "@EVP_PKEY_CTX_set_ec_paramgen_curve_nid(<<x1>>, <<S>>);",
                                             "EVP_PKEY_keygen(<<x1>>, &<<x2>>);", "int <<x3>> = EVP_PKEY_get_bits(<<x2>>);",
                                             "EVP_PKEY_free(<<x2>>);", "EVP_PKEY_CTX_free(<<x1>>);"], "<<x3>>", nid, "int",
                    api="EC paramgen nid", includes=["openssl/evp.h", "openssl/ec.h"])

    def c_ec_gen(r, m=False):
        curve, name = r.choice([("P-256", "P-256"), ("P-384", "secp384r1"), ("P-521", "secp521r1")])
        return spec("EC", {"curve": curve}, ["@EVP_PKEY *<<x2>> = EVP_EC_gen(<<S>>);", "int <<x3>> = EVP_PKEY_get_bits(<<x2>>);",
                                             "EVP_PKEY_free(<<x2>>);"], "<<x3>>", f'"{name}"', "str", api="EVP_EC_gen",
                    includes=["openssl/evp.h", "openssl/ec.h"])

    def c_ed(r, m=False):
        return spec("Ed25519", {}, ["@EVP_PKEY *<<x2>> = EVP_PKEY_Q_keygen(NULL, NULL, <<S>>);", "int <<x3>> = EVP_PKEY_get_bits(<<x2>>);",
                                    "EVP_PKEY_free(<<x2>>);"], "<<x3>>", '"ED25519"', "str", api="Q_keygen ED25519",
                    carries_family=True, includes=["openssl/evp.h"])

    def c_x25519(r, m=False):
        return spec("X25519", {}, ["EVP_PKEY *<<x2>> = NULL;", "@EVP_PKEY_CTX *<<x1>> = EVP_PKEY_CTX_new_id(<<S>>, NULL);",
                                   "EVP_PKEY_keygen_init(<<x1>>);", "EVP_PKEY_keygen(<<x1>>, &<<x2>>);",
                                   "int <<x3>> = EVP_PKEY_get_bits(<<x2>>);", "EVP_PKEY_free(<<x2>>);", "EVP_PKEY_CTX_free(<<x1>>);"],
                    "<<x3>>", "EVP_PKEY_X25519", "int", api="EVP_PKEY_X25519", carries_family=True, includes=["openssl/evp.h"])

    def c_dh(r, m=False):
        grp, bits = r.choice([("ffdhe2048", 2048), ("ffdhe3072", 3072)])
        return spec("DH", {"key_size": bits}, ["EVP_PKEY *<<x2>> = NULL;", '@EVP_PKEY_CTX *<<x1>> = EVP_PKEY_CTX_new_from_name(NULL, "DH", NULL);',
                                               "EVP_PKEY_keygen_init(<<x1>>);", "@EVP_PKEY_CTX_set_group_name(<<x1>>, <<S>>);",
                                               "EVP_PKEY_generate(<<x1>>, &<<x2>>);", "int <<x3>> = EVP_PKEY_get_bits(<<x2>>);",
                                               "EVP_PKEY_free(<<x2>>);", "EVP_PKEY_CTX_free(<<x1>>);"], "<<x3>>",
                    f'"{grp}"', "str", api="DH group", includes=["openssl/evp.h"])

    def c_hmac(r, m=False):
        fam = {1: "SHA-256", 2: "MD5"}.get(m) or r.choice(["MD5", "SHA-1", "SHA-256", "SHA-512"])
        return spec("HMAC", {"hash": fam}, ["unsigned char <<x1>>[EVP_MAX_MD_SIZE];", "unsigned int <<x2>> = 0;",
                                            '@HMAC(<<S>>(), "svc-key", 7, (const unsigned char *)<<d>>, <<dl>>, <<x1>>, &<<x2>>);'],
                    "(int)<<x2>>", C_MD[fam], "md", also_ok=[fam], api="HMAC", includes=["openssl/evp.h", "openssl/hmac.h"])

    def c_pbkdf2(r, m=False):
        fam = "SHA-1" if m else r.choice(["SHA-1", "SHA-256", "SHA-512"])
        return spec("PBKDF2", {"hash": fam}, ["unsigned char <<x1>>[32];",
                                              '@int <<x2>> = PKCS5_PBKDF2_HMAC("pw", 2, (const unsigned char *)"salt", 4, 1000, <<S>>(), 32, <<x1>>);'],
                    "<<x2>> + <<x1>>[0] - <<x1>>[0]", C_MD[fam], "md", also_ok=[fam, "HMAC"], api="PKCS5_PBKDF2_HMAC",
                    includes=["openssl/evp.h"])

    t1 = [c_digest, c_cipher, c_rsa_ctx, c_rsa_legacy, c_ec_nid, c_ed, c_x25519, c_dh, c_hmac, c_pbkdf2]
    t2 = [c_digest_name, c_cipher_name, c_cipher, c_rsa_gen, c_ec_gen, c_hmac]
    broad = t1 + [c_digest_name, c_cipher_name, c_rsa_gen, c_ec_gen]
    return {"t1": t1, "t2": t2, "pqc": [], "broad": broad}


C_TYPE = {"str": "const char *{n}", "int": "int {n}", "md": "const EVP_MD *(*{n})(void)",
          "cipher": "const EVP_CIPHER *(*{n})(void)"}


class CBuilder:
    STYLES = ["macro", "static", "struct", "array", "arg"]

    def __init__(self, rng, names, imports="canonical"):
        self.rng, self.names = rng, names
        self.includes, self.legacy = {"stdio.h"}, False
        self.top, self.funcs, self.mains = [], [], []

    def styles_for(self, sp):
        return [s for s in self.STYLES if not (s == "array" and sp["kind"] in ("md", "cipher"))]

    def add(self, sp, style, fid):
        nm, rng = self.names, self.rng
        self.includes.update(sp.get("includes", []))
        self.legacy |= bool(sp.get("legacy"))
        text = f"{rng.choice(WORDS)}-{rng.randint(100, 999)}"
        m = {f"x{i}": nm.var() for i in range(1, 6)}
        m.update(d=f'"{text}"', dl=str(len(text)))
        slot, kind = sp["slot"], sp["kind"]
        fn = nm.var()
        params, args = "void", ""
        if style == "inline":
            m["S"] = slot
        elif style == "macro":
            c = nm.const()
            self.top.append((f"#define {c} {slot}", fid))
            m["S"] = c
        elif style == "static":
            c = nm.var()
            decl = {"str": f"const char *const {c}", "int": f"const int {c}"}.get(kind) or C_TYPE[kind].format(n=c)
            self.top.append((f"static {decl} = {slot};", fid))
            m["S"] = c
        elif style == "struct":
            c = nm.var()
            field = C_TYPE[kind].format(n="value")
            self.top.append((f'static const struct {{ const char *label; {field}; }} {c} = {{"{rng.choice(WORDS)}", {slot}}};', fid))
            m["S"] = f"{c}.value"
        elif style == "array":
            c = nm.const()
            base = "const char *const" if kind == "str" else "const int"
            self.top.append((f"static {base} {c}[] = {{{slot}}};", fid))
            m["S"] = f"{c}[0]"
        elif style == "arg":
            p = nm.var()
            params, args = C_TYPE[kind].format(n=p), slot
            m["S"] = p
        body = [(f"static int {fn}({params}) {{", None)]
        for line in sp["body"]:
            body.append(("    " + sub(line.lstrip("@"), m), fid if line.startswith("@") else None))
        body += [("    return " + sub(sp["ret"], m) + ";", None), ("}", None), ("", None)]
        self.funcs.append(body)
        self.mains.append((f'    printf("%d\\n", {fn}({args}));', fid if style == "arg" else None))

    def filler(self):
        f = self.names.var()
        n = self.rng.randint(2, 9)
        self.funcs.append([(f"static int {f}(int v) {{", None), (f"    return (v * 31 + {n}) % 97;", None), ("}", None), ("", None)])
        self.mains.append((f'    printf("%d\\n", {f}({n}));', None))

    def render(self):
        self.rng.shuffle(self.funcs)
        lines = [(f"/* {self.rng.choice(['Telemetry agent', 'Payment link', 'Device enrolment', 'Archive tool'])} routines. */", None)]
        if self.legacy:
            lines.append(("#define OPENSSL_SUPPRESS_DEPRECATED", None))
        lines += [(f"#include <{i}>", None) for i in sorted(self.includes)] + [("", None)]
        lines += self.top + ([("", None)] if self.top else [])
        for f in self.funcs:
            lines += f
        return lines + [("int main(void) {", None)] + self.mains + [("    return 0;", None), ("}", None)]


# =============================================================================================
# Negative controls in the new languages: algorithm names in several statement shapes, no crypto.
# =============================================================================================

def negative_go(rng, names, phrases):
    c1, c2, f = names.camel(), names.camel(), names.camel()
    shapes = [f'const {c1} = "{phrases[0]}"', f'var {c2} = map[string]string{{"note": "{phrases[1]}"}}',
              f"func {f}() string {{", f'\treturn "{phrases[2]}"', "}"]
    body = ["// Ops notes for the " + rng.choice(WORDS) + " service.", "package main", "", 'import "fmt"', ""] + shapes + [
        "", "func main() {", f'\tfmt.Println({c1}, {c2}["note"], {f}())', f'\tfmt.Printf("%s\\n", "{phrases[3]}")', "}", ""]
    return "\n".join(body)


def negative_js(rng, names, phrases, ts=False):
    c1, f = names.const(), names.camel()
    return "\n".join([f"// {rng.choice(['Settings', 'Release', 'Audit'])} copy.",
                      f'const {c1}{": string[]" if ts else ""} = ["{phrases[0]}", "{phrases[1]}"];',
                      f"function {f}(){': string' if ts else ''} {{", f'  return `{phrases[2]}`;', "}",
                      f'console.log({c1}.join("; "), {f}());', f'console.error("{phrases[3]}");', ""])


def negative_c(rng, names, phrases):
    c1, f = names.var(), names.var()
    return "\n".join([f"/* {rng.choice(['Changelog', 'Operator notes'])}: {phrases[0]}. */", "#include <stdio.h>", "",
                      f'static const char *const {c1}[] = {{"{phrases[1]}", "{phrases[2]}"}};', "",
                      f"static const char *{f}(void) {{", f'    return "{phrases[3]}";', "}", "",
                      "int main(void) {", f'    printf("%s %s %s\\n", {c1}[0], {c1}[1], {f}());', "    return 0;", "}", ""])
