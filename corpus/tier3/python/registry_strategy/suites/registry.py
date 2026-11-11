"""Name-to-class registry populated by decorators at import time."""

_SUITES = {}


def register(name):
    def deco(cls):
        _SUITES[name] = cls
        return cls
    return deco


def get(name):
    return _SUITES[name]()
