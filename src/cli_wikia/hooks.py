"""Hook integration for cli-wikia (the 2-level design) — fully wiki-derived.

NOTHING here is a hardcoded per-model table. Which models have hooks, what
events they expose, where hooks are configured, and which instructions file a
tool reads are ALL discovered at runtime from each model's wiki (the pages the
deep-dive built). Add or update a model's wiki and this feature follows along.

Level 1 (awareness): add a small block to a model's instructions file so the
model knows the local wiki exists and how to query it.
Level 2 (tailored): generate a manifest of the hook positions documented in the
model's wiki, which you edit, then `apply` merges them into the tool's settings.

Everything is dry-run by default; nothing is written unless you pass --write.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path

from . import MODELS

MARK_START = "<!-- cli-wikia:start -->"
MARK_END = "<!-- cli-wikia:end -->"

# Known custom-instruction filenames to look for when scanning a wiki. This is a
# list of conventions to RECOGNIZE, not a per-model mapping — the wiki decides
# which one applies to each tool.
INSTRUCTION_CANDIDATES = [
    "CLAUDE.md", "GEMINI.md", "AGENTS.md",
    ".github/copilot-instructions.md", "QWEN.md", "codex.md",
    "CLAWSPRING.md", "BOB.md",
]


def _wikis():
    from .cli import wikis_root

    return wikis_root()


def _model_dir(model):
    return _wikis() / model


def _topics(model):
    from .cli import topics

    return topics(model)


def _read(path):
    try:
        return path.read_text(encoding="utf-8") if path.is_file() else ""
    except OSError:
        return ""


def _wiki_text(model, *names):
    """Concatenated text of the named wiki files, or ALL .md if none named."""
    d = _model_dir(model)
    if not d.is_dir():
        return ""
    files = [d / n for n in names] if names else sorted(
        p for p in d.iterdir() if p.name.endswith(".md")
    )
    return "\n".join(_read(f) for f in files)


def manifest_dir():
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(
        os.path.expanduser("~"), ".config"
    )
    return os.path.join(base, "cli-wikia", "hooks")


# --------------------------------------------------------------------------- #
# Wiki-derived facts (no hardcoded per-model tables)
# --------------------------------------------------------------------------- #
def has_hook_system(model):
    """A model has hooks if its wiki documents them (a hooks.md page exists)."""
    return (_model_dir(model) / "hooks.md").is_file()


def hook_events(model):
    """Hook event names parsed out of the model's hooks.md (empty if none listed)."""
    text = _read(_model_dir(model) / "hooks.md")
    if not text:
        return []
    events = re.findall(r"\|\s*`([A-Z][A-Za-z]+)`", text)            # table cells
    if not events:
        events = re.findall(r"^[-*\d.]+\s+`([A-Z][A-Za-z]+)`", text, re.M)  # list items
    return sorted(set(events))


# Known-good per-model settings paths. Preferred over the wiki regex heuristic
# below; extend as models are verified.
KNOWN_SETTINGS_PATHS = {
    "claude": "~/.claude/settings.json",
    "bob": "~/.config/bob/settings.json",
}

# Known-good project config roots where the wiki word-count heuristic picks the
# wrong directory (antigravity's most-mentioned dot-dir is `.system_generated/`,
# its logs dir; the real workspace config dir is `.agents/` per customization.md).
KNOWN_CONFIG_ROOTS = {
    "antigravity": ".agents",
    "bob": ".agents",
}


def hook_config_path(model):
    """Where this tool stores hooks/settings — a verified per-model path when we
    have one, otherwise extracted from its wiki text (heuristic)."""
    known = KNOWN_SETTINGS_PATHS.get(model)
    if known:
        return known
    text = _wiki_text(model, "hooks.md", "configuration.md", "settings.md")
    paths = re.findall(r"`?(~?[\w./-]*(?:settings|hooks)\.json)`?", text)
    paths = [p.strip("`") for p in paths if p]
    if not paths:
        return None
    home = [p for p in paths if p.startswith("~")]
    pool = home or paths
    return max(pool, key=len)  # prefer the most specific (longest) path


def instruction_file(model):
    """The custom-instructions filename this tool reads, found in its wiki."""
    text = _wiki_text(model)
    counts = {c: len(re.findall(re.escape(c), text)) for c in INSTRUCTION_CANDIDATES}
    best = max(counts, key=lambda c: counts[c])
    return best if counts[best] else "AGENTS.md"


