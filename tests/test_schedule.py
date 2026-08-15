"""schedule apply --dry-run must emit a shell-safe ExecStart (Linux) or
a valid launchd plist (macOS), even with spaces in paths."""
import plistlib
import shlex
import sys
from types import SimpleNamespace

from cli_wikia import schedule

SPACED_WIKIA = "/home/my user/bin/wikia"


def test_apply_dry_run_quotes_execstart_with_spaces(monkeypatch, capsys):
    # wikia resolves to a path containing a space; systemd ExecStart is a single
    # line, so the path must be quoted or the unit would split it into args.
    monkeypatch.setattr(schedule.shutil, "which", lambda name: SPACED_WIKIA)
    monkeypatch.setattr(
        schedule, "load_config",
        lambda: {"schedule": {"enabled": True, "interval": "daily", "upgrade": True}},
    )
    # Force Linux path regardless of host platform.
    monkeypatch.setattr(schedule, "_have_launchd", lambda: False)

    schedule.cmd_apply(SimpleNamespace(write=False))

    out = capsys.readouterr().out
    assert "ExecStart=" in out
    # the spaced path appears only in its properly quoted form, never bare.
    assert shlex.quote(SPACED_WIKIA) in out
    assert f" {SPACED_WIKIA} update" not in out


def test_launchd_dry_run_emits_valid_plist(monkeypatch, capsys):
    """On macOS (launchd path): dry-run must print a valid plist with correct keys."""
    monkeypatch.setattr(schedule.shutil, "which", lambda name: "/usr/local/bin/wikia")
    monkeypatch.setattr(schedule, "_have_launchd", lambda: True)
    monkeypatch.setattr(
        schedule, "load_config",
        lambda: {"schedule": {"enabled": True, "interval": "weekly", "upgrade": False}},
    )

    schedule.cmd_apply(SimpleNamespace(write=False))

    out = capsys.readouterr().out
    # Must mention the plist path and the interval seconds.
    assert schedule.LAUNCHD_LABEL in out
    assert str(schedule._INTERVAL_SECONDS["weekly"]) in out
    # The plist block must be parseable.
    start = out.index("<?xml")
    end = out.index("</plist>") + len("</plist>")
    plist = plistlib.loads(out[start:end].encode())
    assert plist["Label"] == schedule.LAUNCHD_LABEL
    assert plist["StartInterval"] == schedule._INTERVAL_SECONDS["weekly"]
    assert plist["RunAtLoad"] is False
    # upgrade=False → no pip install in the script
    assert "pip" not in plist["ProgramArguments"][-1]


def test_launchd_disabled_dry_run(monkeypatch, capsys):
    """enabled=false on macOS → dry-run says it would remove the agent."""
    monkeypatch.setattr(schedule, "_have_launchd", lambda: True)
    monkeypatch.setattr(
        schedule, "load_config",
        lambda: {"schedule": {"enabled": False, "interval": "daily", "upgrade": True}},
    )

    schedule.cmd_apply(SimpleNamespace(write=False))

    out = capsys.readouterr().out
    assert "dry-run" in out
    assert "launchd" in out


def test_interval_seconds_covers_all_intervals():
    """Every INTERVAL string must have a matching seconds entry."""
    for iv in schedule.INTERVALS:
        assert iv in schedule._INTERVAL_SECONDS, f"missing seconds for interval '{iv}'"
        assert schedule._INTERVAL_SECONDS[iv] > 0
