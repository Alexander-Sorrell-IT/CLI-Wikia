"""Hook integration for cli-wikia (the 2-level design).

Level 1 (awareness): add a small block to a model's instructions file so the
model knows the local wiki exists and how to query it. Works for every tool.

Level 2 (tailored): generate a manifest of *every hook position a model
supports* — extracted FROM that model's wiki — which you edit, then `apply`
writes the real hooks into the tool's settings. Only Claude and DeepSeek expose
a hook system today.

Everything is **dry-run by default**; nothing touches your files unless you pass
`--write`.
"""
from __future__ import annotations

import json
import os
import re
import sys

from . import MODELS

# Instructions file each tool reads for project/custom guidance (best-effort;
# override with --file). Used by Level 1 awareness.
INSTRUCTION_FILES = {
    "claude": "CLAUDE.md",
    "deepseek": "CLAUDE.md",
    "copilot": "AGENTS.md",
    "gemini": "GEMINI.md",
    "antigravity": "AGENTS.md",
    "chatgpt": "AGENTS.md",
}

# Which models actually have a hook system (verified from their --help/wiki).
HOOK_SYSTEMS = {
    "claude": {"doc": "hooks.md", "settings": ".claude/settings.json", "auto_apply": True},
    "deepseek": {"doc": "sessions-and-agents.md", "settings": ".deepseek-code/settings.json", "auto_apply": False},
}

MARK_START = "<!-- cli-wikia:start -->"
MARK_END = "<!-- cli-wikia:end -->"


def _wikis():
    from .cli import wikis_root

    return wikis_root()


def _topics(model):
    from .cli import topics

    return topics(model)


def manifest_dir():
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(
        os.path.expanduser("~"), ".config"
    )
    return os.path.join(base, "cli-wikia", "hooks")


# --------------------------------------------------------------------------- #
# Level 1 — awareness
# --------------------------------------------------------------------------- #
def _awareness_block(model):
    tlist = ", ".join(_topics(model)[:12])
    return (
        f"{MARK_START}\n"
        f"## Local reference wiki (cli-wikia) — ⚠️ EXPERIMENTAL\n"
        f"> This wiki integration is experimental and may change.\n"
        f"An offline wiki for this tool is installed. Use it as reference:\n"
        f"- `wikia read {model} <topic>` — read a topic\n"
        f"- `wikia search \"<query>\" --model {model}` — search this tool's docs\n"
        f"- `wikia list {model}` — list topics\n"
        f"Available topics: {tlist}\n"
        f"{MARK_END}"
    )


def _strip_block(text):
    return re.sub(
        re.escape(MARK_START) + r".*?" + re.escape(MARK_END) + r"\n?",
        "",
        text,
        flags=re.S,
    ).rstrip() + ("\n" if text.endswith("\n") else "")


def cmd_enable(args):
    model = _resolve(args.model)
    path = args.file or INSTRUCTION_FILES.get(model, "AGENTS.md")
    block = _awareness_block(model)
    existing = ""
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            existing = f.read()
    new = _strip_block(existing)
    new = (new + ("\n\n" if new.strip() else "") + block + "\n")
    if existing == new:
        print(f"{model}: awareness block already present in {path}")
        return
    if not args.write:
        print(f"[dry-run] would write the cli-wikia awareness block to: {path}")
        print("--- block ---")
        print(block)
        print(f"\nre-run with --write to apply.")
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    print(f"{model}: awareness block written to {path}")


def cmd_disable(args):
    model = _resolve(args.model)
    path = args.file or INSTRUCTION_FILES.get(model, "AGENTS.md")
    if not os.path.exists(path):
        print(f"{model}: {path} does not exist — nothing to remove")
        return
    with open(path, encoding="utf-8") as f:
        existing = f.read()
    new = _strip_block(existing)
    if existing == new:
        print(f"{model}: no cli-wikia block found in {path}")
        return
    if not args.write:
        print(f"[dry-run] would remove the cli-wikia block from: {path} (re-run with --write)")
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    print(f"{model}: awareness block removed from {path}")


# --------------------------------------------------------------------------- #
# Level 2 — tailored hook manifest
# --------------------------------------------------------------------------- #
def hook_events(model):
    """Extract hook event names directly from the model's wiki doc."""
    sysinfo = HOOK_SYSTEMS.get(model)
    if not sysinfo:
        return []
    doc = _wikis() / model / sysinfo["doc"]
    if not doc.is_file():
        return []
    text = doc.read_text(encoding="utf-8")
    # events appear in tables as | `EventName` |
    events = re.findall(r"\|\s*`([A-Z][A-Za-z]+)`", text)
    return sorted(set(events))


