"""Command-line interface for cli-wikia.

A small, dependency-free CLI to browse, search, read and edit an offline
reference wiki for AI coding CLIs. Run `wikia --help` for usage.
"""
from __future__ import annotations

import argparse
import difflib
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from importlib import resources

from . import MODELS, __version__

# Which installed CLI can answer questions / provide updates for each model.
MODEL_CLIS = {
    "claude": "claude",
    "deepseek": "deepseek-code",
    "copilot": "copilot",
    "chatgpt": "codex",  # OpenAI Codex CLI (may not be installed yet)
    "gemini": "gemini",
    "antigravity": "agy",  # Google Antigravity CLI
}

# Sources the `update` command checks for changes, per model. The real signal
# comes from (1) the official docs and (2) asking the model itself — NOT a
# `--help` dump. `version` is just a cheap authoritative version string.
#  - version: read-only version probe (no side effects).
#  - docs: official documentation URL (best-effort; edit if a tool moves its docs).
#  - ask: argv template to query the model in one-shot mode; "{q}" = the question.
#         None means the model can't be queried that way (e.g. tool not installed).
MODEL_SOURCES = {
    "claude": {
        "version": ["--version"],
        "docs": "https://docs.claude.com/en/docs/claude-code/overview",
        "ask": ["-p", "{q}"],
    },
    "deepseek": {
        "version": ["--version"],
        "docs": "https://api-docs.deepseek.com/",
        "ask": ["-p", "{q}"],
    },
    "copilot": {
        "version": ["--version"],
        "docs": "https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli",
        "ask": ["-p", "{q}", "--allow-all-tools"],
    },
    "chatgpt": {
        "version": ["--version"],
        "docs": "https://developers.openai.com/codex/cli/",
        "ask": None,  # codex isn't installed; openai CLI isn't a one-shot agent
    },
    "gemini": {
        "version": ["--version"],
        "docs": "https://google-gemini.github.io/gemini-cli/",
        "ask": ["-p", "{q}"],
    },
    "antigravity": {
        "version": ["--version"],
        "docs": "https://antigravity.google/docs",
        "ask": ["-p", "{q}"],
    },
}

# What `update` asks each model about itself.
WHATS_NEW_Q = (
    "What is your exact version, and what are your most recent features, "
    "commands, or changes? Be specific and concise."
)


def wikis_root():
    """Filesystem path to the bundled wikis/ directory."""
    return resources.files("cli_wikia") / "wikis"


def model_dir(model):
    return wikis_root() / model


def topics(model):
    """Sorted list of topic names (filenames without .md) for a model."""
    d = model_dir(model)
    if not d.is_dir():
        return []
    return sorted(p.name[:-3] for p in d.iterdir() if p.name.endswith(".md"))


def resolve_model(model):
    if model not in MODELS:
        sys.exit(f"unknown model '{model}'. choose from: {', '.join(MODELS)}")
    return model


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #
def cmd_models(args):
    for m in MODELS:
        n = len(topics(m))
        cli = MODEL_CLIS.get(m)
        cli_state = f"cli: {cli}" if cli and shutil.which(cli) else "cli: not installed"
        print(f"{m:12} {n:3} topics   ({cli_state})")


def cmd_list(args):
    models = [resolve_model(args.model)] if args.model else MODELS
    for m in models:
        ts = topics(m)
        print(f"\n# {m} ({len(ts)} topics)")
        for t in ts:
            print(f"  {t}")


def cmd_read(args):
    m = resolve_model(args.model)
    f = model_dir(m) / f"{args.topic}.md"
    if not f.is_file():
        avail = ", ".join(topics(m)) or "(none yet)"
        sys.exit(f"no topic '{args.topic}' in {m}.\navailable: {avail}")
    sys.stdout.write(f.read_text(encoding="utf-8"))


def cmd_search(args):
    needle = args.query.lower()
    models = [resolve_model(args.model)] if args.model else MODELS
    hits = 0
    for m in models:
        d = model_dir(m)
        if not d.is_dir():
            continue
        for p in sorted(d.iterdir(), key=lambda x: x.name):
            if not p.name.endswith(".md"):
                continue
            for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if needle in line.lower():
                    hits += 1
                    print(f"{m}/{p.name[:-3]}:{i}: {line.strip()}")
    if not hits:
        print(f"no matches for '{args.query}'")


def cmd_path(args):
    if args.model:
        print(model_dir(resolve_model(args.model)))
    else:
        print(wikis_root())


