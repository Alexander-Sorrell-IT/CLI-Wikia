"""Layered user config shared by the cli-* family.

Precedence (highest wins): CLI flag > collective global config >
per-package config > built-in default. Each tool works standalone on its
own file; editing the collective global file overrides the smaller ones.

Files (under $XDG_CONFIG_HOME or ~/.config):
  cli-wikia/config.json  cli-enforcement/config.json  cli-fleet/config.json
  cli-collective/config.json   (global overrides)

Corrupt or unreadable files are ignored (fail-open to the next layer) so a
bad edit can never brick a CLI; `*_config_path` helpers let callers and
tests point at the exact file in play.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

PACKAGE_FILES = {
    "wikia": "cli-wikia/config.json",
    "enforcement": "cli-enforcement/config.json",
    "fleet": "cli-fleet/config.json",
    "collective": "cli-collective/config.json",
}


def config_home() -> Path:
    override = os.environ.get("XDG_CONFIG_HOME")
    if override:
        return Path(override)
    return Path(os.path.expanduser("~")) / ".config"


def config_path(package: str) -> Path:
    return config_home() / PACKAGE_FILES[package]


def read_config(package: str) -> Dict[str, Any]:
    try:
        text = config_path(package).read_text(encoding="utf-8")
    except OSError:
        return {}
    try:
        data = json.loads(text)
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def write_config(package: str, updates: Dict[str, Any]) -> Path:
    """Merge updates into the package config file. Returns the path."""
    path = config_path(package)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = read_config(package)
    data.update(updates)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def effective(package: str, key: str, default: Any = None) -> Any:
    """Collective global value wins; else the package value; else default."""
    glob = read_config("collective")
    if key in glob and glob[key] is not None:
        return glob[key]
    own = read_config(package)
    if key in own and own[key] is not None:
        return own[key]
    return default


def pick_model(package: str, flag: Optional[str] = None,
               positional: Optional[str] = None) -> str:
    """Resolve which model a command targets.

    Order: --model/--<name> flag > positional > collective default_model >
    package default_model. Unknown names error with the model list; when
    nothing selects a model, print the list (bare-/model behavior) and exit.
    """
    from .registry import all_models

    models = all_models()
    for cand in (flag, positional):
        if cand is not None:
            if cand not in models:
                sys.exit(f"unknown model '{cand}'. choose from: {', '.join(models)}")
            return cand
    cfg = effective(package, "default_model")
    if cfg is not None:
        if cfg not in models:
            sys.exit(f"invalid default_model '{cfg}' in config. choose from: {', '.join(models)}")
        return cfg
    sys.exit("no model given. choose from: " + ", ".join(models)
             + f" (pass --model, --<name>, or set default_model in {config_path(package)})")


def add_model_flags(parser, models: List[str], with_model: bool = True) -> None:
    """Add --model plus one --<name> shortcut per model (all→model_flag).

    with_model=False skips --model (for parsers that already define it with
    a different dest) and adds only the shortcuts.
    """
    if with_model:
        parser.add_argument("--model", dest="model_flag", default=None,
                            help="target model (or use --<name>, or set default_model in config)")
    for m in models:
        parser.add_argument(f"--{m}", dest="model_flag", action="store_const",
                            const=m, help=f"shortcut for --model {m}")
