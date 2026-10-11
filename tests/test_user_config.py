"""Layered user config + --model/--<name> flags.

Precedence: flag > collective global > package file > list-and-exit.
XDG_CONFIG_HOME redirects all files (tests never touch the real home).
"""
import json

import pytest

from cli_wikia import cli
from cli_wikia.user_config import (
    add_model_flags,
    config_path,
    effective,
    pick_model,
    read_config,
    write_config,
)


@pytest.fixture
def xdg(tmp_path, monkeypatch):
    home = tmp_path / "xdg"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(home))
    return home


def test_precedence_flag_package_collective(xdg):
    write_config("wikia", {"default_model": "grok"})
    write_config("collective", {"default_model": "muse"})
    assert effective("wikia", "default_model") == "muse"
    assert pick_model("wikia", "qwen", None) == "qwen"
    assert pick_model("wikia", None, "aider") == "aider"
    assert pick_model("wikia", None, None) == "muse"


def test_package_config_used_when_no_global(xdg):
    write_config("wikia", {"default_model": "opencode"})
    assert pick_model("wikia", None, None) == "opencode"


def test_nothing_anywhere_lists_models_and_exits(xdg):
    with pytest.raises(SystemExit) as exc:
        pick_model("wikia", None, None)
    assert "qwen" in str(exc.value) and "muse" in str(exc.value)


def test_unknown_names_rejected(xdg):
    with pytest.raises(SystemExit):
        pick_model("wikia", "nope", None)
    with pytest.raises(SystemExit):
        pick_model("wikia", None, "nope")
    write_config("wikia", {"default_model": "nope"})
    with pytest.raises(SystemExit):
        pick_model("wikia", None, None)


def test_corrupt_config_ignored(xdg):
    config_path("wikia").parent.mkdir(parents=True, exist_ok=True)
    config_path("wikia").write_text("{broken", encoding="utf-8")
    assert read_config("wikia") == {}
    assert effective("wikia", "default_model", "fb") == "fb"


def test_model_shortcut_flags_parse():
    p = cli.build_parser()
    a = p.parse_args(["read", "--grok", "README"])
    assert a.model_flag == "grok" and a.model is None
    a = p.parse_args(["read", "--model", "qwen", "README"])
    assert a.model_flag == "qwen"
    a = p.parse_args(["read", "muse", "README"])
    assert a.model == "muse" and a.model_flag is None
    a = p.parse_args(["search", "--aider", "hooks"])
    assert a.model_flag == "aider"


def test_read_via_flag_end_to_end(capsys):
    cli.cmd_read(_ns(model=None, topic="README", model_flag="grok"))
    assert "Grok" in capsys.readouterr().out


def test_read_via_package_config(xdg, capsys):
    write_config("wikia", {"default_model": "qwen"})
    cli.cmd_read(_ns(model=None, topic="README", model_flag=None))
    assert "Qwen" in capsys.readouterr().out


def test_collective_config_overrides_package(xdg, capsys):
    write_config("wikia", {"default_model": "qwen"})
    write_config("collective", {"default_model": "aider"})
    cli.cmd_read(_ns(model=None, topic="README", model_flag=None))
    assert "Aider" in capsys.readouterr().out


def _ns(**kw):
    import types

    base = {"model": None, "topic": None, "model_flag": None, "as_of": None}
    base.update(kw)
    return types.SimpleNamespace(**base)