def cmd_ask(args):
    """Use a local model CLI to answer a question grounded in the wiki docs."""
    m = resolve_model(args.model)
    cli = MODEL_CLIS.get(m)
    runner = cli if (cli and shutil.which(cli)) else ("ollama" if shutil.which("ollama") else None)
    if not runner:
        sys.exit(
            "no local model CLI available to answer. install one of: "
            f"{cli or 'ollama'}, or read the docs with `wikia read {m} <topic>`."
        )
    # Build context from the model's docs (capped to keep the prompt sane).
    context = ""
    for t in topics(m):
        context += f"\n\n## {t}\n" + (model_dir(m) / f"{t}.md").read_text(encoding="utf-8")
    context = context[: args.max_context]
    prompt = (
        "Answer the question using ONLY the reference docs below. "
        "If the answer is not in them, say so.\n"
        f"=== REFERENCE DOCS ({m}) ===\n{context}\n=== QUESTION ===\n{args.question}\n"
    )
    print(f"(asking via: {runner})\n", file=sys.stderr)
    try:
        if runner == "ollama":
            subprocess.run(["ollama", "run", args.ollama_model, prompt], check=False)
        else:
            subprocess.run([runner, prompt], check=False)
    except FileNotFoundError:
        sys.exit(f"could not run '{runner}'.")


def snapshot_dir():
    """Writable per-user dir where CLI ground-truth snapshots are stored."""
    base = os.environ.get("XDG_STATE_HOME") or os.path.join(
        os.path.expanduser("~"), ".local", "state"
    )
    return os.path.join(base, "cli-wikia", "snapshots")


def _run_cli(cli, probe, timeout=30):
    """Run one read-only CLI probe and return its labelled output."""
    try:
        r = subprocess.run(
            [cli, *probe],
            capture_output=True,
            text=True,
            timeout=timeout,
            stdin=subprocess.DEVNULL,
        )
        return f"$ {cli} {' '.join(probe)}\n{r.stdout}{r.stderr}".strip()
    except (subprocess.TimeoutExpired, OSError) as e:
        return f"$ {cli} {' '.join(probe)}\n<error: {e}>"


def fetch_docs(url):
    """Fetch an official docs page and reduce it to text for change detection.

    Uses only the standard library. Returns a text block, or an error note if
    offline / the page is unreachable (so update still works offline).
    """
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "cli-wikia/update"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read(500_000).decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001 - network can fail many ways; degrade gracefully
        return f"# docs: {url}\n<unreachable: {e}>"
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return f"# docs: {url}\n{text[:8000]}"


def query_model(cli, ask_template, question):
    """Ask the model itself, in one-shot mode, via its per-model invocation."""
    if not ask_template:
        return None
    argv = [question if tok == "{q}" else tok for tok in ask_template]
    out = _run_cli(cli, argv, timeout=180)  # models take a while
    return "# model self-report (the model's own answer about itself):\n" + out


def capture_sources(m, cli, use_docs, use_model):
    """Gather ALL THREE sources for a model into one snapshot blob:
    (1) the CLI's own facts (version + help), (2) the official docs, and
    (3) the model's self-report. Docs and the model are the real depth; help is
    the factual cross-check. Use --no-docs / --no-model to drop a source."""
    src = MODEL_SOURCES.get(m, {})
    parts = [
        _run_cli(cli, src.get("version", ["--version"])),
        _run_cli(cli, ["--help"]),
    ]
    if use_docs and src.get("docs"):
        parts.append(fetch_docs(src["docs"]))
    if use_model and src.get("ask"):
        mq = query_model(cli, src["ask"], WHATS_NEW_Q)
        if mq:
            parts.append(mq)
    return "\n\n".join(p for p in parts if p) + "\n"


def cmd_update(args):
    """Check each model's sources (CLI --help/--version, official docs, and
    optionally the model itself) for changes vs the last saved snapshot.

    Reports what changed so curated docs can be refreshed. No API keys. Never
    overwrites the curated .md files; snapshots live in the user state dir.
    """
    if not args.all and not args.model:
        sys.exit("specify a model (e.g. `wikia update gemini`) or use `--all`.")
    models = MODELS if args.all else [resolve_model(args.model)]
    use_docs = not args.no_docs
    use_model = not args.no_model
    sdir = snapshot_dir()
    os.makedirs(sdir, exist_ok=True)
    changed_any = False
    for m in models:
        cli = MODEL_CLIS.get(m)
        if not cli:
            print(f"{m:12} no associated CLI — skip")
            continue
        if not shutil.which(cli):
            print(f"{m:12} '{cli}' not installed — can't check for updates")
            continue
        sources = "help/version" + (" + docs" if use_docs else "") + (" + model" if use_model else "")
        current = capture_sources(m, cli, use_docs, use_model)
        snap = os.path.join(sdir, f"{m}.txt")
        if not os.path.exists(snap):
            with open(snap, "w", encoding="utf-8") as f:
                f.write(current)
            print(f"{m:12} baseline snapshot saved ({sources}). Run again later to detect changes.")
            continue
        with open(snap, encoding="utf-8") as f:
            prev = f.read()
        if prev == current:
            print(f"{m:12} up to date ({sources}, no change)")
            continue
        changed_any = True
        diff = [
            ln
            for ln in difflib.unified_diff(
                prev.splitlines(), current.splitlines(), lineterm="", n=0
            )
            if ln and ln[0] in "+-" and not ln.startswith(("+++", "---"))
        ]
        print(f"{m:12} CHANGED ({sources}) — {len(diff)} differing lines:")
        for ln in diff[:30]:
            print(f"             {ln}")
        if len(diff) > 30:
            print(f"             … (+{len(diff) - 30} more)")
        print(f"             review/update curated docs in: {model_dir(m)}")
        if args.write:
            with open(snap, "w", encoding="utf-8") as f:
                f.write(current)
            print(f"             snapshot updated (acknowledged).")
        else:
            print(f"             re-run with --write to accept this as the new baseline.")
    if changed_any and not args.write:
        print("\nTip: `wikia update --all --write` after you've refreshed the docs.")


