"""Scheduled auto-update for cli-wikia, driven by a config file.

The user edits a small JSON config (interval/upgrade/enabled), then `apply`
installs a systemd *user* timer that runs `wikia update --all` on that cadence.
`Persistent=true` means a run missed while the machine was off ("downtime")
fires on next boot.

Commands:
  wikia schedule config   # create/show the config file (pick your interval here)
  wikia schedule apply     # make the timer match the config (dry-run unless --write)
  wikia schedule status    # show config + installed timer
  wikia schedule remove    # remove the timer (dry-run unless --write)
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

INTERVALS = ("hourly", "daily", "weekly", "monthly")
UNIT_NAME = "cli-wikia-update"


def _config_dir():
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(
        os.path.expanduser("~"), ".config"
    )
    return os.path.join(base, "cli-wikia")


def config_path():
    return os.path.join(_config_dir(), "config.json")


def _unit_dir():
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(
        os.path.expanduser("~"), ".config"
    )
    return os.path.join(base, "systemd", "user")


def _log_path():
    base = os.environ.get("XDG_STATE_HOME") or os.path.join(
        os.path.expanduser("~"), ".local", "state"
    )
    return os.path.join(base, "cli-wikia", "update.log")


DEFAULT_CONFIG = {
    "schedule": {
        "enabled": False,
        "interval": "daily",
        "_interval_options": list(INTERVALS),
        "upgrade": True,
        "_help": "Set enabled=true, pick interval from _interval_options, then run `wikia schedule apply --write`.",
    }
}


def load_config():
    p = config_path()
    if not os.path.exists(p):
        return DEFAULT_CONFIG
    with open(p, encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------------------- #
# systemd unit text
# --------------------------------------------------------------------------- #
def _exec_command(upgrade):
    wikia = shutil.which("wikia") or "wikia"
    log = _log_path()
    parts = []
    if upgrade:
        parts.append(f"{sys.executable} -m pip install --quiet --upgrade cli-wikia")
    parts.append(f"{wikia} update --all --write")
    chain = " ; ".join(parts)
    return f"/bin/sh -c 'mkdir -p {os.path.dirname(log)} ; {{ date ; {chain} ; }} >> {log} 2>&1'"


def _service_unit(upgrade):
    return (
        "[Unit]\n"
        "Description=cli-wikia: refresh AI-CLI wikis and detect tool changes\n\n"
        "[Service]\nType=oneshot\n"
        f"ExecStart={_exec_command(upgrade)}\n"
    )


def _timer_unit(interval):
    return (
        f"[Unit]\nDescription=cli-wikia scheduled update ({interval})\n\n"
        f"[Timer]\nOnCalendar={interval}\nPersistent=true\n\n"
        "[Install]\nWantedBy=timers.target\n"
    )


def _systemctl(*a):
    return subprocess.run(["systemctl", "--user", *a], capture_output=True, text=True)


def _have_systemd_user():
    return bool(shutil.which("systemctl")) and _systemctl("show-environment").returncode == 0


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #
def cmd_config(args):
    """Create the config file (if missing) or show it."""
    p = config_path()
    if os.path.exists(p):
        print(f"# {p}")
        with open(p, encoding="utf-8") as f:
            print(f.read().rstrip())
        print("\nEdit this file, then: wikia schedule apply --write")
        return
    text = json.dumps(DEFAULT_CONFIG, indent=2)
    if not args.write:
        print(f"[dry-run] would create config at: {p}\n")
        print(text)
        print("\nre-run with --write to create it, then edit and `wikia schedule apply --write`.")
        return
    os.makedirs(_config_dir(), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print(f"created config: {p}")
    print("Edit `interval`/`upgrade`, set `enabled: true`, then: wikia schedule apply --write")


def cmd_apply(args):
    """Install or remove the timer so it matches the config file."""
    cfg = load_config().get("schedule", {})
    enabled = bool(cfg.get("enabled"))
    interval = cfg.get("interval", "daily")
    upgrade = bool(cfg.get("upgrade", True))
    if interval not in INTERVALS:
        sys.exit(f"config interval '{interval}' invalid; choose from: {', '.join(INTERVALS)}")

    udir = _unit_dir()
    svc = os.path.join(udir, f"{UNIT_NAME}.service")
    tmr = os.path.join(udir, f"{UNIT_NAME}.timer")

    if not enabled:
        if not args.write:
            print("[dry-run] config has enabled=false → would remove any installed timer (re-run with --write)")
            return
        _systemctl("disable", "--now", f"{UNIT_NAME}.timer")
        for q in (svc, tmr):
            if os.path.exists(q):
                os.remove(q)
        _systemctl("daemon-reload")
        print("schedule disabled (timer removed) per config.")
        return

    service_text = _service_unit(upgrade)
    timer_text = _timer_unit(interval)
    if not args.write:
        print(f"[dry-run] would install timer: interval={interval}, upgrade={upgrade}\n")
        print(f"# {svc}\n{service_text}")
        print(f"# {tmr}\n{timer_text}")
        print(f"log: {_log_path()}\n\nre-run with --write to install.")
        return
    if not _have_systemd_user():
        sys.exit(
            "systemd user instance unavailable. Cron fallback:\n"
            f"  (crontab -l 2>/dev/null; echo '@{interval} {shutil.which('wikia') or 'wikia'} update --all --write') | crontab -"
        )
    os.makedirs(udir, exist_ok=True)
    with open(svc, "w", encoding="utf-8") as f:
        f.write(service_text)
    with open(tmr, "w", encoding="utf-8") as f:
        f.write(timer_text)
    _systemctl("daemon-reload")
    r = _systemctl("enable", "--now", f"{UNIT_NAME}.timer")
    if r.returncode != 0:
        sys.exit(f"failed to enable timer:\n{r.stderr}")
    print(f"scheduled: auto-update {interval} (upgrade={upgrade}, downtime catch-up on).")
    print(f"  status: wikia schedule status\n  log:    {_log_path()}")


def cmd_status(args):
    p = config_path()
    print(f"config: {p}" + ("" if os.path.exists(p) else "  (not created yet — run `wikia schedule config --write`)"))
    cfg = load_config().get("schedule", {})
    print(f"  enabled={cfg.get('enabled')}  interval={cfg.get('interval')}  upgrade={cfg.get('upgrade')}")
    if shutil.which("systemctl"):
        r = _systemctl("list-timers", f"{UNIT_NAME}.timer", "--all", "--no-pager")
        print("\n" + (r.stdout.strip() or "(timer not installed)"))
    print(f"\nlog: {_log_path()}")


def cmd_remove(args):
    if not args.write:
        print(f"[dry-run] would disable and remove the {UNIT_NAME} timer (re-run with --write)")
        return
    udir = _unit_dir()
    _systemctl("disable", "--now", f"{UNIT_NAME}.timer")
    for q in (os.path.join(udir, f"{UNIT_NAME}.service"), os.path.join(udir, f"{UNIT_NAME}.timer")):
        if os.path.exists(q):
            os.remove(q)
    _systemctl("daemon-reload")
    print(f"removed {UNIT_NAME} timer.")
