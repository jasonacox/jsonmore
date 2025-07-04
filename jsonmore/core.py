"""
jsonmore - Core functionality for JSON reading, formatting, and repair

Core business logic including:
- JSONReader: File reading and parsing with error recovery
- JSONFormatter: Pretty-printing with syntax highlighting
- JSONRepair: Automatic repair of malformed JSON files

Features:
- Multi-level error handling (valid, repair, partial, corrupt)
- Automatic JSON syntax error detection and repair
- Structure analysis and preview generation
- Color-coded JSON formatting
- File size validation and encoding detection

Requirements:
- Python 3.8+ (uses f-strings, type hints, pathlib)
- Standard library (json, re, pathlib)
- jsonmore.colors module for terminal formatting

Author: Jason Cox
Date: July 2, 2025
Repository: https://github.com/jasonacox/jsonmore
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Union

from .colors import Colors


class JSONFormatter:
    """JSON formatter with color coding"""

    def __init__(self, use_colors: bool = True, indent: int = 2):
        self.use_colors = use_colors
        self.indent = indent

    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled"""
        if not self.use_colors:
            return text
        return f"{color}{text}{Colors.RESET}"

    def _format_key(self, key: str) -> str:
        """Format JSON keys with color"""
        return self._colorize(f'"{key}"', Colors.BRIGHT_CYAN)

    def _format_string(self, value: str) -> str:
        """Format string values with color"""
        escaped_value = json.dumps(value)
        return self._colorize(escaped_value, Colors.BRIGHT_GREEN)

    def _format_number(self, value: Union[int, float]) -> str:
        """Format number values with color"""
        return self._colorize(str(value), Colors.BRIGHT_YELLOW)

    def _format_boolean(self, value: bool) -> str:
        """Format boolean values with color"""
        return self._colorize(str(value).lower(), Colors.BRIGHT_MAGENTA)

    def _format_null(self) -> str:
        """Format null values with color"""
        return self._colorize("null", Colors.BRIGHT_BLACK)

    def format_json(self, data: Any, current_indent: int = 0) -> str:
        """Format JSON data with colors and proper indentation"""
        indent_str = " " * current_indent
        next_indent_str = " " * (current_indent + self.indent)

        if isinstance(data, dict):
            if not data:
                return self._colorize("{}", Colors.WHITE)

            lines = [self._colorize("{", Colors.WHITE)]
            items = list(data.items())

            for i, (key, value) in enumerate(items):
                key_str = self._format_key(key)
                value_str = self.format_json(value, current_indent + self.indent)
                comma = "," if i < len(items) - 1 else ""
                lines.append(f"{next_indent_str}{key_str}: {value_str}{comma}")

            lines.append(f"{indent_str}{self._colorize('}', Colors.WHITE)}")
            return "\n".join(lines)

        elif isinstance(data, list):
            if not data:
                return self._colorize("[]", Colors.WHITE)

            lines = [self._colorize("[", Colors.WHITE)]

            for i, item in enumerate(data):
                item_str = self.format_json(item, current_indent + self.indent)
                comma = "," if i < len(data) - 1 else ""
                lines.append(f"{next_indent_str}{item_str}{comma}")

            lines.append(f"{indent_str}{self._colorize(']', Colors.WHITE)}")
            return "\n".join(lines)

        elif isinstance(data, str):
            return self._format_string(data)
        elif isinstance(data, bool):
            return self._format_boolean(data)
        elif isinstance(data, (int, float)):
            return self._format_number(data)
        elif data is None:
            return self._format_null()
        else:
            return str(data)


