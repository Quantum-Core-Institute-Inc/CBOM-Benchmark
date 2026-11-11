"""Policy engine: date every cryptographic finding against a published transition policy.

A policy is a JSON file in policies/: an ordered list of rules, first match wins. Each rule
gives a status and, where there is one, the date after which the algorithm is disallowed.
A policy may inherit another (EO 14412 inherits NIST); the stricter verdict always wins, so an
overlay can only bring a deadline forward, never push one back.

Statuses:
  not-approved   not permitted under this policy at all          -> due now
  disallowed     disallowed after a date (which may be past)      -> due on that date
  deprecated     allowed with risk until a disallow date          -> due on that date
  approved       no deadline
  review         policy leaves the call to the organization       -> flagged, no date
  out-of-scope   the policy doesn't speak to it
  unknown        no rule matched (e.g. a key size the scanner didn't report)
"""
from __future__ import annotations

import datetime as dt
import json
from fnmatch import fnmatch
from pathlib import Path

from cbomlib import CLASSICALLY_BROKEN, FAMILIES

ROOT = Path(__file__).resolve().parent.parent
POLICY_DIR = ROOT / "policies"
DEFAULT_AS_OF = dt.date(2026, 11, 10)

BUCKETS = [  # (key, label, weight in deadline-weighted recall)
    ("now", "Due now (not approved or past its date)", 5),
    ("by-2030", "Due by end of 2030", 4),
    ("2031-2033", "Due 2031 to 2033", 3),
    ("2034-2035", "Due 2034 to 2035", 2),
    ("none", "No deadline (approved, review, out of scope, unknown)", 1),
]
WEIGHT = {k: w for k, _, w in BUCKETS}
LABEL = {k: lbl for k, lbl, _ in BUCKETS}

# Default system type per location, for policies (CNSA 2.0) whose dates depend on it.
# Override with --use-map: a JSON list of [glob, use] pairs, first match wins.
DEFAULT_USE_MAP = [
    ["*firmware*", "firmware-signing"],
    ["*/ssh/*", "networking"],
    ["*/tls/*", "web"],
    ["*/k8s/*", "web"],
    ["*/keystores/*", "web"],
    ["*/certs/*", "web"],
    ["*", "custom"],
]


def load_policy(pid: str) -> dict:
    p = POLICY_DIR / f"{pid}.json"
    if not p.exists():
        raise SystemExit(f"unknown policy {pid!r}; have: {', '.join(sorted(x.stem for x in POLICY_DIR.glob('*.json')))}")
    pol = json.loads(p.read_text(encoding="utf-8"))
    if pol.get("inherits"):
        pol["_parent"] = load_policy(pol["inherits"])
    return pol


def infer_use(path: str, use_map=None) -> str:
    for pattern, use in (use_map or DEFAULT_USE_MAP):
        if fnmatch(path, pattern):
            return use
    return "custom"


def _flag(family: str, flag: str) -> bool:
    if flag == "broken":
        return family in CLASSICALLY_BROKEN
    return bool(FAMILIES.get(family, {}).get(flag))


def _cond(value, cond: dict) -> bool:
    if value is None:
        return False  # unknown parameter: the rule can't be shown to apply
    if "lt" in cond:
        return isinstance(value, (int, float)) and value < cond["lt"]
    if "gte" in cond:
        return isinstance(value, (int, float)) and value >= cond["gte"]
    if "in" in cond:
        return value in cond["in"]
    if "not_in" in cond:
        return value not in cond["not_in"]
    return False


def _matches(rule: dict, family: str, params: dict, use: str, primitive: str | None) -> bool:
    m = rule.get("match", {})
    if "family" in m and family not in m["family"]:
        return False
    if "flag" in m and not _flag(family, m["flag"]):
        return False
    if "name_contains" in m and not any(s in family for s in m["name_contains"]):
        return False
    for key, cond in m.get("params", {}).items():
        if not _cond(params.get(key), cond):
            return False
    if "use" in m and not _cond(use, m["use"]):
        return False
    if "primitive" in m and not _cond(primitive, m["primitive"]):
        return False
    return True


def _verdict(pol: dict, rule: dict | None, use: str) -> dict:
    if rule is None:
        return {"policy": pol["id"], "status": "unknown", "disallowed_after": None, "rule": None,
                "note": "No rule matched (often a missing key size or curve).", "source": None}
    d = rule.get("disallowed_after")
    if d == "use":
        d = pol.get("use_dates", {}).get(use) or pol.get("use_dates", {}).get("custom")
    return {"policy": pol["id"], "status": rule["status"], "deprecated_after": rule.get("deprecated_after"),
            "disallowed_after": d, "rule": rule["id"], "note": rule.get("note", ""), "source": rule.get("source"),
            "use": use}


def _strictness(v: dict) -> tuple:
    """Lower sorts stricter: not-approved, then earliest date, then everything without one."""
    if v["status"] == "not-approved":
        return (0, "")
    if v.get("disallowed_after"):
        return (1, v["disallowed_after"])
    return (2, "")


def evaluate(pol: dict, family: str, params: dict | None = None, use: str = "custom",
             primitive: str | None = None) -> dict:
    params = params or {}
    primitive = primitive or FAMILIES.get(family, {}).get("primitive")
    own = next((r for r in pol["rules"] if _matches(r, family, params, use, primitive)), None)
    mine = _verdict(pol, own, use)
    if "_parent" not in pol:
        return mine
    parent = evaluate(pol["_parent"], family, params, use, primitive)
    if own is None:
        return parent
    return min((mine, parent), key=_strictness) if parent["status"] != "unknown" else mine


def due_date(v: dict) -> str | None:
    if v["status"] == "not-approved":
        return "now"
    return v.get("disallowed_after")


def bucket(v: dict, as_of: dt.date = DEFAULT_AS_OF) -> str:
    if v["status"] == "not-approved":
        return "now"
    d = v.get("disallowed_after")
    if not d or v["status"] in ("approved", "out-of-scope", "review", "unknown"):
        return "none"
    day = dt.date.fromisoformat(d)
    if day < as_of:
        return "now"
    if day <= dt.date(2030, 12, 31):
        return "by-2030"
    if day <= dt.date(2033, 12, 31):
        return "2031-2033"
    if day <= dt.date(2035, 12, 31):
        return "2034-2035"
    return "none"
