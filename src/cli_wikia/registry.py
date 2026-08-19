"""Model registry loader for cli-wikia.

Reads models.json (bundled with this package) and, when cli-collective is
installed, deep-merges the collective override on top so that all three
packages (wikia / enforcement / fleet) pick up changes from one place.

Usage (inside cli-wikia):
    from .registry import model_data, all_models, get

Usage (from cli-enforcement / cli-fleet):
    from cli_wikia.registry import model_data, all_models, get
"""
from __future__ import annotations

import copy
import json
from importlib import resources
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Loading helpers
# ---------------------------------------------------------------------------

def _load_bundled() -> Dict[str, Any]:
    """Load the models.json bundled with cli-wikia."""
    text = (resources.files("cli_wikia") / "models.json").read_text(encoding="utf-8")
    return json.loads(text)


def _load_collective_override() -> Optional[Dict[str, Any]]:
    """Load the cli-collective override file when cli-collective is installed.

    Returns the 'wikia' sub-dict of the collective models.json, or None if
    cli-collective is not installed or has no wikia override.
    """
    try:
        from importlib import resources as _r
        text = (_r.files("cli_collective") / "models.json").read_text(encoding="utf-8")
        data = json.loads(text)
        return data.get("wikia") or None
    except Exception:
        return None


def _deep_merge(base: Dict, override: Dict) -> Dict:
    """Recursively merge override into a copy of base. Lists are replaced, not
    appended. None values in override are passed through (they clear a field)."""
    result = copy.deepcopy(base)
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = copy.deepcopy(val)
    return result


def _build_registry() -> Dict[str, Any]:
    """Load and merge wikia model data once at import time."""
    data = _load_bundled()
    override = _load_collective_override()
    if override:
        base_models = data.get("models", {})
        over_models = override.get("models", {})
        if over_models:
            data["models"] = _deep_merge(base_models, over_models)
    return data


# Module-level singleton — loaded once.
_REGISTRY: Dict[str, Any] = _build_registry()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def all_models() -> List[str]:
    """Ordered list of all model names in the registry."""
    return list(_REGISTRY.get("models", {}).keys())


def model_data(model: str) -> Dict[str, Any]:
    """Full data dict for one model. Returns {} for unknown models."""
    return _REGISTRY.get("models", {}).get(model, {})


def get(model: str, field: str, default: Any = None) -> Any:
    """Get one field for a model, with a default if absent."""
    return model_data(model).get(field, default)


# Convenience accessors used across wikia / enforcement / fleet

def binary(model: str) -> Optional[str]:
    return get(model, "binary")


def docs_url(model: str) -> Optional[str]:
    return get(model, "docs_url")


def ask_template(model: str) -> Optional[List[str]]:
    return get(model, "ask_template")


def subcommands(model: str) -> List[List[str]]:
    return get(model, "subcommands", [])


def config_root(model: str) -> Optional[str]:
    return get(model, "config_root")


def settings_path(model: str) -> Optional[str]:
    return get(model, "settings_path")


def config_dir_env(model: str) -> Optional[str]:
    """The env var this tool uses to relocate its config root, if it has one.

    None means no known variable, not "no override" — callers fall back to
    WIKIA_CONFIG_DIR. Guessing a name here would be worse than leaving it
    null: a variable nobody sets never fires, which looks exactly like a user
    who did not want an override.
    """
    return get(model, "config_dir_env")


def instruction_file(model: str) -> str:
    return get(model, "instruction_file", "AGENTS.md")


def has_hook_system(model: str) -> bool:
    return bool(get(model, "has_hook_system", False))


def artificial_hooks(model: str) -> bool:
    """True when the model's enforcement was deployed with artificial event names.
    The engine is fully wired but the CLI won't actually fire those events yet.
    Once the CLI gains a real hook system, run cli-enforcement sync to upgrade."""
    return bool(get(model, "artificial_hooks", False))


def reload() -> None:
    """Force a reload of the registry (useful after tests patch files)."""
    global _REGISTRY
    _REGISTRY = _build_registry()
