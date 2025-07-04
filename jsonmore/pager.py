import sys
import shutil


class Pager:
    """
    Cross-platform, color-friendly pager for terminal output.
    - Supports ANSI color codes.
    - Prompts with ':' for navigation: space (page), enter (line), up/down arrows.
    - At end, displays (END) and quits on any key.
    """

    def __init__(self, text: str):
        self.lines = text.splitlines()
        self.term_height = self._get_terminal_height()
        self.term_width = self._get_terminal_width()
        self.pos = 0

    def _get_terminal_height(self) -> int:
        try:
            return shutil.get_terminal_size().lines
        except Exception:
            return 24

    def _get_terminal_width(self) -> int:
        try:
            return shutil.get_terminal_size().columns
        except Exception:
            return 80

    def _getch(self) -> str:
        # Cross-platform single char input
        try:
            import termios
            import tty

            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
            return ch
        except ImportError:
            # Windows
            import msvcrt

            return msvcrt.getch().decode(errors="ignore") if msvcrt else ""  # type: ignore[attr-defined]
        except Exception:
            # Fallback: return empty string if getch fails
            return ""

    def _get_arrow(self) -> str:
        # Detect arrow keys (returns 'up', 'down', or None)
        ch = self._getch()
        if ch == "\x1b":  # ANSI escape
            next1 = self._getch()
            if next1 == "[":
                next2 = self._getch()
                if next2 == "A":
                    return "up"
                elif next2 == "B":
                    return "down"
            return ""  # If escape sequence is incomplete, return empty string
        return ch

    def show(self) -> None:
        lines = self.lines
        height = self.term_height - 1  # Leave room for prompt
        pos = 0
        while True:
            end = min(pos + height, len(lines))
            for i in range(pos, end):
                print(lines[i])
            if end >= len(lines):
                print("(END) ", end="", flush=True)
                self._getch()
                print()
                break
            print(":", end="", flush=True)
            ch = self._getch()
            print(
                "\r" + " " * (self.term_width - 1) + "\r", end="", flush=True
            )  # Clear line
            if ch == "q":
                print()
                break
            elif ch == " ":
                pos = min(
                    pos + height, len(lines) - height if len(lines) > height else 0
                )
            elif ch in ("\r", "\n"):
                pos = min(pos + 1, len(lines) - height if len(lines) > height else 0)
            else:
                arrow = ch if ch not in ("\x1b",) else self._get_arrow()
                if arrow == "down":
                    pos = min(
                        pos + 1, len(lines) - height if len(lines) > height else 0
                    )
                elif arrow == "up":
                    pos = max(0, pos - 1)
                else:
                    pos = min(
                        pos + 1, len(lines) - height if len(lines) > height else 0
                    )


def page(text: str) -> None:
    Pager(text).show()
