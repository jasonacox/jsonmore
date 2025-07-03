"""
jsonmore - Color definitions for terminal output

Cross-platform color codes and formatting definitions for colorized terminal output.
Uses colorama for Windows compatibility and consistent color display.

Features:
- Cross-platform color support via colorama
- Standard color codes (black, red, green, yellow, blue, magenta, cyan, white)
- Bright/bold color variants
- Reset and formatting codes (bold, dim)

Requirements:
- Python 3.8+
- colorama for cross-platform color support

Author: Jason Cox
Date: July 2, 2025
Repository: https://github.com/jasonacox/jsonmore
"""

from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
# autoreset=True means colors reset after each print
init(autoreset=True)


class Colors:
    """Cross-platform color codes for terminal output using colorama"""

    # Reset and formatting
    RESET = Style.RESET_ALL
    BOLD = Style.BRIGHT
    DIM = Style.DIM

    # Regular colors using colorama
    BLACK = Fore.BLACK
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE

    # Bright colors using colorama's bright variants
    BRIGHT_BLACK = Fore.LIGHTBLACK_EX
    BRIGHT_RED = Fore.LIGHTRED_EX
    BRIGHT_GREEN = Fore.LIGHTGREEN_EX
    BRIGHT_YELLOW = Fore.LIGHTYELLOW_EX
    BRIGHT_BLUE = Fore.LIGHTBLUE_EX
    BRIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX
    BRIGHT_CYAN = Fore.LIGHTCYAN_EX
    BRIGHT_WHITE = Fore.LIGHTWHITE_EX
