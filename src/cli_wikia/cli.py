"""Command-line interface for cli-wikia.

A small, dependency-free CLI to browse, search, read and edit an offline
reference wiki for AI coding CLIs. Run `wikia --help` for usage.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from importlib import resources

from . import MODELS, __version__

# Which installed CLI can answer questions / provide updates for each model.
MODEL_CLIS = {
    "claude": "claude",
    "deepseek": "deepseek-code",
    "copilot": "copilot",
    "chatgpt": None,  # no local CLI; docs only
    "gemini": "gemini",
}


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
        print(f"{m:10} {n:3} topics   ({cli_state})")


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


def cmd_update(args):
    """Phase 2 placeholder: refresh a model's docs from its source."""
    m = resolve_model(args.model)
    cli = MODEL_CLIS.get(m)
    print(
        f"update for '{m}' is not implemented yet.\n"
        f"planned source: {cli + ' CLI' if cli else 'official online docs'}.\n"
        f"for now, edit files directly: {model_dir(m)}"
    )


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

    sp = sub.add_parser("update", help="(phase 2) refresh a model's docs from its source")
    sp.add_argument("model")
    sp.set_defaults(func=cmd_update)

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
