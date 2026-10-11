"""Registry contract: every registered model must be complete and consistent.

Adding a model to models.json without its wiki dir, or claiming a hook
system the wiki doesn't document, fails here before it can drift downstream
into enforcement/fleet. Scope: cli-wikia package only (cross-package parity
lives in cli-collective's suite).
"""
from cli_wikia import MODELS, registry
from cli_wikia.cli import model_dir


def test_every_model_has_required_fields():
    for m in MODELS:
        d = registry.model_data(m)
        assert isinstance(d.get("config_root"), str) and d["config_root"], m
        assert isinstance(d.get("settings_path"), str) and d["settings_path"], m
        assert isinstance(d.get("instruction_file"), str) and d["instruction_file"], m
        assert isinstance(d.get("has_hook_system"), bool), m
        assert isinstance(d.get("artificial_hooks"), bool), m
        assert d.get("binary") is None or isinstance(d["binary"], str), m
        assert d.get("docs_url") is None or isinstance(d["docs_url"], str), m
        assert d.get("config_dir_env") is None or isinstance(d["config_dir_env"], str), m
        ask = d.get("ask_template")
        assert ask is None or (isinstance(ask, list) and "{q}" in ask), m
        subs = d.get("subcommands")
        assert isinstance(subs, list) and all(isinstance(s, list) for s in subs), m


def test_every_model_has_wiki_dir():
    for m in MODELS:
        d = model_dir(m)
        assert d.is_dir(), m
        pages = [p for p in d.iterdir() if p.name.endswith(".md")]
        assert pages, m


def test_hook_system_claim_matches_wiki():
    for m in MODELS:
        has_page = (model_dir(m) / "hooks.md").is_file()
        assert registry.has_hook_system(m) == has_page, m