def config_root(model):
    """The project-level config directory a tool uses (e.g. .claude, .gemini,
    .github), derived dynamically from the model's wiki — the most-mentioned
    dot-directory. Used by downstream tools (e.g. cli-enforcement) to know where
    to deploy per-model files. Returns None if the wiki names no such dir."""
    known = KNOWN_CONFIG_ROOTS.get(model)
    if known:
        return known
    text = _wiki_text(model, "hooks.md", "configuration.md", "settings.md",
                      "getting-started.md", "cli-reference.md")
    dirs = re.findall(r"(?<![\w/~.])(\.[a-z][\w-]+)/", text)
    # ignore obvious non-config dot-dirs
    ignore = {".md", ".py", ".sh", ".json", ".git", ".env", ".venv"}
    counts = {}
    for d in dirs:
        if d in ignore:
            continue
        counts[d] = counts.get(d, 0) + 1
    if not counts:
        return None
    return max(counts, key=lambda d: counts[d])


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
        "", text, flags=re.S,
    ).rstrip() + ("\n" if text.endswith("\n") else "")


def _instruction_path(model, override=None):
    """Absolute path of the Level-1 instructions file (cwd-relative by default)."""
    p = Path(override) if override else Path.cwd() / instruction_file(model)
    return p.resolve()


def cmd_enable(args):
    model = _resolve(args.model)
    path = _instruction_path(model, args.file)
    block = _awareness_block(model)
    existing = _read_text(path)
    new = _strip_block(existing)
    new = new + ("\n\n" if new.strip() else "") + block + "\n"
    if existing == new:
        print(f"{model}: awareness block already present in {path}")
        return
    if not args.write:
        print(f"[dry-run] would write the cli-wikia awareness block to: {path}")
        print("--- block ---")
        print(block)
        print("\nre-run with --write to apply.")
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    print(f"{model}: awareness block written to {path}")


def cmd_disable(args):
    model = _resolve(args.model)
    path = _instruction_path(model, args.file)
    if not os.path.exists(path):
        print(f"{model}: {path} does not exist — nothing to remove")
        return
    existing = _read_text(path)
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
def cmd_manifest(args):
    model = _resolve(args.model)
    if not has_hook_system(model):
        sys.exit(
            f"{model}'s wiki documents no hook system (no hooks.md). "
            f"Use `wikia hooks enable {model}` for Level-1 awareness instead."
        )
    events = hook_events(model)
    cfg = hook_config_path(model)
    mdir = manifest_dir()
    os.makedirs(mdir, exist_ok=True)
    json_path = os.path.join(mdir, f"{model}.hooks.json")
    ref_path = os.path.join(mdir, f"{model}.hooks.md")

    skeleton = {ev: [] for ev in events}
    if not events:
        skeleton = {
            "_note": "No hook events were enumerated in this tool's wiki. Add event "
            f"names as keys (see `wikia read {model} hooks` and the official docs)."
        }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(skeleton, f, indent=2)
        f.write("\n")

    ref = [
        f"# {model} hook positions (generated from the wiki)",
        "",
        "> ⚠️ **EXPERIMENTAL.** Hooks run automatically and can block the tool — "
        "review carefully before applying.",
        "",
        f"Config target (from the wiki): `{cfg or 'unknown — see the tool docs'}`",
        f"Handler format: see `wikia read {model} hooks`.",
        "",
        f"Edit `{model}.hooks.json`, then run `wikia hooks apply {model}`.",
        "",
        "## Hook events documented in the wiki",
    ]
    ref += [f"- `{ev}`" for ev in events] or [
        "_(The wiki does not enumerate named events for this tool — add them "
        "manually from the official docs.)_"
    ]
    with open(ref_path, "w", encoding="utf-8") as f:
        f.write("\n".join(ref) + "\n")

    n = len(events)
    print(f"{model}: manifest generated ({n} hook event{'s' if n != 1 else ''} from the wiki)")
    print(f"  config target (from wiki): {cfg or 'unknown'}")
    print(f"  edit:  {json_path}")
    print(f"  guide: {ref_path}")
    print(f"  then:  wikia hooks apply {model}")


def _load_json_file(path, what):
    """json.load with a clean error message instead of a traceback."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"error: could not read {what} ({path}): {e}")
    if not isinstance(data, dict):
        sys.exit(f"error: {what} ({path}) top level is not a JSON object — refusing to touch it.")
    return data


def _group_commands(group):
    """The command strings inside one handler group (our identity for dedupe)."""
    cmds = set()
    if isinstance(group, dict):
        if group.get("command"):
            cmds.add(group["command"])
        for h in group.get("hooks", []) or []:
            if isinstance(h, dict) and h.get("command"):
                cmds.add(h["command"])
    return frozenset(cmds)


def _load_manifest_hooks(model):
    """The manifest's chosen event→handler-groups, validated against the wiki."""
    json_path = os.path.join(manifest_dir(), f"{model}.hooks.json")
    if not os.path.exists(json_path):
        sys.exit(f"no manifest yet — run `wikia hooks manifest {model}` first.")
    manifest = _load_json_file(json_path, "manifest")
    chosen = {ev: hs for ev, hs in manifest.items() if hs and not ev.startswith("_")}
    return json_path, chosen


