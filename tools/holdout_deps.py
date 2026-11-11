"""Holdout dependency manifests (imported by holdout.py).

Every version below exists: checked against PyPI and npm, against Maven Central's search API, and
against the projects' Git tags on 2026-11-10. Post-quantum capability is derived from the thresholds
cited in expected/libraries.json (cryptography 48.0.0, Bouncy Castle 1.79, CIRCL 1.4.0 for ML-KEM);
libraries whose status wasn't verified carry None.
"""
from __future__ import annotations

from holdout_common import WORDS


def _v(s):
    return tuple(int(x) for x in s.replace("w", "").split(".") if x.isdigit())


CATALOG = {
    "pypi": [  # (package, library key, versions, pq rule)
        ("cryptography", "pyca-cryptography", ["41.0.7", "42.0.8", "43.0.3", "44.0.3", "46.0.3", "48.0.0", "48.0.1", "49.0.0", "50.0.1"],
         lambda v: _v(v) >= (48,)),
        ("pycryptodome", "pycryptodome", ["3.18.0", "3.19.0", "3.20.0", "3.21.0"], lambda v: False),
        ("pyOpenSSL", "pyopenssl", ["23.2.0", "23.3.0", "24.1.0", "24.3.0"], lambda v: None),
        ("PyJWT", "pyjwt", ["2.6.0", "2.8.0", "2.9.0", "2.10.1"], lambda v: False),
        ("paramiko", "paramiko", ["3.3.1", "3.4.0", "3.5.0"], lambda v: None),
        ("bcrypt", "bcrypt", ["4.0.1", "4.1.2", "4.2.0"], lambda v: None),
        ("liboqs-python", "liboqs", ["0.16.0"], lambda v: True),
    ],
    "npm": [
        ("jsonwebtoken", "jsonwebtoken", ["8.5.1", "9.0.0", "9.0.2"], lambda v: False),
        ("crypto-js", "crypto-js", ["4.1.1", "4.2.0"], lambda v: False),
        ("node-forge", "node-forge", ["1.3.0", "1.3.1"], lambda v: None),
        ("bcryptjs", "bcryptjs", ["2.4.3", "3.0.2"], lambda v: None),
        ("@noble/post-quantum", "noble-post-quantum", ["0.4.1", "0.5.4", "0.6.0"], lambda v: True),
    ],
    "maven": [
        ("org.bouncycastle:bcprov-jdk18on", "bouncycastle", ["1.76", "1.77", "1.78.1", "1.79", "1.80"], lambda v: _v(v) >= (1, 79)),
        ("org.bouncycastle:bcprov-jdk15on", "bouncycastle", ["1.68", "1.69", "1.70"], lambda v: False),
        ("com.nimbusds:nimbus-jose-jwt", "nimbus-jose-jwt", ["9.37.3"], lambda v: None),
        ("io.jsonwebtoken:jjwt-api", "jjwt", ["0.12.5"], lambda v: None),
    ],
    "golang": [
        ("github.com/cloudflare/circl", "circl", ["1.3.9", "1.4.0", "1.5.0", "1.6.1"], lambda v: _v(v) >= (1, 4)),
        ("golang.org/x/crypto", "golang-x-crypto", ["0.17.0", "0.24.0", "0.31.0"], lambda v: None),
        ("github.com/golang-jwt/jwt/v5", "golang-jwt", ["5.2.0", "5.2.1"], lambda v: None),
    ],
    "conan": [
        ("openssl", "openssl", ["1.1.1w"], lambda v: False),
        ("libsodium", "libsodium", ["1.0.18"], lambda v: None),
    ],
}
FILLER = {"pypi": [("requests", "2.31.0"), ("click", "8.1.7"), ("python-dateutil", "2.8.2")],
          "npm": [("lodash", "4.17.21"), ("express", "4.19.2")],
          "maven": [("org.slf4j:slf4j-api", "2.0.13"), ("com.google.guava:guava", "33.2.1-jre")],
          "golang": [], "conan": [("zlib", "1.3.1")]}
FORMATS = {"pypi": ["requirements.txt", "pyproject.toml"], "npm": ["package.json"], "maven": ["pom.xml", "build.gradle"],
           "golang": ["go.mod"], "conan": ["conanfile.txt"]}
DECOYS = {"pypi": ("pycrypto", "pycrypto", "2.6.1"), "maven": ("org.jasypt:jasypt", "jasypt", "1.9.3")}


