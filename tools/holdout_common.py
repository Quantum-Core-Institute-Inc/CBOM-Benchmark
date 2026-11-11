"""Helpers shared by the holdout generators (holdout.py, holdout_langs.py, holdout_t3.py, holdout_deps.py)."""
from __future__ import annotations

import pyreq  # noqa: F401  (fails early on an unsupported Python)
import random
import re

WORDS = ["ledger", "invoice", "session", "payload", "record", "batch", "export", "audit", "tenant", "order",
         "report", "upload", "account", "profile", "metric", "event", "receipt", "archive", "partner",
         "shipment", "billing", "catalog", "voucher", "claim", "booking", "device", "member", "policy"]
VERBS = ["build", "make", "prepare", "load", "create", "derive", "compute", "pack", "seal", "stamp", "issue",
         "render", "collect", "assemble", "process", "emit"]
DOCS = ["Nightly {w} export job.", "Helpers for the {w} service.", "{W} pipeline step.", "Internal {w} utilities.",
        "Batch worker for {w} records.", "{W} sync task."]


class Names:
    def __init__(self, rng: random.Random):
        self.rng, self.used = rng, set()

    def _fresh(self, make):
        for _ in range(200):
            n = make()
            if n not in self.used:
                self.used.add(n)
                return n
        raise RuntimeError("name space exhausted")

    def snake(self):
        return self._fresh(lambda: f"{self.rng.choice(VERBS)}_{self.rng.choice(WORDS)}")

    def var(self):
        return self._fresh(lambda: f"{self.rng.choice(WORDS)}_{self.rng.choice(['out', 'blob', 'val', 'res', 'buf', 'obj'])}")

    def alias(self):
        return self._fresh(lambda: f"_{self.rng.choice(WORDS)[:4]}{self.rng.randint(1, 9)}")

    def const(self):
        return self._fresh(lambda: f"{self.rng.choice(WORDS).upper()}_{self.rng.choice(['MODE', 'PROFILE', 'SETTING', 'KIND', 'LEVEL', 'SPEC'])}")

    def cap(self):
        return self._fresh(lambda: f"{self.rng.choice(WORDS).capitalize()}{self.rng.choice(['Settings', 'Profile', 'Config', 'Defaults', 'Options'])}")

    def camel(self):
        return self._fresh(lambda: f"{self.rng.choice(VERBS)}{self.rng.choice(WORDS).capitalize()}")

    def key(self):
        return self._fresh(lambda: f"{self.rng.choice(WORDS)}_{self.rng.choice(['algo', 'kind', 'mode', 'size', 'spec', 'setting'])}")


def spec(family, params, body, ret, slot=None, kind="expr", also_ok=(), api="", carries_family=False, **extra):
    """carries_family: the slot names the algorithm (hiding it hides the family), not just a parameter."""
    return {"family": family, "params": params, "body": body, "ret": ret, "slot": slot, "kind": kind,
            "also_ok": list(also_ok), "api": api, "carries_family": carries_family, **extra}


def sub(text: str, m: dict) -> str:
    return re.sub(r"<<(\w+)>>", lambda mo: m[mo.group(1)], text)


