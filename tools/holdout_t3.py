"""Tier 3 holdout: multi-file Python and Java projects (imported by holdout.py).

Three patterns, mirroring the published Tier 3 kinds without reusing any of their names:
  constant   the algorithm or parameter is defined in one module and used in another
  wrapper    a shared helper does the crypto; each caller binds the parameter (one finding per caller,
             anchored at the call, with the helper as an alternate location: the published convention)
  registry   strategy classes with random names, selected through a registry / factory map
Spec bodies come from holdout.py's canonical (published) spellings; imports are canonical.
"""
from __future__ import annotations

import re

from holdout_common import WORDS, sub


def _refs(texts, mods, lang):
    """Canonical import lines and refs for every module placeholder used in texts."""
    imports, m = set(), {}
    for t in texts:
        for name in re.findall(r"<<(\w+)>>", t):
            if name in m or name in ("S", "d", "d32", "w") or re.fullmatch(r"x\d", name):
                continue
            imp, ref = mods[name][0]
            if imp:
                imports.add(imp)
            m[name] = ref
    return imports, m


def _locals(rng, names, m, lang):
    m.update({f"x{i}": names.var() for i in range(1, 5)}, w=rng.choice(WORDS))
    if lang == "python":
        m["d"], m["d32"] = f'b"{rng.choice(WORDS)}-{rng.randint(100, 999)}"', 'b"0123456789abcdef0123456789abcdef"'
    else:
        m["d"] = f'"{rng.choice(WORDS)}-{rng.randint(100, 999)}".getBytes()'
    return m


class Project:
    def __init__(self):
        self.files = {}  # rel path -> list of (text, anchor_id)

    def put(self, rel, lines):
        self.files[rel] = lines


def _py_body(sp, m, indent="    "):
    return [(indent + sub(line.lstrip("@"), m), "F" if line.startswith("@") else None) for line in sp["body"]]


