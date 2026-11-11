"""Run an untrusted command (a scanner, a BYOC case) in a restricted process.

What it guarantees, on every platform:
  * a scrubbed environment: PATH, HOME, TMPDIR and LANG, plus only the variables you name. The
    holdout seed is never passed, even if named.
  * inputs are private copies inside a fresh work directory, hashed before and after; a run that
    changed its inputs is reported as tampered.
  * wall-clock, CPU, address-space, file-size and core-dump limits (POSIX rlimits), and the whole
    process group is killed on timeout.
  * exit status, signal, wall time, CPU time and peak memory, from wait4().

What it adds on Linux when the kernel allows it (`unshare`, as root or with user namespaces):
  * no network: a fresh network namespace with only a down loopback.
  * read-only inputs: each input directory is bind-mounted read-only inside a private mount namespace.
  * a filesystem boundary: /home, /root, /tmp, /var/tmp, /mnt, /srv, /media and /run, plus any path
    the caller names (the testbench tree with its answer key, a holdout set), are replaced by empty
    tmpfs mounts. What stays visible under them is an allowlist: the work directory, the directories
    on PATH that hold the scanner and its interpreters, and paths the caller explicitly allows.
    System directories (/usr, /etc, /opt, ...) stay readable; the scanner needs them to run.

Whatever couldn't be applied is recorded in `isolation`, and `require=True` turns a missing guard
into an error instead of a note. In the container image (Dockerfile) run with `--network none` and
the network guard is met by the container itself.
"""
from __future__ import annotations

import hashlib
import os
import resource
import shlex
import shutil
import signal
import subprocess
import tempfile
import threading
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path

SEED_VARS = {"CBOM_HOLDOUT_SEED"}
DEFAULT_PATH = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"


@dataclass
class Limits:
    wall_s: int = 1800
    cpu_s: int | None = None          # None: no CPU limit beyond wall time
    mem_mb: int | None = 32768        # address space; generous because JVMs and V8 reserve a lot
    fsize_mb: int = 4096              # largest file the command may write
    network: bool = False             # True: leave the network alone


@dataclass
class Result:
    cmd: list
    exit_code: int | None
    signal: int | None
    timed_out: bool
    wall_s: float
    cpu_user_s: float
    cpu_sys_s: float
    peak_rss_mb: float | None
    isolation: dict
    tampered: list
    work: str
    out: str
    stdout: str
    stderr: str
    limits: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.exit_code is not None and not self.timed_out and not self.tampered

    def record(self) -> dict:
        """What goes into an evidence bundle (no host paths, no output text)."""
        d = asdict(self)
        for k in ("work", "out", "stdout", "stderr"):
            d.pop(k)
        d["cmd"] = [Path(c).name if os.path.isabs(c) else c for c in self.cmd]
        return d