def generate_app(rng, names, app_dir: str):
    """-> (files {rel: text}, libraries [...], decoys [...], lookalikes [...])"""
    eco = rng.choice(list(CATALOG))
    fmt = rng.choice(FORMATS[eco])
    cat = list(CATALOG[eco])
    rng.shuffle(cat)
    picked, keys = [], set()
    for pkg, key, versions, pq in cat:
        if key in keys:
            continue
        keys.add(key)
        picked.append((pkg, key, rng.choice(versions), pq))
        if len(picked) >= rng.randint(2, 4):
            break
    decoy = DECOYS.get(eco) if rng.random() < 0.5 and fmt in ("requirements.txt", "pom.xml") else None
    lookalike = eco in ("pypi", "npm") and fmt != "pyproject.toml" and rng.random() < 0.5
    filler = rng.sample(FILLER[eco], min(len(FILLER[eco]), rng.randint(0, 2)))
    rel = f"{app_dir}/{fmt}"
    deps = [(p, v) for p, _, v, _ in picked] + filler
    rng.shuffle(deps)
    if fmt == "requirements.txt":
        lines = [f"# {rng.choice(WORDS)} service dependencies"] + [f"{p}=={v}" for p, v in deps]
        if lookalike:
            lines.insert(rng.randint(1, len(lines)), "hashids==1.3.1")
        if decoy:
            lines.append(f"# {decoy[0]}=={decoy[2]}  removed")
        text = "\n".join(lines) + "\n"
    elif fmt == "pyproject.toml":
        text = "\n".join(["[project]", f'name = "{names.snake().replace("_", "-")}"', 'version = "1.0.0"', "dependencies = ["]
                         + [f'    "{p}=={v}",' for p, v in deps] + ["]", ""])
    elif fmt == "package.json":
        allp = deps + ([("hashids", "2.3.0")] if lookalike else [])
        body = ",\n".join(f'    "{p}": "{v}"' for p, v in sorted(allp))
        text = f'{{\n  "name": "{names.snake().replace("_", "-")}",\n  "version": "1.0.0",\n  "private": true,\n  "dependencies": {{\n{body}\n  }}\n}}\n'
    elif fmt == "pom.xml":
        use_prop = rng.random() < 0.5
        props, deps_xml = [], []
        for p, v in deps:
            g, a = p.split(":")
            ver = v
            if use_prop and g == "org.bouncycastle":
                props.append(f"    <bc.version>{v}</bc.version>")
                ver = "${bc.version}"
            deps_xml.append(f"    <dependency>\n      <groupId>{g}</groupId>\n      <artifactId>{a}</artifactId>\n      <version>{ver}</version>\n    </dependency>")
        if decoy:
            g, a = decoy[0].split(":")
            deps_xml.append(f"    <!--\n    <dependency>\n      <groupId>{g}</groupId>\n      <artifactId>{a}</artifactId>\n      <version>{decoy[2]}</version>\n    </dependency>\n    -->")
        text = ('<?xml version="1.0" encoding="UTF-8"?>\n<project xmlns="http://maven.apache.org/POM/4.0.0">\n'
                f"  <modelVersion>4.0.0</modelVersion>\n  <groupId>com.acme</groupId>\n  <artifactId>{names.snake().replace('_', '-')}</artifactId>\n"
                "  <version>1.0.0</version>\n" + (f"  <properties>\n{chr(10).join(props)}\n  </properties>\n" if props else "")
                + "  <dependencies>\n" + "\n".join(deps_xml) + "\n  </dependencies>\n</project>\n")
    elif fmt == "build.gradle":
        text = "plugins {\n    id 'java'\n}\n\nrepositories {\n    mavenCentral()\n}\n\ndependencies {\n" + "".join(
            f"    implementation '{p}:{v}'\n" for p, v in deps) + "}\n"
    elif fmt == "go.mod":
        text = f"module example.com/{names.snake().replace('_', '-')}\n\ngo 1.24\n\nrequire (\n" + "".join(
            f"\t{p} v{v}\n" for p, v in sorted(deps)) + ")\n"
    else:  # conanfile.txt
        text = "[requires]\n" + "".join(f"{p}/{v}\n" for p, v in deps) + "\n[generators]\nCMakeDeps\n"
    libs = [{"file": rel, "ecosystem": eco, "package": p, "library": k, "version": v, "scope": "direct", "pq_capable": pq(v)}
            for p, k, v, pq in picked]
    decoys = [{"file": rel, "library": decoy[1], "why": "commented out"}] if decoy else []
    looks = [{"file": rel, "library": "hashids", "why": "not cryptography"}] if lookalike else []
    return {rel: text}, libs, decoys, looks