def _resolve_target(args, model, json_path):
    target = args.file or hook_config_path(model)
    if not target:
        print(f"{model}: couldn't find a settings file in the wiki. Your manifest is "
              f"ready at {json_path}; add these hooks via the tool itself.")
        return None
    return os.path.expanduser(target)


def _write_settings(target, merged):
    """Back up the settings file, then write the merged settings."""
    parent = os.path.dirname(os.path.abspath(target))
    os.makedirs(parent, exist_ok=True)
    if os.path.exists(target):
        backup = target + ".bak-cli-wikia"
        shutil.copy2(target, backup)
        print(f"backup saved: {backup}")
    with open(target, "w", encoding="utf-8") as f:
        f.write(json.dumps(merged, indent=2) + "\n")


def cmd_apply(args):
    model = _resolve(args.model)
    if not has_hook_system(model):
        sys.exit(f"{model}'s wiki documents no hook system to apply to.")
    json_path, chosen = _load_manifest_hooks(model)
    if not chosen:
        print(f"{model}: manifest is empty — add hooks in {json_path} first.")
        return
    known = set(hook_events(model))
    if known:  # only validate when the wiki actually enumerates events
        bad = [ev for ev in chosen if ev not in known]
        if bad:
            sys.exit(f"event(s) not in {model}'s wiki: {', '.join(bad)}")
    target = _resolve_target(args, model, json_path)
    if not target:
        return
    print(f"target settings file: {target}")
    current = _load_json_file(target, "settings file") if os.path.exists(target) else {}
    merged = dict(current)
    hooks = merged.setdefault("hooks", {})
    added = 0
    for ev, handlers in chosen.items():
        existing = hooks.get(ev)
        if not isinstance(existing, list):
            existing = []
        have = set()
        for g in existing:
            have |= _group_commands(g)
        for g in handlers:
            gc = _group_commands(g)
            if gc and gc <= have:
                continue  # already installed — keep the user's copy
            existing.append(g)  # verbatim — the tool's own handler schema
            have |= gc
            added += 1
        hooks[ev] = existing
    preview = json.dumps(merged, indent=2)
    if not args.write:
        print(f"[dry-run] would merge {len(chosen)} event(s) ({added} new handler group(s)) into: {target}")
        print("--- resulting file ---")
        print(preview[:2000] + ("\n…" if len(preview) > 2000 else ""))
        print("\nre-run with --write to install.")
        return
    _write_settings(target, merged)
    print(f"{model}: merged {len(chosen)} hook event(s) ({added} new handler group(s)) into {target}")


def cmd_unapply(args):
    """Remove exactly the handler groups our manifest installed (by command string)."""
    model = _resolve(args.model)
    json_path, chosen = _load_manifest_hooks(model)
    ours = set()
    for handlers in chosen.values():
        for g in handlers:
            ours |= _group_commands(g)
    if not ours:
        print(f"{model}: manifest at {json_path} defines no commands — nothing to remove.")
        return
    target = _resolve_target(args, model, json_path)
    if not target:
        return
    print(f"target settings file: {target}")
    if not os.path.exists(target):
        print(f"{model}: {target} does not exist — nothing to remove.")
        return
    current = _load_json_file(target, "settings file")
    hooks = current.get("hooks")
    removed = 0
    if isinstance(hooks, dict):
        for ev in list(hooks):
            groups = hooks[ev]
            if not isinstance(groups, list):
                continue
            kept = [g for g in groups
                    if not (_group_commands(g) and _group_commands(g) <= ours)]
            removed += len(groups) - len(kept)
            if kept:
                hooks[ev] = kept
            else:
                del hooks[ev]
    if not removed:
        print(f"{model}: no cli-wikia-installed hooks found in {target}.")
        return
    if not args.write:
        print(f"[dry-run] would remove {removed} handler group(s) from: {target}")
        print("\nre-run with --write to remove.")
        return
    _write_settings(target, current)
    print(f"{model}: removed {removed} handler group(s) from {target}")


def cmd_status(args):
    models = MODELS if (args.all or not args.model) else [_resolve(args.model)]
    for m in models:
        if has_hook_system(m):
            n = len(hook_events(m))
            hooks = f"yes ({n} events)" if n else "yes (events n/a)"
        else:
            hooks = "no"
        ipath = _instruction_path(m)
        aware = "no" if os.path.exists(ipath) else "—"
        if os.path.exists(ipath) and MARK_START in _read_text(ipath):
            aware = "installed"
        man = "yes" if os.path.exists(os.path.join(manifest_dir(), f"{m}.hooks.json")) else "no"
        print(f"{m:12} hooks: {hooks:16} L1({ipath}): {aware:9} L2-manifest: {man}")


# --------------------------------------------------------------------------- #
def _read_text(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def _resolve(model):
    if model not in MODELS:
        sys.exit(f"unknown model '{model}'. choose from: {', '.join(MODELS)}")
    return model
