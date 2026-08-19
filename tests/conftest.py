"""Shared fixtures — keep every test hermetic (no network, never touch real ~/.claude)."""
import json

import pytest


@pytest.fixture
def isolated_home(tmp_path, monkeypatch):
    """Point HOME and all XDG base dirs at a scratch tree.

    This reroutes every path the package derives from HOME/XDG — the claude
    settings file (~/.claude/settings.json), the hook manifest dir
    (XDG_CONFIG_HOME/cli-wikia/hooks), snapshots and schedule config — so a
    test can never read or write the real user environment.
    """
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(home / ".config"))
    monkeypatch.setenv("XDG_STATE_HOME", str(home / ".local" / "state"))
    # Some libc-backed expanduser paths read USERPROFILE/pwd; keep them aligned.
    monkeypatch.setenv("USERPROFILE", str(home))
    # Config-root overrides must be cleared too. This fixture promises a test
    # can never touch the real user environment, and 0.17.0 added a variable
    # that redirects writes straight back out of the scratch tree: with
    # CLAUDE_CONFIG_DIR set in the shell, four tests wrote to the developer's
    # real config and failed. HOME isolation alone is no longer isolation.
    for var in ("CLAUDE_CONFIG_DIR", "WIKIA_CONFIG_DIR"):
        monkeypatch.delenv(var, raising=False)
    return home


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