def build_parser():
    p = argparse.ArgumentParser(
        prog="wikia",
        description="Offline reference wiki for AI coding CLIs "
        "(claude, deepseek, copilot, chatgpt, gemini).",
    )
    p.add_argument("--version", action="version", version=f"cli-wikia {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("models", help="list models and how many topics each has").set_defaults(func=cmd_models)

    sp = sub.add_parser("list", help="list topics (optionally for one model)")
    sp.add_argument("model", nargs="?", help="model name (default: all)")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("read", help="print a topic")
    sp.add_argument("model")
    sp.add_argument("topic")
    sp.set_defaults(func=cmd_read)

    sp = sub.add_parser("search", help="search text across topics")
    sp.add_argument("query")
    sp.add_argument("--model", help="limit to one model")
    sp.set_defaults(func=cmd_search)

    sp = sub.add_parser("path", help="print the on-disk path (for editing files)")
    sp.add_argument("model", nargs="?")
    sp.set_defaults(func=cmd_path)

    sp = sub.add_parser("ask", help="ask a question answered from the docs via a local model")
    sp.add_argument("model")
    sp.add_argument("question")
    sp.add_argument("--ollama-model", default="llama3", help="ollama model to use as fallback")
    sp.add_argument("--max-context", type=int, default=24000, help="max chars of docs to feed")
    sp.set_defaults(func=cmd_ask)

    sp = sub.add_parser("update", help="check a model's sources (help, docs, model) for changes")
    sp.add_argument("model", nargs="?", help="model name (omit and use --all for every model)")
    sp.add_argument("--all", action="store_true", help="check every model")
    sp.add_argument("--write", action="store_true", help="accept current state as the new baseline")
    sp.add_argument("--no-docs", action="store_true", help="skip fetching official docs (offline / faster)")
    sp.add_argument("--no-model", action="store_true", help="skip asking the model itself (faster)")
    sp.set_defaults(func=cmd_update)

    # hooks (Level 1 awareness + Level 2 tailored hooks) — see hooks.py
    from . import hooks as H

    hp = sub.add_parser("hooks", help="integrate the wiki into a model (awareness + real hooks)")
    hsub = hp.add_subparsers(dest="hooks_cmd", required=True)

    s = hsub.add_parser("status", help="show integration status per model")
    s.add_argument("model", nargs="?")
    s.add_argument("--all", action="store_true")
    s.set_defaults(func=H.cmd_status)

    s = hsub.add_parser("enable", help="Level 1: tell a model the wiki exists (dry-run unless --write)")
    s.add_argument("model")
    s.add_argument("--file", help="instructions file to write (default: per-model convention)")
    s.add_argument("--write", action="store_true", help="actually write the change")
    s.set_defaults(func=H.cmd_enable)

    s = hsub.add_parser("disable", help="Level 1: remove the wiki awareness block")
    s.add_argument("model")
    s.add_argument("--file")
    s.add_argument("--write", action="store_true")
    s.set_defaults(func=H.cmd_disable)

    s = hsub.add_parser("manifest", help="Level 2: generate the hook-positions doc from the wiki")
    s.add_argument("model")
    s.set_defaults(func=H.cmd_manifest)

    s = hsub.add_parser("apply", help="Level 2: install the edited hooks (dry-run unless --write)")
    s.add_argument("model")
    s.add_argument("--file", help="target settings file (default: per-model)")
    s.add_argument("--write", action="store_true", help="actually install the hooks")
    s.set_defaults(func=H.cmd_apply)

    # schedule — config-driven auto-update timer (see schedule.py)
    from . import schedule as S

    sc = sub.add_parser("schedule", help="auto-update on a timer, configured via a file")
    scsub = sc.add_subparsers(dest="schedule_cmd", required=True)

    c = scsub.add_parser("config", help="create/show the schedule config file (pick interval here)")
    c.add_argument("--write", action="store_true", help="create the config file")
    c.set_defaults(func=S.cmd_config)

    c = scsub.add_parser("apply", help="make the timer match the config (dry-run unless --write)")
    c.add_argument("--write", action="store_true", help="actually install/remove the timer")
    c.set_defaults(func=S.cmd_apply)

    c = scsub.add_parser("status", help="show config + installed timer")
    c.set_defaults(func=S.cmd_status)

    c = scsub.add_parser("remove", help="remove the scheduled timer (dry-run unless --write)")
    c.add_argument("--write", action="store_true", help="actually remove")
    c.set_defaults(func=S.cmd_remove)

    return p


def main(argv=None):
    # Behave like a normal Unix tool when output is piped into `head`/`less`
    # and the reader closes early: die quietly instead of dumping a traceback.
    try:
        import signal

        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError):
        pass  # SIGPIPE not available (e.g. Windows)
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
