"""
jsonmore - Utility functions for terminal handling and paging

Utility functions including:
- Paging support for long output (less, more, etc.)
- Terminal size detection and handling
- Cross-platform compatibility helpers

Requirements:
- Python 3.8+ (uses f-strings and subprocess)
- colorama for cross-platform color support
- Standard library (os, shutil, subprocess)

Author: Jason Cox
Date: July 2, 2025
Repository: https://github.com/jasonacox/jsonmore
"""

import os
import shutil
import sys
from typing import Optional

# Ensure colorama is initialized for Windows terminals
from colorama import init

from .pager import page

init(strip=(not sys.stdout.isatty()))


def get_pager() -> Optional[str]:
    """Get the preferred pager command"""
    # Check for user preference in environment
    pager = os.environ.get("PAGER")
    if pager and shutil.which(pager):
        return pager

    # Try common pagers in order of preference
    for cmd in ["less", "more", "cat"]:
        if shutil.which(cmd):
            return cmd

    return None


def paginate_output(text: str, use_pager: bool = True) -> None:
    """Display text with pagination if needed (cross-platform, color-friendly)."""
    # Only use pager if output is a TTY (terminal)
    if not use_pager or not sys.stdout.isatty():
        print(text)
        return

    # If input is not a TTY (e.g., piped), use a simple pager (space/enter only), reading navigation from /dev/tty in raw mode only for keypress
    if not sys.stdin.isatty():
        lines = text.splitlines()
        height = shutil.get_terminal_size().lines - 1 if sys.stdout.isatty() else 24
        pos = 0
        tty_in = None
        try:
            tty_in = open("/dev/tty")
            import termios
            import tty as ttymod

            fd = tty_in.fileno()
            old_settings = termios.tcgetattr(fd)

            def getch() -> str:
                # Switch to raw mode, read one char, restore mode
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                try:
                    ttymod.setraw(fd)
                    ch = tty_in.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch

            while pos < len(lines):
                end = min(pos + height, len(lines))
                for i in range(pos, end):
                    print(lines[i])
                if end >= len(lines):
                    print("(END) ", end="", flush=True)
                    if tty_in:
                        ch = getch()
                    else:
                        break
                    print()
                    break
                print(":", end="", flush=True)
                if tty_in:
                    ch = getch()
                else:
                    break
                if ch == "q":
                    print()
                    break
                elif ch == " ":
                    pos += height
                elif ch in ("\r", "\n"):
                    pos += 1
                else:
                    pos += 1
        except OSError:
            # If /dev/tty or termios fails, just print all
            print("\n".join(lines))
        finally:
            if tty_in:
                tty_in.close()
        return

    # Otherwise, use the full-featured pager
    page(text)
