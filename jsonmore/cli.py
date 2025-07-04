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
        prog="jsonmore",
        description="JSON File Reader with formatting and color coding",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  jsonmore examples/test.json
  jsonmore examples/test.json --no-colors
  jsonmore examples/large_test.json --max-size 100
  jsonmore examples/test.json --no-pager            # Disable paging
  jsonmore examples/test.json --verbose             # Show headers and structure info
  jsonmore examples/bad.json                        # Auto-repair malformed JSON
  jsonmore examples/bad.json --no-repair            # Disable auto-repair

  # Read from stdin:
  cat examples/test.json | jsonmore
  echo '{"key": "value"}' | jsonmore
  curl -s api.example.com/data.json | jsonmore --no-pager
        """,
    )

    parser.add_argument(
        "files",
        nargs="*",
        help="Path(s) to JSON file(s) (or read from stdin if not provided)",
    )
    parser.add_argument("--no-colors", action="store_true", help="Disable color output")

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
        "--verbose",
        action="store_true",
        help="Display additional information (headers, structure overview)",
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

        if not args.files:
            # Read from stdin
            try:
                json_text = sys.stdin.read()
                if not json_text.strip():
                    print(
                        f"{Colors.YELLOW}No input provided via stdin{Colors.RESET}",
                        file=sys.stderr,
                    )
                    sys.exit(1)

                # Process stdin content using the same repair logic
                result = reader.read_stdin(
                    json_text, repair_attempts=not args.no_repair, verbose=args.verbose
                )
                output = reader.handle_json_result(
                    result,
                    use_colors=not args.no_colors,
                    verbose=args.verbose,
                )
                if output:
                    paginate_output(output, use_pager=not args.no_pager)
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Operation cancelled by user{Colors.RESET}")
                sys.exit(1)
        else:
            # Multiple files: process each in sequence
            show_filenames = len(args.files) > 1
            for idx, file_path in enumerate(args.files):
                if show_filenames:
                    print(f"{Colors.CYAN}File: {file_path}{Colors.RESET}\n")
                try:
                    result = reader.read_file(
                        file_path,
                        args.max_size,
                        repair_attempts=not args.no_repair,
                        verbose=args.verbose,
                    )
                    output = reader.handle_json_result(
                        result,
                        use_colors=not args.no_colors,
                        verbose=args.verbose,
                    )
                    if output:
                        paginate_output(output, use_pager=not args.no_pager)
                except (FileNotFoundError, ValueError) as e:
                    print(f"{Colors.RED}Error: {e}{Colors.RESET}", file=sys.stderr)
                except KeyboardInterrupt:
                    print(f"\n{Colors.YELLOW}Operation cancelled by user{Colors.RESET}")
                    sys.exit(1)
                except Exception as e:
                    print(
                        f"{Colors.RED}Unexpected error: {e}{Colors.RESET}",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                if show_filenames and idx < len(args.files) - 1:
                    print()

    except Exception as e:
        print(f"{Colors.RED}Unexpected error: {e}{Colors.RESET}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
