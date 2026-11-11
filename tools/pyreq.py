"""Fail early, with a clear message, on a Python the testbench doesn't support.

The tools use tomllib (3.11) and are tested on 3.11, 3.12 and 3.13. Imported first by the shared
modules (cbomlib, truth, release) and by the scripts that use neither.
"""
import sys

MIN = (3, 11)
if sys.version_info < MIN:
    sys.exit(f"CBOM Testbench needs Python {MIN[0]}.{MIN[1]} or later; this is {sys.version.split()[0]}. "
             "See README, Quick start.")