def tree_sha(root: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if p.is_file() and not p.is_symlink():
            h.update(str(p.relative_to(root)).encode() + b"\0" + hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()


def no_network_interfaces() -> bool:
    """True when the only interface is loopback, as in a container started with --network none."""
    try:
        return set(os.listdir("/sys/class/net")) <= {"lo"}
    except OSError:
        return False


DEFAULT_HIDDEN = ("/home", "/root", "/tmp", "/var/tmp", "/mnt", "/srv", "/media", "/run")


def _under(p: str, root: str) -> bool:
    return p == root or p.startswith(root.rstrip("/") + "/")


def _outermost(paths, files: bool = False) -> list[str]:
    out = []
    for p in sorted({os.path.realpath(x) for x in paths if x and (os.path.isdir(x) or (files and os.path.isfile(x)))}, key=len):
        if not any(_under(p, q) for q in out):
            out.append(p)
    return out


def _install_root(d: str) -> str:
    """The directory to keep visible for a PATH entry: a venv or toolchain root, or a node project."""
    p = Path(os.path.realpath(d))
    if "node_modules" in p.parts:
        return str(Path(*p.parts[:p.parts.index("node_modules")]))
    return str(p.parent if p.name in ("bin", ".bin", "sbin", "Scripts") else p)


def confine_script(hidden: list[str], allowed: list[str], stage: str) -> str:
    """Shell that hides `hidden` behind empty tmpfs mounts and puts `allowed` (dirs or files) back."""
    q = shlex.quote
    keep = [a for a in _outermost(allowed, files=True) if any(_under(a, h) for h in hidden)]
    mk = lambda path, a: (f"mkdir -p {q(path)}" if os.path.isdir(a) else  # noqa: E731
                          f"mkdir -p {q(os.path.dirname(path))} && touch {q(path)}")
    lines = [f"mount -t tmpfs -o size=16m tmpfs {q(stage)}"]
    lines += [f"{mk(f'{stage}/k{i}', a)} && mount --rbind {q(a)} {q(stage)}/k{i}" for i, a in enumerate(keep)]
    lines += [f"mount -t tmpfs -o size=256m,mode=1777 tmpfs {q(h)}" for h in hidden if h != stage]
    lines += [f"{mk(a, a)} && mount --move {q(stage)}/k{i} {q(a)}" for i, a in enumerate(keep)]
    return " && ".join(lines)


STAGE_DIRS = ("/mnt", "/media", "/srv", "/run", "/var/tmp", "/home")


def pick_stage(visible: list[str]) -> str | None:
    """A hidden location to stage the visible paths in while everything else is covered: it must
    exist and must not itself contain anything that has to stay visible."""
    real = [os.path.realpath(v) for v in visible]
    return next((d for d in STAGE_DIRS if os.path.isdir(d) and not any(_under(v, os.path.realpath(d)) for v in real)), None)


_PROBE: dict = {}


def probe() -> dict:
    """Which Linux guards this host can apply. Cached."""
    if _PROBE:
        return _PROBE
    us = shutil.which("unshare")
    net = ro = False
    if us:
        base = [us, "--net", "--mount", "--fork", "--kill-child"] + ([] if os.geteuid() == 0 else ["--map-root-user"])
        try:
            net = subprocess.run(base + ["true"], capture_output=True, timeout=10).returncode == 0
            if net:
                d = tempfile.mkdtemp(prefix="cbom-probe-")
                script = (f"mount --bind {shlex.quote(d)} {shlex.quote(d)} && mount -o remount,bind,ro {shlex.quote(d)} "
                          f"&& ! touch {shlex.quote(d)}/x 2>/dev/null")
                ro = subprocess.run(base + ["sh", "-c", script], capture_output=True, timeout=10).returncode == 0
                shutil.rmtree(d, ignore_errors=True)
        except (OSError, subprocess.TimeoutExpired):
            pass
    confine = False
    d = tempfile.mkdtemp(prefix="cbom-probe-")
    stage = pick_stage([d])
    if not (ro and stage):
        shutil.rmtree(d, ignore_errors=True)
    else:
        (Path(d) / "marker").write_text("x")
        hidden = _outermost(DEFAULT_HIDDEN)
        script = confine_script(hidden, [d], stage) + f" && test -f {shlex.quote(d)}/marker"
        try:
            confine = subprocess.run(base + ["sh", "-c", script], capture_output=True, timeout=20).returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            pass
        shutil.rmtree(d, ignore_errors=True)
    _PROBE.update({"unshare": us, "base": base if us else None, "network": net, "readonly": ro,
                   "confine": confine, "stage": stage})
    return _PROBE


def _preexec(lim: Limits):
    def fn():
        os.setsid()
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        if lim.mem_mb:
            b = lim.mem_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (b, b))
        if lim.cpu_s:
            resource.setrlimit(resource.RLIMIT_CPU, (lim.cpu_s, lim.cpu_s + 5))
        if lim.fsize_mb:
            b = lim.fsize_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_FSIZE, (b, b))
    return fn