def python_project(rng, names, pattern, specs, mods):
    """specs: list of spec dicts (wrapper: same body, one per caller). Returns (Project, findings) where
    findings are dicts: family, params, file, anchor tag, alt (file, tag) list, also_ok."""
    pkg = names.snake().split("_")[1] + "_" + rng.choice(["core", "svc", "lib", "app"])
    proj, finds = Project(), []
    proj.put(f"{pkg}/__init__.py", [])
    if pattern == "constant":
        sp = specs[0]
        settings, service, const, fn = names.snake(), names.snake(), names.const(), names.snake()
        imp_s, m_s = _refs([sp["slot"]], mods, "python")
        slot = sub(sp["slot"], m_s)
        filler = [(f'{names.const()} = "{rng.choice(WORDS)}"', None), (f"{names.const()} = {rng.randint(2, 90)}", None)]
        proj.put(f"{pkg}/{settings}.py", [(f'"""{rng.choice(WORDS).capitalize()} settings."""', None)]
                 + [(i, None) for i in sorted(imp_s)] + [("", None)] + filler + [(f"{const} = {slot}", "D")])
        imp, m = _refs(sp["body"] + [sp["ret"]], mods, "python")
        m = _locals(rng, names, m, "python")
        m["S"] = f"{settings}.{const}"
        lines = [(f'"""{rng.choice(WORDS).capitalize()} service."""', None)] + [(i, None) for i in sorted(imp)] + [
            (f"from {pkg} import {settings}", None), ("", None), ("", None), (f"def {fn}():", None)]
        lines += _py_body(sp, m) + [("    return " + sub(sp["ret"], m), None)]
        proj.put(f"{pkg}/{service}.py", lines)
        proj.put("main.py", [(f"from {pkg} import {service}", None), ("", None), ('if __name__ == "__main__":', None),
                             (f"    print(len(repr({service}.{fn}())))", None)])
        finds.append({"spec": sp, "file": f"{pkg}/{service}.py", "tag": "F", "alt": [(f"{pkg}/{settings}.py", "D")]})
    elif pattern == "wrapper":
        sp = specs[0]
        lib, fn, p = names.snake(), names.snake(), names.key()
        imp, m = _refs(sp["body"] + [sp["ret"]], mods, "python")
        m = _locals(rng, names, m, "python")
        m["S"] = p
        lines = [(f'"""Shared {rng.choice(WORDS)} helper."""', None)] + [(i, None) for i in sorted(imp)] + [("", None), ("", None),
                                                                                                    (f"def {fn}({p}):", None)]
        lines += _py_body(sp, m) + [("    return " + sub(sp["ret"], m), None)]
        proj.put(f"{pkg}/{lib}.py", lines)
        mains = []
        for i, csp in enumerate(specs):
            caller, cfn = names.snake(), names.snake()
            imp_c, m_c = _refs([csp["slot"]], mods, "python")
            tag = f"C{i}"
            proj.put(f"{pkg}/{caller}.py", [(f'"""{rng.choice(WORDS).capitalize()} flow."""', None)] + [(x, None) for x in sorted(imp_c)]
                     + [(f"from {pkg} import {lib}", None), ("", None), ("", None), (f"def {cfn}():", None),
                        (f"    return {lib}.{fn}({sub(csp['slot'], m_c)})", tag)])
            mains.append((caller, cfn))
            finds.append({"spec": csp, "file": f"{pkg}/{caller}.py", "tag": tag, "alt": [(f"{pkg}/{lib}.py", "F")]})
        proj.put("main.py", [(f"from {pkg} import {', '.join(c for c, _ in mains)}", None), ("", None), ('if __name__ == "__main__":', None)]
                 + [(f"    print(len(repr({c}.{f}())))", None) for c, f in mains])
    else:  # registry
        mod = names.snake()
        imps, classes, body = set(), [], []
        for i, sp in enumerate(specs):
            imp, m = _refs(sp["body"] + [sp["ret"], sp["slot"] or ""], mods, "python")
            imps |= imp
            m = _locals(rng, names, m, "python")
            m["S"] = sub(sp["slot"], m) if sp["slot"] else None
            cls = names.cap() + rng.choice(["Strategy", "Handler", "Provider", "Codec"])
            tag = f"R{i}"
            body += [("", None), ("", None), (f"class {cls}:", None), ("    def run(self):", None)]
            body += [("    " + t, tag if a else None) for t, a in _py_body(sp, m)] + [("        return " + sub(sp["ret"], m), None)]
            classes.append(cls)
            finds.append({"spec": sp, "file": f"{pkg}/{mod}.py", "tag": tag, "alt": []})
        keys = [names.key() for _ in classes]
        reg = names.const()
        lines = [(f'"""{rng.choice(WORDS).capitalize()} strategies."""', None)] + [(i, None) for i in sorted(imps)] + body + [
            ("", None), ("", None), (f"{reg} = {{" + ", ".join(f'"{k}": {c}' for k, c in zip(keys, classes)) + "}", None)]
        proj.put(f"{pkg}/{mod}.py", lines)
        proj.put("main.py", [(f"from {pkg}.{mod} import {reg}", None), ("", None), ('if __name__ == "__main__":', None),
                             (f"    for profile in {keys!r}:", None), (f"        print(len(repr({reg}[profile]().run())))", None)])
    return proj, finds


