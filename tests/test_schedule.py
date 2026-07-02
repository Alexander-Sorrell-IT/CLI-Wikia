"""schedule apply --dry-run must emit a shell-safe ExecStart even with spaces in paths."""
import shlex
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

    schedule.cmd_apply(SimpleNamespace(write=False))

    out = capsys.readouterr().out
    assert "ExecStart=" in out
    # the spaced path appears only in its properly quoted form, never bare.
    assert shlex.quote(SPACED_WIKIA) in out
    assert f" {SPACED_WIKIA} update" not in out
