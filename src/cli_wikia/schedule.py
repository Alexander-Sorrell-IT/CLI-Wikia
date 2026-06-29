"""Scheduled auto-update for cli-wikia.

Installs a systemd *user* timer that periodically runs `wikia update --all`
(optionally also `pip install --upgrade cli-wikia`). Uses `Persistent=true`, so
a run missed while the machine was off ("downtime") fires on next boot.

Interval is one of: hourly, daily, weekly, monthly.
Dry-run by default; pass --write to actually install/remove.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

INTERVALS = ("hourly", "daily", "weekly", "monthly")
UNIT_NAME = "cli-wikia-update"


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
        "[Service]\n"
        "Type=oneshot\n"
        f"ExecStart={_exec_command(upgrade)}\n"
    )


def _timer_unit(interval):
    return (
        f"[Unit]\nDescription=cli-wikia scheduled update ({interval})\n\n"
        "[Timer]\n"
        f"OnCalendar={interval}\n"
        "Persistent=true\n\n"
        "[Install]\nWantedBy=timers.target\n"
    )


def _systemctl(*a):
    return subprocess.run(
        ["systemctl", "--user", *a], capture_output=True, text=True
    )


def _have_systemd_user():
    if not shutil.which("systemctl"):
        return False
    return _systemctl("is-system-running").returncode is not None


def cmd_schedule(args):
    udir = _unit_dir()
    svc = os.path.join(udir, f"{UNIT_NAME}.service")
    tmr = os.path.join(udir, f"{UNIT_NAME}.timer")

    if args.status:
        if not shutil.which("systemctl"):
            print("systemctl not found — no systemd timer scheduling on this system.")
            return
        r = _systemctl("list-timers", f"{UNIT_NAME}.timer", "--all", "--no-pager")
        print(r.stdout.strip() or "(no cli-wikia timer installed)")
        print(f"\nlog: {_log_path()}")
        return

    if args.remove:
        if not args.write:
            print(f"[dry-run] would disable and remove {UNIT_NAME}.timer/.service (re-run with --write)")
            return
        _systemctl("disable", "--now", f"{UNIT_NAME}.timer")
        for p in (svc, tmr):
            if os.path.exists(p):
                os.remove(p)
        _systemctl("daemon-reload")
        print(f"removed {UNIT_NAME} timer.")
        return

    interval = args.interval
    if interval not in INTERVALS:
        sys.exit(f"interval must be one of: {', '.join(INTERVALS)}")

    service_text = _service_unit(args.upgrade)
    timer_text = _timer_unit(interval)

    if not args.write:
        print(f"[dry-run] would install a systemd user timer running '{interval}'"
              f"{' (with pip upgrade)' if args.upgrade else ''}:\n")
        print(f"# {svc}\n{service_text}")
        print(f"# {tmr}\n{timer_text}")
        print("then: systemctl --user daemon-reload && "
              f"systemctl --user enable --now {UNIT_NAME}.timer")
        print(f"\nlog would be written to: {_log_path()}")
        print("\nre-run with --write to install.")
        return

    if not _have_systemd_user():
        sys.exit(
            "systemd user instance not available. As a fallback, add a cron job, e.g.:\n"
            f"  (crontab -l 2>/dev/null; echo '@{interval} {shutil.which('wikia') or 'wikia'} "
            "update --all --write') | crontab -"
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
    print(f"installed: cli-wikia will auto-update {interval} (with downtime catch-up).")
    print(f"  check:  wikia schedule --status")
    print(f"  log:    {_log_path()}")
