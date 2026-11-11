#!/usr/bin/env python3
"""The secure lane: what an untrusted scanner or BYOC command can and can't reach.

Network isolation must come from somewhere: a network namespace (unshare) or a host with no
interfaces (the container run with --network none). If neither, that check is skipped and
`--strict` fails. Without a mount namespace the corpus copy is writable, and the check becomes
"tampering is detected", which is the guarantee bench.py relies on there.

Run: python tools/test_sandbox.py [--strict]
"""
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sandbox  # noqa: E402

PY = sys.executable
skips = 0


def check(name, cond):
    print(f"[{'ok ' if cond else 'FAIL'}] {name}")
    return bool(cond)


def skip(name, why):
    global skips
    skips += 1
    print(f"[skip] {name}: {why}")
    return True


def main() -> int:
    ok = True
    pr = sandbox.probe()
    src = Path(tempfile.mkdtemp(prefix="sbx-test-"))
    (src / "a.py").write_text("import hashlib\nhashlib.md5(b'x')\n")

    os.environ["CBOM_HOLDOUT_SEED"] = "424242"
    os.environ["GITHUB_TOKEN"] = "ghp_should_not_leak"
    r = sandbox.run([PY, "-c", "import os, json; print(json.dumps(dict(os.environ)))"], {"corpus": src},
                    pass_env=("CBOM_HOLDOUT_SEED",))
    import json
    env = json.loads(r.stdout)
    ok &= check("holdout seed never reaches the command, even when named in pass_env",
                "CBOM_HOLDOUT_SEED" not in env and r.isolation.get("refused_env") == ["CBOM_HOLDOUT_SEED"])
    ok &= check("credentials in the parent environment are not inherited", "GITHUB_TOKEN" not in env)
    ok &= check("HOME and TMPDIR point inside the work directory",
                env["HOME"].startswith(r.work) and env["TMPDIR"].startswith(r.work))
    sandbox.cleanup(r)

    r = sandbox.run([PY, "-c", "open('{corpus}/a.py', 'a').write('# tampered\\n')"], {"corpus": src})
    if pr["readonly"]:
        ok &= check("writing to the corpus fails (read-only mount) and nothing changes",
                    r.exit_code != 0 and not r.tampered)
    else:
        # No mount namespace (e.g. an unprivileged container): the copy is writable, so tampering is
        # detected and the run isn't scored. That is the guarantee here, not a gap.
        ok &= check("writing to the corpus copy is detected as tampering (no mount namespace here)", r.tampered == ["corpus"])
    ok &= check("the original corpus is never touched", "tampered" not in (src / "a.py").read_text())
    sandbox.cleanup(r)

    r = sandbox.run([PY, "-c", "open('{out}/cbom.json', 'w').write('{{}}')"], {"corpus": src})
    ok &= check("the output directory is writable", r.exit_code == 0 and (Path(r.out) / "cbom.json").exists())
    sandbox.cleanup(r)

    net = "import socket; s=socket.socket(); s.settimeout(3); s.connect(('1.1.1.1', 443))"
    r = sandbox.run([PY, "-c", net], {"corpus": src})
    if pr["network"]:
        ok &= check("no network: an outbound connection fails", r.exit_code != 0
                    and r.isolation["network"].startswith("isolated"))
    elif sandbox.no_network_interfaces():
        ok &= check("no network (container --network none): an outbound connection fails and it's recorded",
                    r.exit_code != 0 and "network none" in r.isolation["network"])
    else:
        skip("network isolation", "this host can neither unshare a network namespace nor has --network none")
    sandbox.cleanup(r)
    if not pr["network"] and not sandbox.no_network_interfaces():
        try:
            sandbox.run([PY, "-c", "pass"], {"corpus": src}, require=True)
            ok &= check("require=True refuses to run without network isolation", False)
        except RuntimeError:
            ok &= check("require=True refuses to run without network isolation", True)

    r = sandbox.run([PY, "-c", "import time; time.sleep(30)"], limits=sandbox.Limits(wall_s=2))
    ok &= check("wall-clock limit kills the run and says so", r.timed_out and r.wall_s < 10)
    sandbox.cleanup(r)

    r = sandbox.run([PY, "-c", "b = bytearray(600 * 1024 * 1024)"], limits=sandbox.Limits(mem_mb=300))
    ok &= check("memory limit stops a 600 MB allocation under a 300 MB cap", r.exit_code != 0)
    sandbox.cleanup(r)

    r = sandbox.run([PY, "-c", "b = bytearray(200 * 1024 * 1024); b[::4096] = b'x' * len(b[::4096])"])
    ok &= check(f"peak memory is measured (200 MB touched -> {r.peak_rss_mb} MB)", 180 <= r.peak_rss_mb <= 400)
    rec = r.record()
    ok &= check("the bundle record carries no host paths or output text",
                not any(k in rec for k in ("work", "out", "stdout", "stderr")) and "exit_code" in rec)
    sandbox.cleanup(r)

    # Filesystem boundary (v2.1 review): the answer key, the user's home and other temp files are
    # not there to read; the scanner's own input and toolchain are.
    root = Path(__file__).resolve().parent.parent
    other = Path(tempfile.mkdtemp(prefix="evaluator-side-"))
    (other / "truth.json").write_text("{}")
    probe_src = ("import os, sys, json\n"
                 "def can(p):\n"
                 "    try:\n        os.listdir(p) if os.path.isdir(p) else open(p, 'rb').read(8)\n        return True\n"
                 "    except OSError:\n        return False\n"
                 "print(json.dumps([can(p) for p in sys.argv[1:]]))\n")
    r = sandbox.run([PY, "-c", probe_src, str(root / "expected" / "ground_truth.json"), str(root / "evidence"),
                     str(other / "truth.json"), str(Path.home()), "{corpus}/a.py"], {"corpus": src}, hide=(str(root),))
    if pr.get("confine"):
        got = json.loads(r.stdout)
        ok &= check("the answer key and evidence are not readable from inside", got[:2] == [False, False])
        ok &= check("an evaluator-side temp directory (a holdout set) is not readable", got[2] is False)
        ok &= check("the scanner's own input is readable, and the run says it was confined",
                    got[4] is True and r.isolation["filesystem"].startswith("confined"))
        r2 = sandbox.run([PY, "-c", probe_src, str(root / "tools" / "cbomlib.py"), str(root / "expected" / "ground_truth.json")],
                         hide=(str(root),), allow=(str(root / "tools"),))
        ok &= check("a path allowed back by the caller is readable; its hidden siblings are not", json.loads(r2.stdout) == [True, False])
        sandbox.cleanup(r2)
    else:
        skip("filesystem boundary", "this host can't make a mount namespace")
        try:
            sandbox.run([PY, "-c", "pass"], require_confine=True)
            ok &= check("require_confine refuses to run without a boundary", False)
        except RuntimeError:
            ok &= check("require_confine refuses to run without a boundary", True)
    sandbox.cleanup(r)

    # The container lane (bench.py --scanner-image): the scanner in its own container. Needs docker and
    # a local image with python3 in it, named in CBOM_TEST_SCANNER_IMAGE; CI pulls one. Not counted as
    # a skip when absent: it's a second lane, and the checks above cover the first.
    img = os.environ.get("CBOM_TEST_SCANNER_IMAGE")
    if img and shutil.which("docker"):
        code = ("import os, json, socket\n"
                "def net():\n"
                "    try:\n        socket.create_connection(('1.1.1.1', 443), 3); return True\n"
                "    except OSError:\n        return False\n"
                "def wr(p):\n"
                "    try:\n        open(p, 'a').write('x'); return True\n"
                "    except OSError:\n        return False\n"
                f"print(json.dumps([os.path.exists({str(root)!r}), os.path.exists({str(Path.home())!r}) and bool(os.listdir({str(Path.home())!r})), "
                "os.path.exists('/in/corpus/a.py'), wr('/in/corpus/a.py'), wr('/out/cbom.json'), net(), "
                "sorted(k for k in os.environ if 'SEED' in k or 'TOKEN' in k)]))\n")
        r = sandbox.run(["python3", "-c", code], {"corpus": src}, image=img, pass_env=("CBOM_HOLDOUT_SEED",))
        got = json.loads(r.stdout) if r.stdout.strip() else None
        ok &= check("container lane: no testbench tree, no home contents, no network, no seed or token; corpus readable but "
                    "not writable; output writable", got == [False, False, True, False, True, False, []])
        ok &= check("container lane: recorded as its own container with no capabilities, input untouched",
                    r.isolation["filesystem"].startswith("confined: own container") and r.isolation["capabilities"] == "none"
                    and not r.tampered and (Path(r.out) / "cbom.json").exists())
        sandbox.cleanup(r)
        r = sandbox.run(["python3", "-c", "import time; time.sleep(60)"], image=img, limits=sandbox.Limits(wall_s=3))
        ok &= check("container lane: the wall-clock limit kills the container", r.timed_out and r.wall_s < 20)
        sandbox.cleanup(r)
    else:
        print("[note] container lane not exercised (set CBOM_TEST_SCANNER_IMAGE to a local image with python3)")

    # The fallback on a host with no namespaces: tampering is still caught, and require=True refuses.
    saved = dict(sandbox._PROBE)
    sandbox._PROBE.update({"network": False, "readonly": False, "confine": False})
    real_nni = sandbox.no_network_interfaces
    sandbox.no_network_interfaces = lambda: False
    r = sandbox.run([PY, "-c", "open('{corpus}/a.py', 'a').write('# tampered\\n')"], {"corpus": src})
    ok &= check("no namespaces: a write to the corpus copy is reported as tampering",
                r.tampered == ["corpus"] and r.isolation["network"] == "not isolated")
    sandbox.cleanup(r)
    try:
        sandbox.run([PY, "-c", "pass"], require=True)
        ok &= check("no namespaces: require=True refuses to run", False)
    except RuntimeError:
        ok &= check("no namespaces: require=True refuses to run", True)
    sandbox._PROBE.clear()
    sandbox._PROBE.update(saved)
    sandbox.no_network_interfaces = real_nni

    strict = "--strict" in sys.argv
    print(f"\nSandbox checks: {'all pass' if ok else 'FAILED'}"
          + (f" ({skips} skipped: host lacks a guard)" if skips else ""))
    return 0 if ok and not (strict and skips) else (4 if ok else 1)


if __name__ == "__main__":
    sys.exit(main())
