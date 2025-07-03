# jsonMore

A powerful command-line tool for reading, formatting, and analyzing JSON files with beautiful syntax highlighting, automatic error repair, and smart paging.

[![PyPI version](https://badge.fury.io/py/jsonmore.svg)](https://badge.fury.io/py/jsonmore)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

### 🎨 **Beautiful Output**
- **Color-coded syntax highlighting** for JSON elements
- **Pretty-printed formatting** with customizable indentation
- **Structure overview** showing file statistics and preview
- **Smart paging** for long outputs (like `less` command)

### 🔧 **Automatic JSON Repair**
- **Auto-detection and repair** of common JSON syntax errors
- **Partial JSON extraction** from malformed files
- **Error highlighting** with precise location indicators
- **Graceful fallback** handling for severely corrupted files

### 📊 **Multiple Display Modes**
- **Full display**: Complete formatted JSON with colors
- **Compact mode**: Structure overview only
- **Fragment mode**: Display valid JSON pieces from corrupt files
- **Raw mode**: Original content with error highlighting

### 🛡️ **Robust File Handling**
- **File size protection** with configurable limits
- **Encoding detection** and error handling
- **Large file support** with automatic paging
- **Memory-efficient** processing

## 📦 Installation

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

## 🚀 Quick Start

After installation, use the `jsonmore` command directly:

```bash
# Basic usage
jsonmore data/example.json

# Show structure overview only
jsonmore data/example.json --compact

# Disable colors for plain text output
jsonmore data/example.json --no-colors
```

## 📚 Usage

### Command Line Interface

```bash
# Basic file reading
jsonmore file.json

# Large files with custom size limit
jsonmore large_file.json --max-size 100

# Disable paging for direct output
jsonmore file.json --no-pager

# Compact structure overview
jsonmore file.json --compact

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
| `--compact` | Show only structure overview |
| `--max-size N` | Maximum file size in MB (default: 50) |
| `--indent N` | Indentation spaces (default: 2) |
| `--no-pager` | Disable automatic paging |
| `--no-repair` | Disable automatic JSON repair |
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

### ✅ **Supported Repairs**
- **Missing quotes** around object keys
- **Single quotes** instead of double quotes
- **Trailing commas** in objects and arrays
- **Missing commas** between properties
- **JavaScript-style comments** (`//` and `/* */`)
- **Missing braces** in nested objects
- **Malformed structure** patterns

### 📋 **Example Repairs**

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

## 🏗️ Package Structure

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

## 🔬 Development

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

### Building and Publishing

```bash
# Build package
python -m build

# Test on TestPyPI
python -m twine upload --repository testpypi dist/*

# Publish to PyPI
python -m twine upload dist/*
```

## 📊 Error Handling

The tool provides multiple levels of error handling:

1. **🟢 Valid JSON**: Normal parsing and display
2. **🔧 Auto-Repair**: Attempts to fix common errors
3. **📄 Partial Parsing**: Extracts valid JSON fragments
4. **🚨 Raw Display**: Shows content with error highlighting

### Example: Partial JSON Recovery

For files containing mixed content, jsonmore will extract and display valid JSON fragments:

```
This is some text...

{"user": {"name": "Alice", "age": 25}}

More text here...

["apple", "banana", "cherry"]

End of file.
```

## 🎨 Output Examples

### Structure Overview
```
JSON Structure Overview:
Type: dict
Keys: 8
Top-level keys: ['name', 'age', 'isEmployed', 'skills', 'address', 'projects']

Structure preview:
{name: "John Doe", age: int, isEmployed: bool, skills: ["Python", ... (3 items)], 
 address: {street: "123 Main St", city: "New York", ...}, ...}
```

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

## ⚙️ Configuration

### Paging Behavior

For long outputs, jsonmore automatically uses system pagers:

1. **`less`** (preferred): Full navigation with color support
2. **`more`**: Basic paging functionality  
3. **Direct output**: Fallback when no pager available

Pager selection respects the `$PAGER` environment variable.

### File Size Limits

Default maximum file size: **50MB**

```bash
# Increase limit to 100MB
jsonmore huge_file.json --max-size 100
```

## 📝 Examples

### Different Use Cases

```bash
# Configuration files
jsonmore config/settings.json --compact

# API responses
jsonmore api_response.json

# Large datasets
jsonmore data/large_dataset.json --max-size 200

# Debugging malformed JSON
jsonmore broken_config.json
```

### Integration with Other Tools

```bash
# Pipe output
jsonmore data.json --no-colors --no-pager | grep "name"

# Quick structure check
jsonmore data.json --compact

# Validation in scripts
jsonmore input.json --no-repair || echo "File is invalid"
```

## 🔍 Technical Details

### Performance
- **Fast parsing**: Uses Python's built-in `json` module
- **Memory efficient**: Streams large files when possible
- **Smart paging**: Only activates for outputs longer than terminal height

### Dependencies
- **Python 3.6+** (uses f-strings and type hints)
- **Standard library only** (no external dependencies)
- **Optional**: `less`/`more` for enhanced paging

### Exit Codes
- **0**: Success
- **1**: File not found, parsing error, or size limit exceeded
- **130**: User interrupted (Ctrl+C)

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes** and add tests
4. **Run the test suite**: `python test_jsonmore.py`
5. **Submit a pull request**

### Guidelines

- Maintain compatibility with Python 3.6+
- Follow the existing code style (use `black` for formatting)
- Add tests for new features
- Update documentation as needed

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python's standard library for maximum compatibility
- Inspired by tools like `jq`, `bat`, and `less`
- Thanks to the JSON specification and repair techniques community

---

**Happy JSON reading! 🎉**
