"""
jsonmore - Module entry point for command line execution

This file enables running jsonmore as a module:
    python -m jsonmore <file.json>

The module execution delegates to the CLI main function for
consistent behavior across different invocation methods.

Requirements:
- Python 3.8+ (uses f-strings)
- jsonmore.cli module for command line interface

Author: Jason Cox
Date: July 2, 2025
Repository: https://github.com/jasonacox/jsonmore
"""

from .cli import main

if __name__ == "__main__":
    main()
