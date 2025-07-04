# jsonMore

A powerful command-line tool for reading, formatting, and analyzing JSON files with beautiful syntax highlighting, automatic error repair, and smart paging.

[![PyPI version](https://badge.fury.io/py/jsonmore.svg)](https://badge.fury.io/py/jsonmore)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Quick Start 🚀

After installation, use the `jsonmore` command directly:

```bash
# Install
pip install jsonmore

# Pipe Test
echo '{"id": 123, "name": "Jason", "nerd": true}' | jsonmore

# File Test
jsonmore somefile.json
```

<img width="452" alt="image" src="https://github.com/user-attachments/assets/1a071f4c-f068-4190-89e0-9eb9ddfe9e37" />

## Installation

### For Users (Recommended)

Install globally using your preferred Python package manager:

```bash
# Using pip
pip install jsonmore

# Using pipx (recommended for CLI tools)
pipx install jsonmore

# Using uv
uv pip install jsonmore
```

### For Developers

Clone the repository and install in development mode:

```bash
git clone https://github.com/yourusername/jsonmore.git
cd jsonmore
pip install -e ".[dev]"
```

## Usage

### Command Line Interface

```bash
# Basic file reading
jsonmore file.json

# Large files with custom size limit
jsonmore large_file.json --max-size 100

# Disable paging for direct output
jsonmore file.json --no-pager

# Handle malformed JSON
jsonmore broken.json              # Auto-repair (default)
jsonmore broken.json --no-repair  # Disable auto-repair

# Custom formatting
jsonmore file.json --indent 4 --no-colors
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--no-colors` | Disable color output for plain text |
| `--max-size N` | Maximum file size in MB (default: 50) |
| `--indent N` | Indentation spaces (default: 2) |
| `--no-pager` | Disable automatic paging |
| `--no-repair` | Disable automatic JSON repair |
| `--verbose` | Show headers and JSON structure info |
| `--help` | Show help message and examples |

### Python API

You can also use jsonmore as a Python library:

```python
from jsonmore import JSONReader, JSONFormatter

# Read and parse JSON file
reader = JSONReader()
result = reader.read_file('data.json')

if result['status'] == 'valid':
    data = result['data']
    print(f"Successfully parsed JSON with {len(data)} keys")

# Format JSON with colors
formatter = JSONFormatter(use_colors=True, indent=2)
formatted = formatter.format_json(data)
print(formatted)
```

## 🔧 JSON Repair Capabilities

The tool can automatically detect and fix common JSON syntax errors:

### **Supported Repairs**
- **Missing quotes** around object keys
- **Single quotes** instead of double quotes
- **Trailing commas** in objects and arrays
- **Missing commas** between properties
- **JavaScript-style comments** (`//` and `/* */`)
- **Missing braces** in nested objects
- **Malformed structure** patterns

### **Example Repairs**

**Before (broken JSON):**
```json
{
  name: "John",           // Missing quotes on key
  'age': 25,              // Single quotes
  "skills": ["Python",],  // Trailing comma
  "active": true,         // Trailing comma
}
```

**After (auto-repaired):**
```json
{
  "name": "John",
  "age": 25,
  "skills": ["Python"],
  "active": true
}
```

## Package Structure

For developers and contributors, here's the package organization:

```
jsonmore/
├── __init__.py          # Package initialization and public API
├── cli.py              # Command-line interface entry point
├── colors.py           # ANSI color definitions
├── core.py             # Core JSON processing (JSONReader, JSONFormatter, JSONRepair)
├── utils.py            # Utility functions (paging, terminal handling)
└── py.typed            # Type hints marker file
```

### Module Overview

- **`jsonmore.cli`**: Command-line interface and argument parsing
- **`jsonmore.core`**: Main business logic for JSON reading, formatting, and repair
- **`jsonmore.colors`**: ANSI color code definitions for terminal output
- **`jsonmore.utils`**: Utility functions for paging and terminal interaction
- **`jsonmore`**: Public API exports for library usage

## Development API

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/jsonmore.git
cd jsonmore

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install development tools
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Basic tests
python test_jsonmore.py

# With pytest (if installed)
pytest test_jsonmore.py -v
```

### Code Quality

```bash
# Format code
black jsonmore/

# Lint code
flake8 jsonmore/

# Type checking
mypy jsonmore/
```

## Error Handling

The tool provides multiple levels of error handling:

1. **Valid JSON**: Normal parsing and display
2. **Auto-Repair**: Attempts to fix common errors
3. **Partial Parsing**: Extracts valid JSON fragments
4. **Raw Display**: Shows content with error highlighting

### Color-Coded Output
- **Keys**: Cyan
- **Strings**: Green  
- **Numbers**: Yellow
- **Booleans**: Magenta
- **Null**: Gray
- **Brackets/Braces**: White

### Error Highlighting
```json
{
  "name": "John",
  ►a◄ge: 30,  // Error highlighted here
  "city": "NYC"
}
```

## Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes** and add tests
4. **Run the test suite**: `python test_jsonmore.py`
5. **Submit a pull request**

### Guidelines

- Maintain compatibility with Python 3.8+
- Follow the existing code style (use `black` for formatting)
- Add tests for new features
- Update documentation as needed

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python's standard library for maximum compatibility
- Inspired by tools like `jq`, `bat`, and `less`
- Thanks to the JSON specification and repair techniques community

---

**Happy JSON reading!**
