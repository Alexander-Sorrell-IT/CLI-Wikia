"""CLI read/list/models commands (from package data) and the `ask` one-shot path."""
from types import SimpleNamespace

from cli_wikia import cli


def test_models_lists_all_from_package_data(capsys):
    cli.cmd_models(SimpleNamespace())
    out = capsys.readouterr().out
    for m in ("claude", "gemini", "copilot"):
        assert m in out
    assert "topics" in out


def test_list_topics_for_one_model(capsys):
    cli.cmd_list(SimpleNamespace(model="claude"))
    out = capsys.readouterr().out
    assert "# claude" in out
    assert "hooks" in out  # claude ships a hooks topic


def test_read_topic_prints_file_contents(capsys):
    cli.cmd_read(SimpleNamespace(model="claude", topic="hooks"))
    out = capsys.readouterr().out
    assert out.strip()  # non-empty topic body


def test_ask_uses_oneshot_template(monkeypatch, capsys):
    recorded = {}

    def fake_run(argv, **kwargs):
        recorded["argv"] = argv
        return SimpleNamespace(returncode=0)

    # claude's CLI is "present" and is chosen as the runner.
    monkeypatch.setattr(cli.shutil, "which", lambda name: "/usr/bin/claude" if name == "claude" else None)
    monkeypatch.setattr(cli.subprocess, "run", fake_run)

    args = SimpleNamespace(
        model="claude",
        question="How do hooks work?",
        ollama_model="llama3",
        max_context=24000,
    )
    cli.cmd_ask(args)

    argv = recorded["argv"]
    # one-shot template for claude is ["-p", "{q}"] → claude -p <prompt>
    assert argv[0] == "claude"
    assert argv[1] == "-p"
    prompt = argv[2]
    assert "How do hooks work?" in prompt
    assert "REFERENCE DOCS" in prompt
