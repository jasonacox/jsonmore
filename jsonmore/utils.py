"""
jsonmore - Utility functions for terminal handling and paging

Utility functions including:
- Paging support for long output (less, more, etc.)
- Terminal size detection and handling
- Cross-platform compatibility helpers

Requirements:
- Python 3.8+ (uses f-strings and subprocess)
- Standard library only (os, shutil, subprocess)

Author: Jason Cox
Date: July 2, 2025
Repository: https://github.com/jasonacox/jsonmore
"""

import os
import shutil
import subprocess
from typing import Optional


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
    """Display text with pagination if needed"""
    if not use_pager:
        print(text)
        return

    # Get terminal height
    try:
        terminal_height = shutil.get_terminal_size().lines
    except OSError:
        terminal_height = 24  # Default fallback

    # Count lines in output
    lines = text.split("\n")

    # If output is short enough, just print it
    if len(lines) <= terminal_height - 2:  # Leave some margin
        print(text)
        return

    # Use pager for long output
    pager = get_pager()
    if pager and pager != "cat":
        try:
            # Set up pager with appropriate options
            if pager == "less":
                # Use less with options: -R (raw color codes), -F (quit if fits on screen), -X (no init)
                proc = subprocess.Popen(
                    ["less", "-RFX"], stdin=subprocess.PIPE, text=True
                )
            else:  # 'more' or other pager
                proc = subprocess.Popen([pager], stdin=subprocess.PIPE, text=True)

            proc.communicate(input=text)
            return
        except (subprocess.SubprocessError, FileNotFoundError):
            # Fall back to direct output if pager fails
            pass

    # Fallback: print directly
    print(text)