def java_project(rng, names, pattern, specs, mods):
    root = rng.choice(WORDS)
    base = f"com/{root}"
    proj, finds = Project(), []
    jtype = lambda sp: {"str": "String", "num": "int"}[sp["kind"]]  # noqa: E731

    def method(sp, m, name, params="", static=True):
        out = [(f"    public {'static ' if static else ''}Object {name}({params}) throws Exception {{", None)]
        out += [("        " + sub(line.lstrip("@"), m), "F" if line.startswith("@") else None) for line in sp["body"]]
        return out + [("        return " + sub(sp["ret"], m) + ";", None), ("    }", None)]

    def imports_for(sp):
        imp, m = _refs(sp["body"] + [sp["ret"]], mods, "java")
        return imp, _locals(rng, names, m, "java")

    mains = []
    if pattern == "constant":
        sp = specs[0]
        consts, svc, cname = names.cap(), names.cap() + "Service", names.const()
        proj.put(f"src/{base}/config/{consts}.java", [(f"package com.{root}.config;", None), ("", None),
                                                      (f"public final class {consts} {{", None), (f"    private {consts}() {{}}", None),
                                                      (f"    public static final {jtype(sp)} {cname} = {sp['slot']};", "D"), ("}", None)])
        imp, m = imports_for(sp)
        m["S"] = f"{consts}.{cname}"
        proj.put(f"src/{base}/svc/{svc}.java", [(f"package com.{root}.svc;", None), ("", None)] + [(i, None) for i in sorted(imp)]
                 + [(f"import com.{root}.config.{consts};", None), ("", None), (f"public class {svc} {{", None)]
                 + method(sp, m, "run") + [("}", None)])
        mains.append((f"com.{root}.svc.{svc}", "run()"))
        finds.append({"spec": sp, "file": f"src/{base}/svc/{svc}.java", "tag": "F", "alt": [(f"src/{base}/config/{consts}.java", "D")]})
    elif pattern == "wrapper":
        sp = specs[0]
        util, p = names.cap() + "Crypto", names.key().replace("_", "")
        imp, m = imports_for(sp)
        m["S"] = p
        proj.put(f"src/{base}/util/{util}.java", [(f"package com.{root}.util;", None), ("", None)] + [(i, None) for i in sorted(imp)]
                 + [("", None), (f"public final class {util} {{", None)] + method(sp, m, "apply", f"{jtype(sp)} {p}") + [("}", None)])
        for i, csp in enumerate(specs):
            caller = names.cap() + rng.choice(["Flow", "Job", "Task"])
            tag = f"C{i}"
            proj.put(f"src/{base}/app/{caller}.java", [(f"package com.{root}.app;", None), ("", None),
                                                       (f"import com.{root}.util.{util};", None), ("", None),
                                                       (f"public class {caller} {{", None),
                                                       ("    public static Object run() throws Exception {", None),
                                                       (f"        return {util}.apply({csp['slot']});", tag), ("    }", None), ("}", None)])
            mains.append((f"com.{root}.app.{caller}", "run()"))
            finds.append({"spec": csp, "file": f"src/{base}/app/{caller}.java", "tag": tag, "alt": [(f"src/{base}/util/{util}.java", "F")]})
    else:  # registry: interface + randomly named implementations + factory map
        iface = names.cap() + "Operation"
        proj.put(f"src/{base}/ops/{iface}.java", [(f"package com.{root}.ops;", None), ("", None), (f"public interface {iface} {{", None),
                                                  ("    Object run() throws Exception;", None), ("}", None)])
        entries = []
        for i, sp in enumerate(specs):
            cls = names.cap() + rng.choice(["Strategy", "Handler", "Provider", "Codec"])
            imp, m = imports_for(sp)
            m["S"] = sp["slot"]
            tag = f"R{i}"
            lines = [(f"package com.{root}.ops;", None), ("", None)] + [(x, None) for x in sorted(imp)] + [
                ("", None), (f"public class {cls} implements {iface} {{", None), ("    @Override", None)]
            lines += [(t, tag if a else None) for t, a in method(sp, m, "run", static=False)] + [("}", None)]
            proj.put(f"src/{base}/ops/{cls}.java", lines)
            entries.append((names.key(), cls))
            finds.append({"spec": sp, "file": f"src/{base}/ops/{cls}.java", "tag": tag, "alt": []})
        fac = names.cap() + "Factory"
        proj.put(f"src/{base}/ops/{fac}.java", [(f"package com.{root}.ops;", None), ("", None), ("import java.util.Map;", None),
                                                ("import java.util.function.Supplier;", None), ("", None),
                                                (f"public final class {fac} {{", None),
                                                (f"    static final Map<String, Supplier<{iface}>> OPS = Map.of(" + ", ".join(
                                                    f'"{k}", {c}::new' for k, c in entries) + ");", None),
                                                (f"    public static {iface} forKey(String k) {{ return OPS.get(k).get(); }}", None),
                                                ("}", None)])
        for k, _ in entries:
            mains.append((f"com.{root}.ops.{fac}", f'forKey("{k}").run()'))
    proj.put(f"src/{base}/Main.java", [(f"package com.{root};", None), ("", None), ("public class Main {", None),
                                       ("    public static void main(String[] args) throws Exception {", None)]
             + [(f"        System.out.println(String.valueOf({cls}.{call}).length());", None) for cls, call in mains]
             + [("    }", None), ("}", None)])
    return proj, finds, f"com.{root}.Main"
