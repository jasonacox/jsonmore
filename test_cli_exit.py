"""Regression tests: CLI exit status and keeping stdout clean for piping."""

import json
import os
import subprocess
import sys
import tempfile

import pytest


def run(args, stdin=None):
    return subprocess.run(
        [sys.executable, "-m", "jsonmore", "--no-pager", "--no-colors", *args],
        input=stdin,
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )


@pytest.fixture
def good_file():
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        f.write('{"a": 1}')
    yield f.name
    os.unlink(f.name)


def test_missing_file_exits_nonzero():
    r = run(["/nonexistent/definitely-missing.json"])
    assert r.returncode == 1
    assert "File not found" in r.stderr


def test_one_missing_file_among_many_exits_nonzero(good_file):
    r = run([good_file, "/nonexistent/definitely-missing.json"])
    assert r.returncode == 1
    assert '"a": 1' in r.stdout


def test_invalid_json_with_no_repair_exits_nonzero(good_file):
    with open(good_file, "w") as f:
        f.write("{bad")
    r = run([good_file, "--no-repair"])
    assert r.returncode == 1


def test_valid_file_exits_zero(good_file):
    r = run([good_file])
    assert r.returncode == 0


def test_repaired_output_on_stdout_is_valid_json():
    r = run([], stdin='{"a": 1, "b": [1, 2,],}')
    assert r.returncode == 0
    assert json.loads(r.stdout) == {"a": 1, "b": [1, 2]}
    assert "repair" in r.stderr.lower()
