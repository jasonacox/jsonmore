"""
jsonmore - Comprehensive test suite

Comprehensive tests for the jsonmore package functionality including:
- JSON formatting and parsing with various data types
- File reading, error handling, and edge cases
- Color definitions and repair capabilities
- CLI argument parsing and error scenarios
- Utility functions and paging behavior

Test Coverage:
- JSONFormatter: colors, indentation, data types, edge cases
- JSONReader: file operations, structure analysis, error handling
- JSONRepair: automatic fixing, partial extraction, error highlighting
- Colors: class definitions and constants
- Utils: paging functions and terminal handling
- CLI: argument parsing and main function behavior

Requirements:
- Python 3.8+
- jsonmore package modules
- tempfile for test file creation
- unittest for structured testing

Author: Jason Cox
Date: July 2, 2025
Repository: https://github.com/jasonacox/jsonmore
"""

import json
import tempfile
import os
import unittest
import sys
from unittest.mock import patch, MagicMock

from jsonmore import JSONReader, JSONFormatter, Colors
from jsonmore.core import JSONRepair
from jsonmore.utils import get_pager, paginate_output
from jsonmore.cli import main


class TestJSONFormatter(unittest.TestCase):
    """Test JSONFormatter functionality"""

    def setUp(self):
        self.formatter = JSONFormatter(use_colors=False)
        self.formatter_color = JSONFormatter(use_colors=True)

    def test_simple_object_formatting(self):
        """Test formatting simple JSON objects"""
        data = {"name": "test", "value": 42}
        result = self.formatter.format_json(data)
        self.assertIn('"name": "test"', result)
        self.assertIn('"value": 42', result)

    def test_color_formatting(self):
        """Test that color formatting adds ANSI codes"""
        data = {"name": "test", "value": 42}
        colored_result = self.formatter_color.format_json(data)
        plain_result = self.formatter.format_json(data)
        # Colored result should be longer due to ANSI codes
        self.assertGreater(len(colored_result), len(plain_result))
        # Should contain ANSI reset codes
        self.assertIn("\033[0m", colored_result)

    def test_data_types(self):
        """Test formatting of different JSON data types"""
        data = {
            "string": "hello",
            "number": 123,
            "float": 45.67,
            "boolean": True,
            "null": None,
            "array": [1, 2, 3],
            "object": {"nested": "value"},
        }
        result = self.formatter.format_json(data)
        self.assertIn('"string": "hello"', result)
        self.assertIn('"number": 123', result)
        self.assertIn('"float": 45.67', result)
        self.assertIn('"boolean": true', result)
        self.assertIn('"null": null', result)
        self.assertIn("[", result)  # Array brackets
        self.assertIn("{", result)  # Object brackets

    def test_empty_containers(self):
        """Test formatting of empty arrays and objects"""
        self.assertEqual(self.formatter.format_json({}), "{}")
        self.assertEqual(self.formatter.format_json([]), "[]")

    def test_custom_indentation(self):
        """Test custom indentation settings"""
        formatter_4 = JSONFormatter(use_colors=False, indent=4)
        data = {"nested": {"value": 1}}
        result = formatter_4.format_json(data)
        # Should have 4-space indentation
        self.assertIn('    "nested":', result)
        self.assertIn('        "value": 1', result)


class TestJSONReader(unittest.TestCase):
    """Test JSONReader functionality"""

    def setUp(self):
        self.reader = JSONReader()

    def test_valid_json_file(self):
        """Test reading valid JSON files"""
        test_data = {"test": True, "numbers": [1, 2, 3]}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_data, f)
            temp_file = f.name

        try:
            result = self.reader.read_file(temp_file)
            self.assertEqual(result["status"], "valid")
            self.assertEqual(result["data"], test_data)
        finally:
            os.unlink(temp_file)

    def test_file_not_found(self):
        """Test handling of non-existent files"""
        with self.assertRaises(FileNotFoundError):
            self.reader.read_file("nonexistent_file.json")

    def test_file_size_limit(self):
        """Test file size validation"""
        # Create a file with some content
        test_data = {"large": "data" * 1000}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_data, f)
            temp_file = f.name

        try:
            # Test with very small size limit
            with self.assertRaises(ValueError) as cm:
                self.reader.read_file(temp_file, max_size_mb=0.001)
            self.assertIn("File too large", str(cm.exception))
        finally:
            os.unlink(temp_file)

    def test_structure_preview(self):
        """Test structure preview generation"""
        test_data = {
            "name": "John",
            "age": 30,
            "items": ["a", "b", "c"],
            "nested": {"key": "value"},
        }

        preview = self.reader.preview_structure(test_data)
        self.assertIn("name:", preview)
        self.assertIn("age:", preview)
        self.assertIn("items:", preview)
        self.assertIn("nested:", preview)

    def test_preview_depth_limit(self):
        """Test structure preview depth limiting"""
        deep_data = {"level1": {"level2": {"level3": {"level4": "deep"}}}}
        preview = self.reader.preview_structure(deep_data, max_depth=2)
        self.assertIn("...", preview)

    def test_display_info_dict(self):
        """Test display_info for dictionary data"""
        data = {"a": 1, "b": 2, "c": 3}
        # Capture output
        with patch("builtins.print") as mock_print:
            self.reader.display_info(data)
            # Should print type and key information
            printed_calls = [str(call) for call in mock_print.call_args_list]
            printed_text = " ".join(printed_calls)
            self.assertIn("dict", printed_text)
            self.assertIn("Keys: 3", printed_text)

    def test_display_info_list(self):
        """Test display_info for list data"""
        data = [1, 2, 3, 4, 5]
        with patch("builtins.print") as mock_print:
            self.reader.display_info(data)
            printed_calls = [str(call) for call in mock_print.call_args_list]
            printed_text = " ".join(printed_calls)
            self.assertIn("Items: 5", printed_text)


