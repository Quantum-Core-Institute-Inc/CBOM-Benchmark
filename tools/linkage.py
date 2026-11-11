"""Linkage, for the system fixture: can a finding be routed to the team that fixes it, and does the
CBOM connect the assets that belong together?

Routable. A detected system finding is routable when at least one of its reported locations
resolves, through the fixture's CODEOWNERS, to the finding's owner. When the algorithm is decided
by the shared wrapper and its config, reporting only the wrapper or the config still counts as
detected (they're alt files), but CODEOWNERS sends that ticket to platform-security, not to the team
whose call site has to change. That is the difference this measures.

Asset links. The answer key lists pairs of files whose assets belong together (the nginx config and
the certificate it serves, the certificate and its private key). A link is found when a component
located in the first file references a component located in the second: any *Ref / *RefArray in its
cryptoProperties, a cipher suite's algorithms, or a dependencies entry (dependsOn / provides).
"""
from __future__ import annotations

import fnmatch
from pathlib import Path

from cbomlib import _walk, norm_path, same_file

ROOT = Path(__file__).resolve().parent.parent


def parse_codeowners(path: Path) -> list[tuple[str, list[str]]]:
    rules = []
    for line in Path(path).read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            pat, *owners = line.split()
            rules.append((pat, owners))
    return rules


def owner_of(rel: str, rules) -> str | None:
    """GitHub semantics, the subset the fixture uses: last match wins; a leading / anchors to the
    root; a trailing / matches everything under that directory; * alone matches everything."""
    found = None
    for pat, owners in rules:
        p = pat.lstrip("/")
        if pat == "*":
            hit = True
        elif pat.endswith("/"):
            hit = rel.startswith(p) if pat.startswith("/") else ("/" + p) in ("/" + rel)
        elif pat.startswith("/"):
            hit = rel == p or fnmatch.fnmatch(rel, p)
        else:
            hit = fnmatch.fnmatch(Path(rel).name, p) or fnmatch.fnmatch(rel, p)
        if hit:
            found = owners[0] if owners else None
    return found


def _system_rel(path: str, root: str) -> str | None:
    """'corpus/system/payments-platform/services/x.go' (or any path ending in it) -> 'services/x.go'."""
    p = norm_path(path)
    i = p.find(root.rstrip("/") + "/")
    if i < 0:
        marker = "/" + Path(root).name + "/"
        j = p.find(marker)
        return p[j + len(marker):] if j >= 0 else None
    return p[i + len(root.rstrip("/")) + 1:]


def _refs(c: dict) -> set[str]:
    out = set()

    def walk(x, key=""):
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, k)
        elif isinstance(x, list):
            for v in x:
                walk(v, key)
        elif isinstance(x, str) and (key.endswith("Ref") or key.endswith("RefArray") or key == "algorithms"):
            out.add(x)
    walk(c.get("cryptoProperties") or {})
    return out


def asset_links(bom: dict, links: list[dict]) -> list[dict]:
    comps = [c for c in _walk(bom.get("components")) if c.get("bom-ref")]
    refs = {c["bom-ref"]: _refs(c) for c in comps}
    for d in bom.get("dependencies") or []:
        refs.setdefault(d.get("ref"), set()).update((d.get("dependsOn") or []) + (d.get("provides") or []))

    def located(file):
        return {c["bom-ref"] for c in comps
                if any(same_file(o.get("location", ""), file) for o in (c.get("evidence") or {}).get("occurrences") or [])}
    out = []
    for link in links:
        src, dst = located(link["from"]), located(link["to"])
        out.append({"id": link["id"], "from": link["from"], "to": link["to"], "why": link["why"],
                    "found": any(refs.get(s, set()) & dst for s in src)})
    return out


def evaluate(results: list[dict], gt: dict, bom: dict) -> dict | None:
    sysinfo = gt.get("system")
    sys_results = [r for r in results if r["tier"] == "system"]
    if not sysinfo or not sys_results:
        return None
    rules = parse_codeowners(ROOT / sysinfo["codeowners"])
    owners = {f["id"]: f.get("owner") for f in gt["findings"]}
    rows = []
    for r in sys_results:
        if not r["detected"]:
            continue
        got = sorted({owner_of(rel, rules) for p in r.get("reported_files") or []
                      if (rel := _system_rel(p, sysinfo["root"])) is not None} - {None})
        rows.append({"id": r["id"], "owner": owners.get(r["id"]), "routed_to": got,
                     "routable": owners.get(r["id"]) in got})
    links = asset_links(bom, gt.get("links", []))
    n = len(rows)
    routable = sum(x["routable"] for x in rows)
    wrong = [x for x in rows if not x["routable"]]
    return {"system_findings": len(sys_results), "detected": n, "routable": routable,
            "routable_pct": round(100 * routable / n, 1) if n else None,
            "misrouted": [{"id": x["id"], "owner": x["owner"], "routed_to": x["routed_to"]} for x in wrong],
            "links": links, "links_found": sum(x["found"] for x in links), "links_expected": len(links)}


def markdown(lk: dict | None) -> str:
    if not lk:
        return ""
    out = ["## System fixture: routing and asset links", "",
           f"**Routable: {lk['routable']}/{lk['detected']} detected system findings"
           + (f" ({lk['routable_pct']}%)" if lk["routable_pct"] is not None else "") + "** "
           f"(of {lk['system_findings']}). Routable means a reported location resolves, through the "
           "fixture's CODEOWNERS, to the team that owns the fix. Reporting only the shared wrapper or its "
           "config is detection, but the ticket lands with platform-security.", ""]
    if lk["misrouted"]:
        out += ["| Finding | Owner | Reported locations route to |", "|---|---|---|"]
        out += [f"| {m['id']} | {m['owner']} | {', '.join(m['routed_to']) or 'nowhere'} |" for m in lk["misrouted"]]
        out.append("")
    out += [f"**Asset links: {lk['links_found']}/{lk['links_expected']}.**", "",
            "| Link | Found |", "|---|---|"]
    out += [f"| {x['why']} | {'yes' if x['found'] else 'no'} |" for x in lk["links"]]
    return "\n".join(out + [""])