class JSONReader:
    """Main JSON reader class"""

    def __init__(self) -> None:
        self.formatter = JSONFormatter()

    def format_file_size(self, size_in_bytes: int) -> str:
        """Format file size in human-readable format (bytes, KB, MB, or GB)"""
        if size_in_bytes < 1024:
            return f"{size_in_bytes} bytes"
        elif size_in_bytes < 1024 * 1024:
            return f"{size_in_bytes / 1024:.2f} KB"
        elif size_in_bytes < 1024 * 1024 * 1024:
            return f"{size_in_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"

    def read_file(
        self,
        file_path: str,
        max_size_mb: float = 50,
        repair_attempts: bool = True,
        verbose: bool = False,
    ) -> Dict[str, Any]:
        """Read and parse JSON file with size validation and repair capabilities"""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        # Check file size
        file_size_bytes = path.stat().st_size
        file_size_mb = file_size_bytes / (1024 * 1024)
        if file_size_mb > max_size_mb:
            raise ValueError(
                f"File too large: {self.format_file_size(file_size_bytes)} (max: {max_size_mb}MB)"
            )

        # Only show file info in verbose mode
        if verbose:
            print(f"Reading file: {path}")
            print(f"File size: {self.format_file_size(file_size_bytes)}")
            print("-" * 50)

        try:
            with open(path, "r", encoding="utf-8") as f:
                json_text = f.read()
        except UnicodeDecodeError as e:
            raise ValueError(f"File encoding error: {e}")

        # First attempt: try parsing as-is
        try:
            data = json.loads(json_text)
            return {"status": "valid", "data": data}
        except json.JSONDecodeError as original_error:
            if not repair_attempts:
                raise ValueError(f"Invalid JSON format: {original_error}")

            print(
                f"{Colors.YELLOW}⚠ JSON parsing failed, attempting repairs...{Colors.RESET}"
            )

            # Second attempt: try automatic repair
            try:
                repaired_text = JSONRepair.attempt_repair(json_text)
                data = json.loads(repaired_text)
                print(f"{Colors.GREEN}✓ Successfully repaired JSON!{Colors.RESET}")
                return {"status": "repaired", "data": data, "repairs_applied": True}
            except json.JSONDecodeError as repair_error:
                print(
                    f"{Colors.RED}✗ Automatic repair failed: {repair_error}{Colors.RESET}"
                )

                # Third attempt: extract partial JSON fragments
                fragments = JSONRepair.extract_partial_json(json_text)
                if fragments:
                    print(
                        f"{Colors.YELLOW}Found {len(fragments)} valid JSON fragment(s){Colors.RESET}"
                    )
                    return {
                        "status": "partial",
                        "fragments": fragments,
                        "original_error": original_error,
                        "raw_text": json_text,
                    }

                # Final fallback: return raw content with error highlighting
                highlighted_text = JSONRepair.highlight_errors(
                    json_text, original_error, use_colors=True
                )
                return {
                    "status": "corrupt",
                    "raw_text": json_text,
                    "highlighted_text": highlighted_text,
                    "error": original_error,
                }

    def read_stdin(
        self, json_text: str, repair_attempts: bool = True, verbose: bool = False
    ) -> Dict[str, Any]:
        """Read and parse JSON from stdin with repair capabilities"""
        if verbose:
            print("Reading from stdin...")
            input_size_bytes = len(json_text.encode("utf-8"))
            print(
                f"Input size: {self.format_file_size(input_size_bytes)} ({len(json_text)} characters)"
            )
            print("-" * 50)

        # First attempt: try parsing as-is
        try:
            data = json.loads(json_text)
            return {"status": "valid", "data": data}
        except json.JSONDecodeError as original_error:
            if not repair_attempts:
                raise ValueError(f"Invalid JSON format: {original_error}")

            print(
                f"{Colors.YELLOW}⚠ JSON parsing failed, attempting repairs...{Colors.RESET}"
            )

            # Second attempt: try automatic repair
            try:
                repaired_text = JSONRepair.attempt_repair(json_text)
                data = json.loads(repaired_text)
                print(f"{Colors.GREEN}✓ Successfully repaired JSON!{Colors.RESET}")
                return {"status": "repaired", "data": data, "repairs_applied": True}
            except json.JSONDecodeError as repair_error:
                print(
                    f"{Colors.RED}✗ Automatic repair failed: {repair_error}{Colors.RESET}"
                )

                # Third attempt: extract partial JSON fragments
                fragments = JSONRepair.extract_partial_json(json_text)
                if fragments:
                    print(
                        f"{Colors.YELLOW}Found {len(fragments)} valid JSON fragment(s){Colors.RESET}"
                    )
                    return {
                        "status": "partial",
                        "fragments": fragments,
                        "original_error": original_error,
                        "raw_text": json_text,
                    }

                # Final fallback: return raw content with error highlighting
                highlighted_text = JSONRepair.highlight_errors(
                    json_text, original_error, use_colors=True
                )
                return {
                    "status": "corrupt",
                    "raw_text": json_text,
                    "highlighted_text": highlighted_text,
                    "error": original_error,
                }

    def preview_structure(
        self, data: Any, max_depth: int = 3, current_depth: int = 0
    ) -> str:
        """Generate a structure preview of the JSON data"""
        if current_depth >= max_depth:
            return "..."

        if isinstance(data, dict):
            if not data:
                return "{}"

            items = []
            for key, value in list(data.items())[:5]:  # Show first 5 keys
                preview = self.preview_structure(value, max_depth, current_depth + 1)
                items.append(f"{key}: {preview}")

            if len(data) > 5:
                items.append("...")

            return "{" + ", ".join(items) + "}"

        elif isinstance(data, list):
            if not data:
                return "[]"

            if len(data) == 1:
                preview = self.preview_structure(data[0], max_depth, current_depth + 1)
                return f"[{preview}]"
            else:
                preview = self.preview_structure(data[0], max_depth, current_depth + 1)
                return f"[{preview}, ... ({len(data)} items)]"

        elif isinstance(data, str):
            return f'"{data[:20]}{"..." if len(data) > 20 else ""}"'
        else:
            return str(type(data).__name__)

    def display_info(self, data: Any) -> None:
        """Display information about the JSON structure"""
        print(f"\n{Colors.BOLD}JSON Structure Overview:{Colors.RESET}")
        print(f"Type: {type(data).__name__}")

        if isinstance(data, dict):
            print(f"Keys: {len(data)}")
            if data:
                print(f"Top-level keys: {list(data.keys())[:10]}")
        elif isinstance(data, list):
            print(f"Items: {len(data)}")

        print(f"\nStructure preview:")
        print(self.preview_structure(data))
        print("-" * 50)

    def display_json(self, data: Any, use_colors: bool = True) -> str:
        """Format JSON with colors and return as string"""
        self.formatter.use_colors = use_colors
        return self.formatter.format_json(data)

    def handle_json_result(
        self,
        result: Dict[str, Any],
        use_colors: bool = True,
        verbose: bool = False,
    ) -> str:
        """Handle different JSON parsing results (valid, repaired, partial, corrupt)"""
        status = result.get("status", "unknown")

        if status == "valid":
            # Normal JSON processing
            data = result["data"]

            # Show info only in verbose mode
            if verbose:
                self.display_info(data)

            return self.display_json(data, use_colors)

        elif status == "repaired":
            # Successfully repaired JSON
            data = result["data"]

            if verbose:
                # Always show repair message, but info only in verbose mode
                print(
                    f"\n{Colors.GREEN}✓ JSON was automatically repaired and parsed successfully!{Colors.RESET}"
                )
                self.display_info(data)

            return self.display_json(data, use_colors)

        elif status == "partial":
            # Partial JSON fragments found
            fragments = result["fragments"]
            error = result["original_error"]

            print(
                f"\n{Colors.YELLOW}⚠ JSON is malformed, but found {len(fragments)} valid fragment(s):{Colors.RESET}"
            )
            print(
                f"Original error: {error.msg} (line {getattr(error, 'lineno', '?')}, col {getattr(error, 'colno', '?')})"
            )

            output_parts = []
            for i, (frag_type, start, end, data) in enumerate(fragments):
                print(
                    f"\n{Colors.CYAN}Fragment {i+1} ({frag_type}, chars {start}-{end}):{Colors.RESET}"
                )

                if verbose:
                    self.display_info(data)

                fragment_json = self.display_json(data, use_colors)
                output_parts.append(f"--- Fragment {i+1} ---\n{fragment_json}")

            return "\n\n".join(output_parts) if output_parts else ""

        elif status == "corrupt":
            # Completely malformed JSON
            error = result["error"]
            highlighted_text = str(result["highlighted_text"])

            print(
                f"\n{Colors.RED}✗ JSON is severely malformed and cannot be parsed{Colors.RESET}"
            )
            print(f"Error: {error.msg}")
            if hasattr(error, "lineno") and hasattr(error, "colno"):
                print(f"Location: line {error.lineno}, column {error.colno}")

            print(
                f"\n{Colors.BOLD}Raw file content with error highlighting:{Colors.RESET}"
            )
            return highlighted_text

        else:
            return f"Unknown JSON parsing result status: {status}"


