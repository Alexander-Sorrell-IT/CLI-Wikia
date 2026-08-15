"""wikia daemon — run wikia update --all on the configured schedule interval.

Commands:
  wikia daemon start    # daemonize and start polling
  wikia daemon stop     # send SIGTERM to the running daemon
  wikia daemon status   # show whether the daemon is running + last run time
  wikia daemon logs     # tail the daemon log (last N lines)

The daemon reads the same config as `wikia schedule` (interval/upgrade/enabled).
It replaces the need for systemd/launchd — a pure-Python background process that
survives terminal exit and restarts cleanly.
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time

from . import __version__
from .schedule import load_config, _INTERVAL_SECONDS, snapshot_dir


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

def _state_dir() -> str:
    base = os.environ.get("XDG_STATE_HOME") or os.path.join(
        os.path.expanduser("~"), ".local", "state"
    )
    return os.path.join(base, "cli-wikia")


def _pid_path() -> str:
    return os.path.join(_state_dir(), "daemon.pid")


def _log_path() -> str:
    return os.path.join(_state_dir(), "daemon.log")


# ---------------------------------------------------------------------------
# PID helpers
# ---------------------------------------------------------------------------

def _read_pid() -> int | None:
    p = _pid_path()
    try:
        return int(open(p).read().strip())
    except (OSError, ValueError):
        return None


def _is_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _write_pid(pid: int) -> None:
    os.makedirs(_state_dir(), exist_ok=True)
    with open(_pid_path(), "w") as f:
        f.write(str(pid))


def _clear_pid() -> None:
    try:
        os.remove(_pid_path())
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Daemonize (double-fork, POSIX)
# ---------------------------------------------------------------------------

def _daemonize(log_path: str) -> None:
    """Detach from the terminal using the double-fork technique."""
    # First fork
    if os.fork() > 0:
        sys.exit(0)
    os.setsid()
    # Second fork — prevent reacquiring a terminal
    if os.fork() > 0:
        sys.exit(0)
    # Redirect stdio to /dev/null (log goes to file via _log())
    devnull = open(os.devnull, "r")
    os.dup2(devnull.fileno(), sys.stdin.fileno())
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logfile = open(log_path, "a", buffering=1)
    os.dup2(logfile.fileno(), sys.stdout.fileno())
    os.dup2(logfile.fileno(), sys.stderr.fileno())


# ---------------------------------------------------------------------------
# Logging inside the daemon
# ---------------------------------------------------------------------------

def _log(msg: str) -> None:
    ts = time.strftime("%Y-%m-%dT%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


# ---------------------------------------------------------------------------
# Main daemon loop
# ---------------------------------------------------------------------------

def _run_update(upgrade: bool) -> bool:
    """Run wikia update --all --write. Returns True on success."""
    wikia = sys.argv[0]  # the running wikia binary
    cmd = [wikia, "update", "--all", "--write", "--no-model"]
    if upgrade:
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", "cli-wikia"],
                timeout=120,
            )
        except Exception as e:
            _log(f"pip upgrade failed (continuing): {e}")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        for line in (r.stdout + r.stderr).splitlines():
            if line.strip():
                _log(f"  {line}")
        return r.returncode == 0
    except Exception as e:
        _log(f"update error: {e}")
        return False


def _daemon_loop() -> None:
    cfg = load_config().get("schedule", {})
    interval_name = cfg.get("interval", "daily")
    upgrade = bool(cfg.get("upgrade", True))
    interval_secs = _INTERVAL_SECONDS.get(interval_name, 86400)

    _log(f"wikia daemon v{__version__} started — interval={interval_name} ({interval_secs}s), upgrade={upgrade}")
    _write_pid(os.getpid())

    def _handle_term(sig, frame):
        _log("daemon stopping (SIGTERM).")
        _clear_pid()
        sys.exit(0)

    signal.signal(signal.SIGTERM, _handle_term)
    signal.signal(signal.SIGINT, _handle_term)

    next_run = time.time()  # run immediately on first start
    while True:
        now = time.time()
        if now >= next_run:
            _log(f"running: wikia update --all --write")
            ok = _run_update(upgrade)
            _log(f"update {'ok' if ok else 'FAILED'}")
            next_run = time.time() + interval_secs
            _log(f"next run in {interval_secs}s ({time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(next_run))})")
        time.sleep(30)  # check every 30s so SIGTERM is responsive


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_start(args):
    pid = _read_pid()
    if pid and _is_alive(pid):
        print(f"wikia daemon already running (pid {pid}). Use `wikia daemon stop` first.")
        return

    cfg = load_config().get("schedule", {})
    interval = cfg.get("interval", "daily")
    upgrade = cfg.get("upgrade", True)
    log = _log_path()

    if not args.foreground:
        _daemonize(log)
        _daemon_loop()
    else:
        print(f"wikia daemon starting (foreground) — interval={interval}, upgrade={upgrade}")
        print(f"log: {log}  (Ctrl-C to stop)")
        _write_pid(os.getpid())
        try:
            _daemon_loop()
        except KeyboardInterrupt:
            _clear_pid()
            print("\ndaemon stopped.")


def cmd_stop(args):
    pid = _read_pid()
    if not pid:
        print("wikia daemon is not running (no pid file).")
        return
    if not _is_alive(pid):
        print(f"wikia daemon pid {pid} is not alive — clearing stale pid file.")
        _clear_pid()
        return
    os.kill(pid, signal.SIGTERM)
    # Wait up to 5s for it to exit
    for _ in range(50):
        time.sleep(0.1)
        if not _is_alive(pid):
            break
    _clear_pid()
    print(f"wikia daemon (pid {pid}) stopped.")


def cmd_status(args):
    pid = _read_pid()
    log = _log_path()
    if pid and _is_alive(pid):
        print(f"wikia daemon: RUNNING  (pid {pid})")
    elif pid:
        print(f"wikia daemon: DEAD  (stale pid {pid} — run `wikia daemon stop` to clean up)")
    else:
        print("wikia daemon: STOPPED")
    print(f"log: {log}" + ("" if os.path.exists(log) else "  (no log yet)"))
    cfg = load_config().get("schedule", {})
    print(f"config: interval={cfg.get('interval','daily')}  upgrade={cfg.get('upgrade',True)}")
    # Show last run from log tail
    if os.path.exists(log):
        lines = open(log).readlines()
        last_run = next((l.rstrip() for l in reversed(lines) if "running:" in l or "update ok" in l or "update FAILED" in l), None)
        if last_run:
            print(f"last: {last_run.strip()}")


def cmd_logs(args):
    log = _log_path()
    if not os.path.exists(log):
        print(f"no log file yet: {log}")
        return
    lines = open(log).readlines()
    n = getattr(args, "lines", 40)
    for line in lines[-n:]:
        print(line, end="")