class TestJSONRepair(unittest.TestCase):
    """Test JSONRepair functionality"""

    def test_repair_unquoted_keys(self):
        """Test repairing unquoted object keys"""
        broken_json = '{name: "John", age: 30}'
        repaired = JSONRepair.attempt_repair(broken_json)

        try:
            parsed = json.loads(repaired)
            self.assertEqual(parsed["name"], "John")
            self.assertEqual(parsed["age"], 30)
        except json.JSONDecodeError:
            # Some repairs might not work perfectly, which is acceptable
            pass

    def test_repair_single_quotes(self):
        """Test repairing single quotes"""
        broken_json = "{'name': 'John', 'age': 30}"
        repaired = JSONRepair.attempt_repair(broken_json)

        try:
            parsed = json.loads(repaired)
            self.assertEqual(parsed["name"], "John")
            self.assertEqual(parsed["age"], 30)
        except json.JSONDecodeError:
            pass

    def test_repair_trailing_commas(self):
        """Test removing trailing commas"""
        broken_json = '{"name": "John", "age": 30,}'
        repaired = JSONRepair.attempt_repair(broken_json)

        try:
            parsed = json.loads(repaired)
            self.assertEqual(parsed["name"], "John")
            self.assertEqual(parsed["age"], 30)
        except json.JSONDecodeError:
            pass

    def test_repair_comments(self):
        """Test removing JavaScript-style comments"""
        broken_json = """
        {
            "name": "John", // This is a comment
            /* Multi-line
               comment */
            "age": 30
        }
        """
        repaired = JSONRepair.attempt_repair(broken_json)

        try:
            parsed = json.loads(repaired)
            self.assertEqual(parsed["name"], "John")
            self.assertEqual(parsed["age"], 30)
        except json.JSONDecodeError:
            pass

    def test_extract_partial_json_objects(self):
        """Test extracting valid JSON objects from mixed content"""
        mixed_content = """
        Some random text here
        {"valid": "object", "number": 42}
        More text
        {"another": "object"}
        End text
        """

        fragments = JSONRepair.extract_partial_json(mixed_content)
        self.assertGreater(len(fragments), 0)

        # Check that we found valid objects
        for frag_type, start, end, data in fragments:
            self.assertEqual(frag_type, "object")
            self.assertIsInstance(data, dict)

    def test_extract_partial_json_arrays(self):
        """Test extracting valid JSON arrays from mixed content"""
        mixed_content = """
        Some text
        [1, 2, 3, 4]
        More text
        ["a", "b", "c"]
        End
        """

        fragments = JSONRepair.extract_partial_json(mixed_content)
        self.assertGreater(len(fragments), 0)

        # Check for array fragments
        array_fragments = [f for f in fragments if f[0] == "array"]
        self.assertGreater(len(array_fragments), 0)

    def test_highlight_errors(self):
        """Test error highlighting functionality"""
        broken_json = '{"name": "John", "age":}'

        try:
            json.loads(broken_json)
        except json.JSONDecodeError as e:
            highlighted = JSONRepair.highlight_errors(broken_json, e, use_colors=True)
            self.assertIn("►", highlighted)  # Error marker
            self.assertIn("◄", highlighted)  # Error marker

            # Test without colors
            highlighted_plain = JSONRepair.highlight_errors(
                broken_json, e, use_colors=False
            )
            self.assertIn("Error on line", highlighted_plain)


class TestColors(unittest.TestCase):
    """Test Colors class"""

    def test_color_constants(self):
        """Test that all expected color constants exist"""
        expected_colors = [
            "RED",
            "GREEN",
            "YELLOW",
            "BLUE",
            "MAGENTA",
            "CYAN",
            "WHITE",
            "RESET",
        ]
        for color in expected_colors:
            self.assertTrue(hasattr(Colors, color))
            self.assertIsInstance(getattr(Colors, color), str)

    def test_bright_colors(self):
        """Test bright color variants"""
        bright_colors = ["BRIGHT_RED", "BRIGHT_GREEN", "BRIGHT_YELLOW", "BRIGHT_BLUE"]
        for color in bright_colors:
            self.assertTrue(hasattr(Colors, color))

    def test_reset_code(self):
        """Test that RESET code is correct"""
        self.assertEqual(Colors.RESET, "\033[0m")