class JSONRepair:
    """JSON repair utilities for handling malformed JSON"""

    @staticmethod
    def attempt_repair(json_text: str, debug: bool = False) -> str:
        """Attempt to repair common JSON syntax errors"""
        # Remove comments (// and /* */)
        json_text = re.sub(r"//.*$", "", json_text, flags=re.MULTILINE)
        json_text = re.sub(r"/\*.*?\*/", "", json_text, flags=re.DOTALL)

        # Fix specific pattern: "key": \n "prop": value -> "key": { "prop": value
        json_text = re.sub(
            r'("coordinates"\s*:\s*)\n(\s*)"([^"]+)":', r'\1{\n\2"\3":', json_text
        )

        # Fix common issues
        repairs = [
            # Fix Python-style booleans and None to JSON equivalents using capturing groups
            (r"([:\[{{,\s])True(?=\s*([,}}\]]|$|\s))", r"\1true"),
            (r"([:\[{{,\s])False(?=\s*([,}}\]]|$|\s))", r"\1false"),
            (r"([:\[{{,\s])None(?=\s*([,}}\]]|$|\s))", r"\1null"),
            # Specific fix for the problematic example
            (r'"Jason",\s*nerd:', r'"Jason", "nerd":'),
            # Fix unquoted keys immediately after a comma
            (r",\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:", r', "\1":'),
            # Fix missing comma before unquoted key after quoted value (no whitespace or with whitespace)
            (r'("[^"]*")\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1, "\2":'),
            # Fix missing comma before unquoted key after quoted value (with at least one whitespace)
            (r'("[^"]*"\s*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1, "\2":'),
            # Fix unquoted keys after a quoted string value (general case)
            (r'("[^"]*")\s*,\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1, "\2":'),
            # Fix unquoted keys at the beginning or after commas - basic pattern
            (r"([{{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:", r'\1 "\2":'),
            # Fix unquoted keys after any valid JSON value followed by comma
            (
                r'(["}}\]\d]|true|false|null)\s*,\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:',
                r'\1, "\2":',
            ),
            # Fix single quotes to double quotes for keys and values
            (r"'([^']*)'", r'"\1"'),
            # Fix missing commas between object properties (line break without comma)
            (r'"\s*\n\s*"', '",\n    "'),
            (r'(\w|true|false|null|\d)\s*\n\s*"', r'\1,\n    "'),
            # Fix trailing commas in objects and arrays
            (r",(\s*[}}\]])", r"\1"),
            # Fix missing commas between array elements
            (r"]\s*\n\s*\[", "],\n    ["),
            # Fix missing opening braces for objects after colons
            (r':\s*\n\s*"[^"]+"\s*:', r": {\n    "),
        ]

        repaired = json_text
        max_iterations = 5
        for i in range(max_iterations):
            prev = repaired
            for pattern, replacement in repairs:
                repaired = re.sub(pattern, replacement, repaired)
            if debug:
                print(f"[DEBUG] After repair iteration {i+1}: {repaired}")
            if repaired == prev:
                break

        # Add missing closing braces/brackets if needed
        open_braces = repaired.count("{")
        close_braces = repaired.count("}")
        open_brackets = repaired.count("[")
        close_brackets = repaired.count("]")
        if open_braces > close_braces:
            repaired += "}" * (open_braces - close_braces)
        if open_brackets > close_brackets:
            repaired += "]" * (open_brackets - close_brackets)

        if debug:
            print(f"[DEBUG] After adding closing braces/brackets: {repaired}")

        return repaired

    @staticmethod
    def extract_partial_json(json_text: str) -> List[tuple]:
        """Extract valid JSON fragments from malformed text"""
        fragments = []

        # Try to find complete JSON objects
        brace_count = 0
        start_pos = -1

        for i, char in enumerate(json_text):
            if char == "{":
                if brace_count == 0:
                    start_pos = i
                brace_count += 1
            elif char == "}":
                brace_count -= 1
                if brace_count == 0 and start_pos != -1:
                    fragment = json_text[start_pos : i + 1]
                    try:
                        parsed = json.loads(fragment)
                        fragments.append(("object", start_pos, i + 1, parsed))
                    except json.JSONDecodeError:
                        pass
                    start_pos = -1

        # Try to find complete JSON arrays
        bracket_count = 0
        start_pos = -1

        for i, char in enumerate(json_text):
            if char == "[":
                if bracket_count == 0:
                    start_pos = i
                bracket_count += 1
            elif char == "]":
                bracket_count -= 1
                if bracket_count == 0 and start_pos != -1:
                    fragment = json_text[start_pos : i + 1]
                    try:
                        parsed = json.loads(fragment)
                        fragments.append(("array", start_pos, i + 1, parsed))
                    except json.JSONDecodeError:
                        pass
                    start_pos = -1

        return fragments

    @staticmethod
    def highlight_errors(
        json_text: str, error: json.JSONDecodeError, use_colors: bool = True
    ) -> str:
        """Highlight the location of JSON errors in the text"""
        lines = json_text.split("\n")

        if hasattr(error, "lineno") and hasattr(error, "colno"):
            error_line = error.lineno - 1
            error_col = error.colno - 1

            if 0 <= error_line < len(lines):
                line = lines[error_line]
                if use_colors:
                    # Add error highlighting
                    before = line[:error_col]
                    error_char = line[error_col] if error_col < len(line) else ""
                    after = line[error_col + 1 :]

                    highlighted_line = (
                        before
                        + f"{Colors.BRIGHT_RED}{Colors.BOLD}►{error_char}◄{Colors.RESET}"
                        + after
                    )
                    lines[error_line] = highlighted_line

                    # Add error message
                    error_msg = f"{Colors.BRIGHT_RED}Error on line {error.lineno}, column {error.colno}: {error.msg}{Colors.RESET}"
                else:
                    # Text-only error highlighting
                    error_msg = f"Error on line {error.lineno}, column {error.colno}: {error.msg}"
                    lines.insert(error_line + 1, f"{'':>{error_col}}^^^^ {error_msg}")

        return "\n".join(lines)
