"""Archived wiki versions ship in the package and are readable.

Every model keeps versions/<N>/ snapshots + versions.json; `wikia versions`
lists them and `wikia read --as-of N` reads old pages. Current commands
(list/read/search/models) only ever see the flat latest pages.
"""
import json

import pytest

from cli_wikia import cli
from cli_wikia.cli import model_dir, model_versions


def test_every_model_has_v1_archive():
    for m in cli.MODELS:
        vs = model_versions(m)
        assert vs, f"{m} has no archived versions"
        assert vs[0]["version"] == 1
        vdir = model_dir(m) / "versions" / "1"
        assert vdir.is_dir(), m
        assert (vdir / "README.md").is_file(), m


def test_versions_manifest_shape():
    for m in cli.MODELS:
        mf = model_dir(m) / "versions.json"
        data = json.loads(mf.read_text(encoding="utf-8"))
        assert isinstance(data.get("versions"), list) and data["versions"], m
        for e in data["versions"]:
            assert isinstance(e.get("version"), int), m
            assert e.get("date"), m


def test_read_as_of_returns_archived_page(capsys):
    cli.cmd_read(_args("muse", "README", as_of="1"))
    out = capsys.readouterr().out
    assert "Muse Code" in out
    archived = (model_dir("muse") / "versions" / "1" / "README.md").read_text(encoding="utf-8")
    assert out.strip() == archived.strip()


def test_read_as_of_unknown_version_errors():
    with pytest.raises(SystemExit) as exc:
        cli.cmd_read(_args("muse", "README", as_of="999"))
    assert "unknown version" in str(exc.value)


def test_archives_invisible_to_current_commands():
    assert "1" not in cli.topics("muse")
    assert "versions" not in cli.topics("muse")


def _args(model, topic, as_of=None):
    import types

    return types.SimpleNamespace(model=model, topic=topic, as_of=as_of)
