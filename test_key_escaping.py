"""Regression tests: object keys must be JSON-escaped in formatted output."""

import json

from jsonmore import JSONFormatter


def test_keys_with_special_characters_round_trip():
    data = {'quote"key': 1, "back\\slash": 2, "new\nline": 3, "tab\t": 4}
    out = JSONFormatter(use_colors=False).format_json(data)
    assert json.loads(out) == data


def test_nested_keys_are_escaped():
    data = {"outer": {'in"ner': [{"a\\b": None}]}}
    out = JSONFormatter(use_colors=False, indent=4).format_json(data)
    assert json.loads(out) == data


def test_plain_keys_unchanged():
    out = JSONFormatter(use_colors=False).format_json({"name": "x"})
    assert out == '{\n  "name": "x"\n}'


def test_non_ascii_is_displayed_not_escaped():
    data = {"név": "café ☕"}
    out = JSONFormatter(use_colors=False).format_json(data)
    assert out == '{\n  "név": "café ☕"\n}'
    assert json.loads(out) == data