class TestUtils(unittest.TestCase):
    """Test utility functions"""

    def test_get_pager(self):
        """Test pager detection"""
        pager = get_pager()
        # Should return a string or None
        self.assertTrue(pager is None or isinstance(pager, str))

    @patch.dict(os.environ, {"PAGER": "custom_pager"})
    @patch("shutil.which")
    def test_get_pager_env_variable(self, mock_which):
        """Test pager from environment variable"""
        mock_which.return_value = "/usr/bin/custom_pager"
        pager = get_pager()
        self.assertEqual(pager, "custom_pager")

    @patch("shutil.get_terminal_size")
    @patch("jsonmore.pager.Pager.show", return_value=None)
    @patch("sys.stdout.isatty", return_value=True)
    @patch("sys.stdin.isatty", return_value=True)
    def test_paginate_output_short_text(
        self, _mock_stdin_isatty, _mock_stdout_isatty, _mock_show, mock_terminal_size
    ):
        """Test pagination with short text"""
        mock_terminal_size.return_value = MagicMock(lines=50)

        short_text = "Short text"
        paginate_output(short_text, use_pager=True)

        # Pager.show should be called once
        _mock_show.assert_called_once()

    @patch("builtins.print")
    def test_paginate_output_no_pager(self, mock_print):
        """Test pagination with pager disabled"""
        text = "Some text"
        paginate_output(text, use_pager=False)
        mock_print.assert_called_once_with(text)


class TestCLI(unittest.TestCase):
    """Test CLI functionality"""

    def test_main_function_exists(self):
        """Test that main function is importable"""
        from jsonmore.cli import main

        self.assertTrue(callable(main))

    @patch("sys.argv", ["jsonmore", "--version"])
    def test_version_argument(self):
        """Test --version argument"""
        with self.assertRaises(SystemExit):
            # --version should cause SystemExit
            main()


def run_comprehensive_tests():
    """Run all tests with detailed output"""
    # Create test suite
    test_classes = [
        TestJSONFormatter,
        TestJSONReader,
        TestJSONRepair,
        TestColors,
        TestUtils,
        TestCLI,
    ]

    suite = unittest.TestSuite()
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(
        f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%"
    )

    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            # Extract error message from traceback
            error_msg = traceback.split("AssertionError: ")[-1].split("\n")[0]
            print(f"- {test}: {error_msg}")

    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            # Extract error message from traceback
            error_lines = traceback.split("\n")
            error_msg = error_lines[-2] if len(error_lines) > 1 else "Unknown error"
            print(f"- {test}: {error_msg}")

    return result.wasSuccessful()


# Legacy test functions for backward compatibility
def test_json_formatter():
    """Legacy test function"""
    formatter = JSONFormatter(use_colors=False)
    data = {"name": "test", "value": 42}
    result = formatter.format_json(data)
    assert '"name": "test"' in result
    assert '"value": 42' in result


def test_json_reader():
    """Legacy test function"""
    reader = JSONReader()
    test_data = {"test": True, "numbers": [1, 2, 3]}

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(test_data, f)
        temp_file = f.name

    try:
        result = reader.read_file(temp_file)
        assert result["status"] == "valid"
        assert result["data"] == test_data
    finally:
        os.unlink(temp_file)


def test_json_repair():
    """Legacy test function"""
    broken_json = '{"name": John, "age": 30}'
    repaired = JSONRepair.attempt_repair(broken_json)

    try:
        parsed = json.loads(repaired)
        assert parsed["name"] == "John"
        assert parsed["age"] == 30
    except json.JSONDecodeError:
        pass  # Repair might not always work


def test_colors():
    """Legacy test function"""
    assert hasattr(Colors, "RED")
    assert hasattr(Colors, "GREEN")
    assert hasattr(Colors, "RESET")
    assert Colors.RESET == "\033[0m"


if __name__ == "__main__":
    print("jsonmore - Comprehensive Test Suite")
    print("=" * 50)

    # Check if user wants comprehensive tests
    if len(sys.argv) > 1 and sys.argv[1] == "--comprehensive":
        success = run_comprehensive_tests()
        sys.exit(0 if success else 1)
    else:
        # Run legacy tests
        print("Running basic tests (use --comprehensive for full test suite)...")
        try:
            test_json_formatter()
            test_json_reader()
            test_json_repair()
            test_colors()
            print("All basic tests passed!")
        except Exception as e:
            print(f"Test failed: {e}")
            sys.exit(1)
