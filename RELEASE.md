# jsonMore Release Notes

## Version 1.0.1 - July 2, 2025

### Enhancements
- **Improved file size display**: Now automatically selects appropriate units (bytes, KB, MB, GB) based on file size, making small file sizes more readable
- **Removed deprecated `--compact` option**: This option was no longer working and has been removed from the codebase and documentation

### Internal Changes
- Updated core file size handling in `JSONReader` class
- Enhanced stdin input size reporting with both byte size and character count
- Code cleanup and improved error handling

## Version 1.0.0 - June 28, 2025

### Initial Release
- Command-line interface for JSON file reading with syntax highlighting
- Automatic error detection and repair for malformed JSON files
- Comprehensive error handling (valid, repair, partial, corrupt)
- Smart paging for long outputs with terminal height detection
- Cross-platform color support using colorama
- Support for Python 3.8+ with modern packaging

### Features
- Beautiful syntax highlighting for JSON structures
- File size validation and automatic paging
- Structure analysis and preview generation
- Multi-level error handling and recovery
- Python API for programmatic use
