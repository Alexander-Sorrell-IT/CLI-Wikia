"""Level-2 hook install/remove behaviour, run entirely against a scratch HOME."""
import json
import os
from types import SimpleNamespace

import pytest

from cli_wikia import hooks

from conftest import write_json

# A valid claude hook event (claude's wiki enumerates these; apply validates
# the manifest against them).
EVENT = "PreToolUse"
WIKIA_CMD = "echo cli-wikia-hook"
USER_CMD = "echo pre-existing-user-hook"


def _group(cmd, matcher="Bash"):
    """A handler group in the tool's own schema; its identity is its command."""
    return {"matcher": matcher, "hooks": [{"type": "command", "command": cmd}]}


def _settings_path(home):
    return home / ".claude" / "settings.json"


def _seed_manifest(home):
    """Write a manifest choosing one wikia-owned handler group for EVENT."""
    mdir = home / ".config" / "cli-wikia" / "hooks"
    write_json(mdir / "claude.hooks.json", {EVENT: [_group(WIKIA_CMD)]})


def _seed_settings_with_user_hook(home):
    write_json(_settings_path(home), {"hooks": {EVENT: [_group(USER_CMD)]}})


def _apply_args(write=True):
    return SimpleNamespace(model="claude", file=None, write=write)


def test_known_settings_path_resolves_under_home(isolated_home):
    assert hooks.hook_config_path("claude") == "~/.claude/settings.json"
    resolved = os.path.expanduser(hooks.hook_config_path("claude"))
    assert resolved == str(_settings_path(isolated_home))


def test_apply_preserves_user_hook_and_backs_up(isolated_home):
    _seed_manifest(isolated_home)
    _seed_settings_with_user_hook(isolated_home)

    hooks.cmd_apply(_apply_args())

    data = json.loads(_settings_path(isolated_home).read_text())
    cmds = [h["command"] for g in data["hooks"][EVENT] for h in g["hooks"]]
    assert USER_CMD in cmds  # user's hook survived
    assert WIKIA_CMD in cmds  # ours was merged in

    backup = _settings_path(isolated_home).with_name("settings.json.bak-cli-wikia")
    assert backup.exists()
    assert json.loads(backup.read_text())["hooks"][EVENT]  # backup is the pre-apply file


def test_reapply_is_idempotent(isolated_home):
    _seed_manifest(isolated_home)
    _seed_settings_with_user_hook(isolated_home)

    hooks.cmd_apply(_apply_args())
    first = _settings_path(isolated_home).read_text()
    hooks.cmd_apply(_apply_args())
    second = _settings_path(isolated_home).read_text()

    assert first == second
    groups = json.loads(second)["hooks"][EVENT]
    assert len(groups) == 2  # user group + our single group, not duplicated


def test_remove_deletes_only_wikia_hook(isolated_home):
    _seed_manifest(isolated_home)
    _seed_settings_with_user_hook(isolated_home)

    hooks.cmd_apply(_apply_args())
    hooks.cmd_unapply(_apply_args())

    data = json.loads(_settings_path(isolated_home).read_text())
    cmds = [h["command"] for g in data["hooks"][EVENT] for h in g["hooks"]]
    assert cmds == [USER_CMD]  # only the user's hook remains


def test_apply_on_malformed_json_exits_clean_and_leaves_file(isolated_home, capsys):
    _seed_manifest(isolated_home)
    target = _settings_path(isolated_home)
    target.parent.mkdir(parents=True, exist_ok=True)
    garbage = "{ this is not valid json "
    target.write_text(garbage, encoding="utf-8")

    with pytest.raises(SystemExit) as e:
        hooks.cmd_apply(_apply_args())
    # sys.exit(<message>): non-zero process status (1), a clean message not a raise.
    assert e.value.code not in (0, None)
    assert isinstance(e.value.code, str) and "could not read" in e.value.code
    assert target.read_text() == garbage  # untouched
    assert "Traceback" not in capsys.readouterr().err


def test_apply_on_non_dict_toplevel_exits_clean_and_leaves_file(isolated_home, capsys):
    _seed_manifest(isolated_home)
    target = _settings_path(isolated_home)
    write_json(target, ["not", "a", "dict"])
    before = target.read_text()

    with pytest.raises(SystemExit) as e:
        hooks.cmd_apply(_apply_args())
    assert e.value.code not in (0, None)
    assert isinstance(e.value.code, str) and "not a JSON object" in e.value.code
    assert target.read_text() == before  # untouched
    assert "Traceback" not in capsys.readouterr().err


# ── where hooks get written: --file > model env var > WIKIA_CONFIG_DIR > wiki ──
# 0.17.0 shipped this redirect with no test of its own; its only effect on the
# suite was breaking four unrelated tests. Each branch is pinned here.

def _resolve(model="claude", file=None):
    return hooks._resolve_target(SimpleNamespace(model=model, file=file, write=False),
                                 model, "/tmp/manifest.json")


def test_default_target_is_the_wiki_path(isolated_home):
    assert _resolve() == str(_settings_path(isolated_home))


def test_explicit_file_beats_every_override(isolated_home, monkeypatch):
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", "/opt/ccd")
    monkeypatch.setenv("WIKIA_CONFIG_DIR", "/opt/wcd")
    assert _resolve(file="/tmp/explicit.json") == "/tmp/explicit.json"


def test_model_env_var_redirects(isolated_home, monkeypatch):
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", "/opt/ccd")
    assert _resolve() == "/opt/ccd/settings.json"


def test_generic_var_covers_models_with_no_known_variable(isolated_home, monkeypatch):
    # gemini has config_dir_env=null; without the generic fallback it would be
    # unreachable, which is what made the per-model field alone insufficient.
    monkeypatch.setenv("WIKIA_CONFIG_DIR", "/opt/wcd")
    from cli_wikia import registry
    assert registry.config_dir_env("gemini") is None
    target = _resolve(model="gemini")
    assert target.startswith("/opt/wcd"), target


def test_model_var_wins_over_generic(isolated_home, monkeypatch):
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", "/opt/ccd")
    monkeypatch.setenv("WIKIA_CONFIG_DIR", "/opt/wcd")
    assert _resolve() == "/opt/ccd/settings.json"


def test_prefix_is_anchored_so_claude_alt_is_not_matched(isolated_home, monkeypatch):
    # ~/.claude must not match ~/.claude-alt — the separator is what stops it.
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", "/opt/ccd")
    monkeypatch.setattr(hooks, "hook_config_path", lambda m: "~/.claude-alt/settings.json")
    assert _resolve() == str(isolated_home / ".claude-alt" / "settings.json")


def test_unrelated_root_is_left_alone(isolated_home, monkeypatch):
    # chatgpt's root is .codex; CLAUDE_CONFIG_DIR must not touch it.
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", "/opt/ccd")
    target = _resolve(model="chatgpt")
    assert target is None or "/opt/ccd" not in target, target
