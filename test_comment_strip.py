"""Regression tests: comment removal during repair must not touch string contents."""

import json

from jsonmore.core import JSONRepair


def test_url_in_string_survives_repair():
    bad = '{"url": "http://example.com/a", "n": 1,}'
    assert json.loads(JSONRepair.attempt_repair(bad)) == {
        "url": "http://example.com/a",
        "n": 1,
    }


def test_block_comment_markers_in_string_survive():
    bad = '{"glob": "src/*.py", "end": "*/", "x": 1,}'
    assert json.loads(JSONRepair.attempt_repair(bad)) == {
        "glob": "src/*.py",
        "end": "*/",
        "x": 1,
    }


def test_real_comments_still_removed():
    bad = '{\n  // line comment\n  "a": 1, /* block\n comment */ "b": "x//y"\n}'
    assert json.loads(JSONRepair.attempt_repair(bad)) == {"a": 1, "b": "x//y"}


def test_escaped_quote_inside_string():
    bad = '{"s": "say \\"hi\\" // not a comment", "t": 2,} // trailing'
    assert json.loads(JSONRepair.attempt_repair(bad)) == {
        "s": 'say "hi" // not a comment',
        "t": 2,
    }