def run(cmd: list[str], inputs: dict[str, Path] | None = None, limits: Limits | None = None,
        pass_env: tuple[str, ...] = (), extra_path: tuple[str, ...] = (), require: bool = False,
        cwd_input: str | None = None, keep: bool = True, set_env: dict | None = None,
        hide: tuple = (), allow: tuple = (), require_confine: bool = False, image: str | None = None) -> Result:
    """Run `cmd` with {name} placeholders filled: each input name -> its private copy, {out} -> the
    output directory, {work} -> the work directory. `cwd_input` runs inside that input's copy."""
    lim = limits or Limits()
    inputs = inputs or {}
    work = Path(tempfile.mkdtemp(prefix="cbom-sandbox-"))
    out = work / "out"
    out.mkdir()
    (work / ".home").mkdir()
    (work / ".tmp").mkdir()
    copies = {}
    for name, src in inputs.items():
        dst = work / name
        if Path(src).is_dir():
            shutil.copytree(src, dst, symlinks=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        copies[name] = dst
    before = {n: (tree_sha(p) if p.is_dir() else hashlib.sha256(p.read_bytes()).hexdigest()) for n, p in copies.items()}

    if image:
        return _run_in_container(image, cmd, copies, before, work, out, lim, pass_env, set_env, cwd_input, keep)
    fill = {**{n: str(p) for n, p in copies.items()}, "out": str(out), "work": str(work)}
    argv = [c.format(**fill) for c in cmd]

    leaked = [v for v in pass_env if v in SEED_VARS]
    # PATH is passed through (it locates interpreters; it isn't a credential). Nothing else is.
    env = {"PATH": ":".join([*extra_path, os.environ.get("PATH", ""), DEFAULT_PATH]), "HOME": str(work / ".home"),
           "TMPDIR": str(work / ".tmp"), "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    env.update({k: os.environ[k] for k in pass_env if k in os.environ and k not in SEED_VARS})
    env.update({k: v for k, v in (set_env or {}).items() if k not in SEED_VARS})

    pr = probe()
    isolation = {"environment": "scrubbed", "seed_withheld": True, "inputs_hashed": True,
                 "rlimits": True, "network": "not isolated", "inputs_readonly": "copy only"}
    if leaked:
        isolation["refused_env"] = leaked
    if no_network_interfaces():  # e.g. the container image run with --network none
        isolation["network"] = "no network interfaces on this host (container --network none)"
    wrap = []
    isolation["filesystem"] = "not confined"
    if pr["network"] or pr["readonly"]:
        base = [x for x in pr["base"] if not (x == "--net" and lim.network)]
        script = []
        if pr["network"] and not lim.network:
            isolation["network"] = "isolated (network namespace)"
        stage = None
        if pr.get("confine"):
            hidden = _outermost([*DEFAULT_HIDDEN, *map(str, hide)])
            visible = [str(work)] + [_install_root(d) for d in env["PATH"].split(":") if d and os.path.isdir(d)] \
                      + [str(x) for x in allow]
            stage = pick_stage(visible)
        if stage:
            script.append(confine_script(hidden, visible, stage))
            isolation["filesystem"] = (f"confined: {len(hidden)} location(s) hidden behind empty mounts"
                                       + (f", {len(allow)} path(s) allowed back by the caller" if allow else ""))
            isolation["hidden_caller_paths"] = len(hide)
        if pr["readonly"] and copies:
            ro = [f"mount --bind {shlex.quote(str(p))} {shlex.quote(str(p))} && "
                  f"mount -o remount,bind,ro {shlex.quote(str(p))}" for p in copies.values() if p.is_dir()]
            if ro:
                script += ro
                isolation["inputs_readonly"] = "read-only bind mount"
        if script or (pr["network"] and not lim.network):
            wrap = base + (["sh", "-c", " && ".join(script) + ' && exec "$@"', "sandbox"] if script else [])
    if lim.network:
        isolation["network"] = "allowed (requested)"
    if require_confine and not isolation["filesystem"].startswith("confined"):
        shutil.rmtree(work, ignore_errors=True)
        raise RuntimeError("sandbox: a filesystem boundary was required and this host can't make one (no mount "
                           "namespace). In a container, add --cap-add SYS_ADMIN, or run the scanner in its own "
                           "container with only the corpus and the output directory mounted.")
    if require:
        missing = [k for k in ("network",) if not lim.network and isolation[k] == "not isolated"]
        if missing:
            shutil.rmtree(work, ignore_errors=True)
            raise RuntimeError(f"sandbox: required isolation not available on this host: {', '.join(missing)} "
                               "(run inside the container with --network none, or as a user who can unshare)")

    so, se = open(work / ".stdout", "w+b"), open(work / ".stderr", "w+b")
    t0 = time.monotonic()
    cwd = str(copies[cwd_input]) if cwd_input else str(work)
    try:
        proc = subprocess.Popen(wrap + argv, cwd=cwd, env=env, stdout=so, stderr=se, stdin=subprocess.DEVNULL,
                                preexec_fn=_preexec(lim))
    except OSError as e:
        so.close(); se.close()  # noqa: E702
        return Result(argv, None, None, False, 0.0, 0.0, 0.0, 0.0, isolation, [], str(work), str(out), "", str(e),
                      asdict(lim))
    timed_out = threading.Event()

    def kill():
        timed_out.set()
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    timer = threading.Timer(lim.wall_s, kill)
    timer.start()
    _, status, ru = os.wait4(proc.pid, 0)
    timer.cancel()
    proc.returncode = os.waitstatus_to_exitcode(status)
    wall = time.monotonic() - t0
    try:  # leftovers in the group (daemons the scanner forked) go too
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    so.seek(0); se.seek(0)  # noqa: E702
    stdout, stderr = so.read().decode(errors="replace"), se.read().decode(errors="replace")
    so.close(); se.close()  # noqa: E702

    after = {n: (tree_sha(p) if p.is_dir() else hashlib.sha256(p.read_bytes()).hexdigest()) if p.exists() else "gone"
             for n, p in copies.items()}
    code = proc.returncode
    res = Result(argv, code if code >= 0 else None, -code if code < 0 else None, timed_out.is_set(), round(wall, 2),
                 round(ru.ru_utime, 2), round(ru.ru_stime, 2), round(ru.ru_maxrss / 1024, 1), isolation,
                 [n for n in copies if before[n] != after[n]], str(work), str(out), stdout, stderr, asdict(lim))
    if not keep:
        shutil.rmtree(work, ignore_errors=True)
    return res


def _cgroup_file(cid: str, *names: str) -> Path | None:
    """A container's cgroup counter, on cgroup v2 (memory.peak) or v1 (memory.max_usage_in_bytes)."""
    import glob
    for name in names:
        for pat in (f"/sys/fs/cgroup/system.slice/docker-{cid}.scope/{name}", f"/sys/fs/cgroup/docker/{cid}/{name}",
                    f"/sys/fs/cgroup/*/docker/{cid}/{name}"):
            hits = glob.glob(pat)
            if hits:
                return Path(hits[0])
    return None


def _run_in_container(image, cmd, copies, before, work, out, lim, pass_env, set_env, cwd_input, keep) -> Result:
    """The strongest lane: the scanner runs in its own container. It sees its own image, a read-only
    mount of each input, a writable output directory and a private /tmp. Nothing of the host, the
    testbench or the evaluator exists inside it; there is no network, no capability, no new privilege."""
    docker = shutil.which("docker")
    if not docker:
        shutil.rmtree(work, ignore_errors=True)
        raise RuntimeError("sandbox: --scanner-image needs docker on PATH")
    fill = {**{n: f"/in/{n}" for n in copies}, "out": "/out", "work": "/tmp"}
    argv = [c.format(**fill) for c in cmd]
    img = subprocess.run([docker, "image", "inspect", "-f", "{{.Id}}", image], capture_output=True, text=True)
    if img.returncode:
        shutil.rmtree(work, ignore_errors=True)
        raise RuntimeError(f"sandbox: image {image!r} is not available locally: {img.stderr.strip()[-200:]}")
    os.chmod(out, 0o777)
    env = {"HOME": "/tmp", "TMPDIR": "/tmp", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    env.update({k: os.environ[k] for k in pass_env if k in os.environ and k not in SEED_VARS})
    env.update({k: v for k, v in (set_env or {}).items() if k not in SEED_VARS})
    name = f"cbom-scan-{os.getpid()}-{int(time.time() * 1000) % 10 ** 9}"
    args = [docker, "create", "--name", name, "--network", "none", "--read-only", "--tmpfs", "/tmp:rw,exec,size=1g,mode=1777",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges", "--pids-limit", "1024",
            "--user", f"{os.getuid()}:{os.getgid()}", "--workdir", f"/in/{cwd_input}" if cwd_input else "/tmp",
            "-v", f"{out}:/out"]
    if lim.mem_mb:
        args += ["--memory", f"{lim.mem_mb}m", "--memory-swap", f"{lim.mem_mb}m"]
    for n, p in copies.items():
        args += ["-v", f"{p}:/in/{n}:ro"]
    for k, v in env.items():
        args += ["-e", f"{k}={v}"]
    args += ["--entrypoint", argv[0], image, *argv[1:]]
    isolation = {"environment": "scrubbed", "seed_withheld": True, "inputs_hashed": True, "rlimits": "container limits",
                 "network": "isolated (container, --network none)", "inputs_readonly": "read-only mount",
                 "filesystem": "confined: own container; only the inputs (read-only) and the output directory are mounted",
                 "container_image": img.stdout.strip(), "capabilities": "none"}
    c = subprocess.run(args, capture_output=True, text=True)
    if c.returncode:
        shutil.rmtree(work, ignore_errors=True)
        raise RuntimeError(f"sandbox: docker create failed: {c.stderr.strip()[-300:]}")
    cid = c.stdout.strip()
    peak = {"mem": None, "cpu": None}
    stop = threading.Event()

    def poll():
        while not stop.is_set():
            for key, fnames in (("mem", ("memory.peak", "memory.max_usage_in_bytes")), ("cpu", ("cpu.stat",))):
                f = _cgroup_file(cid, *fnames)
                try:
                    if f and key == "mem":
                        peak["mem"] = max(peak["mem"] or 0, int(f.read_text()))
                    elif f:
                        got = {ln.split()[0]: int(ln.split()[1]) for ln in f.read_text().splitlines()}
                        if "user_usec" in got:
                            peak["cpu"] = got
                except (OSError, ValueError):
                    pass
            stop.wait(0.05)
    t0 = time.monotonic()
    so, se = open(work / ".stdout", "w+b"), open(work / ".stderr", "w+b")
    proc = subprocess.Popen([docker, "start", "-a", cid], stdout=so, stderr=se, stdin=subprocess.DEVNULL)
    th = threading.Thread(target=poll, daemon=True)
    th.start()
    timed_out = False
    try:
        proc.wait(timeout=lim.wall_s)
    except subprocess.TimeoutExpired:
        timed_out = True
        subprocess.run([docker, "kill", cid], capture_output=True)
        proc.wait()
    wall = time.monotonic() - t0
    stop.set()
    th.join(timeout=2)
    insp = subprocess.run([docker, "inspect", "-f", "{{.State.ExitCode}} {{.State.OOMKilled}}", cid], capture_output=True, text=True)
    subprocess.run([docker, "rm", "-f", cid], capture_output=True)
    code, oom = (insp.stdout.split() + ["", ""])[:2] if insp.returncode == 0 else (str(proc.returncode), "false")
    so.seek(0); se.seek(0)  # noqa: E702
    stdout, stderr = so.read().decode(errors="replace"), se.read().decode(errors="replace")
    so.close(); se.close()  # noqa: E702
    after = {n: (tree_sha(p) if p.is_dir() else hashlib.sha256(p.read_bytes()).hexdigest()) if p.exists() else "gone"
             for n, p in copies.items()}
    if oom == "true":
        isolation["oom_killed"] = True
    cpu = peak["cpu"] or {}
    code = int(code) if str(code).lstrip("-").isdigit() else None
    res = Result(argv, None if timed_out else code, 9 if timed_out or oom == "true" else None, timed_out, round(wall, 2),
                 round(cpu.get("user_usec", 0) / 1e6, 2), round(cpu.get("system_usec", 0) / 1e6, 2),
                 round(peak["mem"] / 1048576, 1) if peak["mem"] else None, isolation,
                 [n for n in copies if before[n] != after[n]], str(work), str(out), stdout, stderr, asdict(lim))
    if not keep:
        shutil.rmtree(work, ignore_errors=True)
    return res


def cleanup(res: Result) -> None:
    shutil.rmtree(res.work, ignore_errors=True)
