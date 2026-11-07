"""Regression tests: arrow keys in the built-in pager."""

from unittest.mock import patch

from jsonmore.pager import Pager


def first_lines_drawn(keys, capsys, total=50, height=11):
    """Run the pager with scripted keypresses; return first line of each redraw."""
    pager = Pager("\n".join(f"line{i}" for i in range(total)))
    pager.term_height = height  # 10 content lines + prompt
    keys = iter(keys)
    with patch.object(Pager, "_getch", lambda self: next(keys)):
        pager.show()
    printed = [ln.strip("\r :") for ln in capsys.readouterr().out.splitlines()]
    printed = [ln for ln in printed if ln.startswith("line")]
    # each redraw prints 10 lines
    return [printed[i] for i in range(0, len(printed), 10)]


def test_up_arrow_scrolls_up_one_line(capsys):
    # space -> page down (pos 10), up arrow -> pos 9, quit
    assert first_lines_drawn([" ", "\x1b", "[", "A", "q"], capsys) == [
        "line0",
        "line10",
        "line9",
    ]


def test_down_arrow_scrolls_down_one_line(capsys):
    assert first_lines_drawn(["\x1b", "[", "B", "q"], capsys) == ["line0", "line1"]
