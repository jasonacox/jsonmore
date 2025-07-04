"""
jsonmore - A powerful JSON file reader with formatting, repair, and analysis capabilities

This package provides tools for reading, formatting, and analyzing JSON files with:
- Beautiful syntax highlighting
- Automatic error repair
- Smart paging
- Structure analysis

Requirements:
- Python 3.8+ (uses f-strings and type hints)
- Standard library only (json, re, pathlib, subprocess, etc.)

Author: Jason Cox
Date: July 2, 2025
Repository: https://github.com/jasonacox/jsonmore
"""

__version__ = "1.0.2"
__author__ = "Jason Cox"
__description__ = (
    "A powerful JSON file reader with formatting, repair, and analysis capabilities"
)

from .core import JSONReader, JSONFormatter, JSONRepair
from .colors import Colors
from .utils import paginate_output, get_pager

__all__ = [
    "JSONReader",
    "JSONFormatter",
    "JSONRepair",
    "Colors",
    "paginate_output",
    "get_pager",
]