def cmd_manifest(args):
    model = _resolve(args.model)
    if model not in HOOK_SYSTEMS:
        sys.exit(
            f"{model} has no hook system (only {', '.join(HOOK_SYSTEMS)} do). "
            f"Use `wikia hooks enable {model}` for Level-1 awareness instead."
        )
    events = hook_events(model)
    if not events:
        sys.exit(f"could not extract hook events from {model}'s wiki.")
    mdir = manifest_dir()
    os.makedirs(mdir, exist_ok=True)
    skeleton = {ev: [] for ev in events}
    json_path = os.path.join(mdir, f"{model}.hooks.json")
    ref_path = os.path.join(mdir, f"{model}.hooks.md")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(skeleton, f, indent=2)
        f.write("\n")
    ref = [
        f"# {model} hook positions (generated from the wiki)",
        "",
        "> ⚠️ **EXPERIMENTAL.** This hook integration is new and may change. "
        "Hooks run automatically and can block the tool — review carefully before applying.",
        "",
        f"Edit `{model}.hooks.json` to add hooks. Each event maps to a list of",
        'handlers, e.g.: {"matcher": "Bash", "type": "command", "command": "echo hi"}',
        "",
        f"Then run: `wikia hooks apply {model}` (dry-run) and `--write` to install.",
        "",
        "## Available events",
    ]
    ref += [f"- `{ev}`" for ev in events]
    with open(ref_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ref) + "\n")
    print(f"{model}: manifest generated ({len(events)} hook positions)")
    print(f"  edit:  {json_path}")
    print(f"  guide: {ref_path}")
    print(f"  then:  wikia hooks apply {model}")


def cmd_apply(args):
    model = _resolve(args.model)
    sysinfo = HOOK_SYSTEMS.get(model)
    if not sysinfo:
        sys.exit(f"{model} has no hook system to apply to.")
    json_path = os.path.join(manifest_dir(), f"{model}.hooks.json")
    if not os.path.exists(json_path):
        sys.exit(f"no manifest yet — run `wikia hooks manifest {model}` first.")
    with open(json_path, encoding="utf-8") as f:
        manifest = json.load(f)
    valid = set(hook_events(model))
    chosen = {ev: hs for ev, hs in manifest.items() if hs}
    bad = [ev for ev in chosen if ev not in valid]
    if bad:
        sys.exit(f"unknown event(s) in manifest: {', '.join(bad)}")
    if not chosen:
        print(f"{model}: manifest is empty — nothing to apply. Edit {json_path} first.")
        return
    if not sysinfo["auto_apply"]:
        print(f"{model}: auto-apply not yet wired for this tool's config format.")
        print(f"  Your manifest is ready at {json_path}.")
        print(f"  Add these hooks via the tool itself (e.g. `deepseek-code hooks`)"
              f" or its settings file: {sysinfo['settings']}")
        return
    # Build the settings.json `hooks` structure (Claude Code format).
    hooks_block = {}
    for ev, handlers in chosen.items():
        hooks_block[ev] = [{"matcher": h.get("matcher", ""), "hooks": [
            {k: v for k, v in h.items() if k != "matcher"}]} for h in handlers]
    target = args.file or sysinfo["settings"]
    current = {}
    if os.path.exists(target):
        with open(target, encoding="utf-8") as f:
            current = json.load(f)
    merged = dict(current)
    merged.setdefault("hooks", {})
    merged["hooks"].update(hooks_block)
    preview = json.dumps(merged, indent=2)
    if not args.write:
        print(f"[dry-run] would write {len(chosen)} event(s) into: {target}")
        print("--- resulting settings.json ---")
        print(preview[:2000] + ("\n…" if len(preview) > 2000 else ""))
        print(f"\nre-run with --write to install.")
        return
    os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(preview + "\n")
    print(f"{model}: wrote {len(chosen)} hook event(s) into {target}")


def cmd_status(args):
    models = MODELS if (args.all or not args.model) else [_resolve(args.model)]
    for m in models:
        has_hooks = "yes" if m in HOOK_SYSTEMS else "no"
        ifile = INSTRUCTION_FILES.get(m, "AGENTS.md")
        aware = "—"
        if os.path.exists(ifile):
            with open(ifile, encoding="utf-8") as f:
                aware = "installed" if MARK_START in f.read() else "no"
        man = os.path.join(manifest_dir(), f"{m}.hooks.json")
        manifest = "yes" if os.path.exists(man) else "no"
        print(f"{m:12} hook-system: {has_hooks:3}  L1-awareness({ifile}): {aware:9}  L2-manifest: {manifest}")


def _resolve(model):
    if model not in MODELS:
        sys.exit(f"unknown model '{model}'. choose from: {', '.join(MODELS)}")
    return model
