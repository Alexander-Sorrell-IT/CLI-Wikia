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
import sys

from . import MODELS

MARK_START = "<!-- cli-wikia:start -->"
MARK_END = "<!-- cli-wikia:end -->"

# Known custom-instruction filenames to look for when scanning a wiki. This is a
# list of conventions to RECOGNIZE, not a per-model mapping — the wiki decides
# which one applies to each tool.
INSTRUCTION_CANDIDATES = [
    "CLAUDE.md", "GEMINI.md", "AGENTS.md",
    ".github/copilot-instructions.md", "QWEN.md", "codex.md",
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


def hook_config_path(model):
    """Where this tool stores hooks/settings — extracted from its wiki text."""
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


def cmd_enable(args):
    model = _resolve(args.model)
    path = args.file or instruction_file(model)
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
    path = args.file or instruction_file(model)
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


def cmd_apply(args):
    model = _resolve(args.model)
    if not has_hook_system(model):
        sys.exit(f"{model}'s wiki documents no hook system to apply to.")
    json_path = os.path.join(manifest_dir(), f"{model}.hooks.json")
    if not os.path.exists(json_path):
        sys.exit(f"no manifest yet — run `wikia hooks manifest {model}` first.")
    with open(json_path, encoding="utf-8") as f:
        manifest = json.load(f)
    chosen = {ev: hs for ev, hs in manifest.items() if hs and not ev.startswith("_")}
    if not chosen:
        print(f"{model}: manifest is empty — add hooks in {json_path} first.")
        return
    known = set(hook_events(model))
    if known:  # only validate when the wiki actually enumerates events
        bad = [ev for ev in chosen if ev not in known]
        if bad:
            sys.exit(f"event(s) not in {model}'s wiki: {', '.join(bad)}")
    target = args.file or hook_config_path(model)
    if not target:
        print(f"{model}: couldn't find a settings file in the wiki. Your manifest is "
              f"ready at {json_path}; add these hooks via the tool itself.")
        return
    target = os.path.expanduser(target)
    current = {}
    if os.path.exists(target):
        with open(target, encoding="utf-8") as f:
            current = json.load(f)
    merged = dict(current)
    merged.setdefault("hooks", {})
    for ev, handlers in chosen.items():
        merged["hooks"][ev] = handlers  # verbatim — the tool's own handler schema
    preview = json.dumps(merged, indent=2)
    if not args.write:
        print(f"[dry-run] would merge {len(chosen)} event(s) into: {target}")
        print("--- resulting file ---")
        print(preview[:2000] + ("\n…" if len(preview) > 2000 else ""))
        print("\nre-run with --write to install.")
        return
    parent = os.path.dirname(os.path.abspath(target))
    os.makedirs(parent, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(preview + "\n")
    print(f"{model}: wrote {len(chosen)} hook event(s) into {target}")


def cmd_status(args):
    models = MODELS if (args.all or not args.model) else [_resolve(args.model)]
    for m in models:
        if has_hook_system(m):
            n = len(hook_events(m))
            hooks = f"yes ({n} events)" if n else "yes (events n/a)"
        else:
            hooks = "no"
        ifile = instruction_file(m)
        aware = "no" if os.path.exists(ifile) else "—"
        if os.path.exists(ifile) and MARK_START in _read_text(ifile):
            aware = "installed"
        man = "yes" if os.path.exists(os.path.join(manifest_dir(), f"{m}.hooks.json")) else "no"
        print(f"{m:12} hooks: {hooks:16} L1({ifile}): {aware:9} L2-manifest: {man}")


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
