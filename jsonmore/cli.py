"""
jsonmore - Command line interface

Command line interface for jsonmore package - handles argument parsing
and serves as the main entry point for the jsonmore CLI tool.

Features:
- Argument parsing and validation
- Error handling and user feedback
- Integration with core JSON processing modules

Requirements:
- Python 3.8+ (uses f-strings)
- Standard library (argparse, sys)
- jsonmore.core, jsonmore.colors, jsonmore.utils modules

Author: Jason Cox
Date: July 2, 2025
Repository: https://github.com/jasonacox/jsonmore
"""

import argparse
import sys

from .colors import Colors
from .core import JSONReader
from .utils import paginate_output
from . import __version__, __description__


def main() -> None:
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(
        description="JSON File Reader with formatting and color coding",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  jsonmore data/squad-train-v2.0.json
  jsonmore data/squad-train-v2.0.json --no-colors
  jsonmore data/squad-train-v2.0.json --compact
  jsonmore data/squad-train-v2.0.json --max-size 100
  jsonmore data/squad-train-v2.0.json --no-pager    # Disable paging
  jsonmore bad.json                     # Auto-repair malformed JSON
  jsonmore bad.json --no-repair         # Disable auto-repair
        """,
    )

    parser.add_argument("file", help="Path to JSON file")
    parser.add_argument("--no-colors", action="store_true", help="Disable color output")
    parser.add_argument(
        "--compact", action="store_true", help="Show compact structure overview only"
    )
    parser.add_argument(
        "--max-size",
        type=float,
        default=50,
        help="Maximum file size in MB (default: 50)",
    )
    parser.add_argument(
        "--indent", type=int, default=2, help="Indentation spaces (default: 2)"
    )
    parser.add_argument(
        "--no-pager", action="store_true", help="Disable paging for long output"
    )
    parser.add_argument(
        "--no-repair",
        action="store_true",
        help="Disable automatic JSON repair attempts",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"jsonmore {__version__} - {__description__}",
    )

    args = parser.parse_args()

    try:
        reader = JSONReader()
        reader.formatter.indent = args.indent

        # Read the JSON file (with repair attempts by default)
        result = reader.read_file(
            args.file, args.max_size, repair_attempts=not args.no_repair
        )

        # Handle and display JSON parsing results with paging
        output = reader.handle_json_result(
            result, use_colors=not args.no_colors, compact=args.compact
        )

        if output:  # Only paginate if there's formatted content
            paginate_output(output, use_pager=not args.no_pager)

    except (FileNotFoundError, ValueError) as e:
        print(f"{Colors.RED}Error: {e}{Colors.RESET}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}Unexpected error: {e}{Colors.RESET}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
