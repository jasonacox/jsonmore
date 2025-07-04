# jsonMore Release Notes

## Version 1.0.2 - July 3, 2025

### Enhancements
- **Robust cross-platform paging:**
  - Custom pager now supports up/down/space/enter navigation, color output, and interactive navigation for both file and piped input.
  - Fallback pager for piped input supports single-key navigation (space, enter, q) using /dev/tty, with proper terminal formatting.
- **Improved CLI usability:**
  - Paging now works for piped input as well as files.
  - Pager is only disabled if output is not a TTY, ensuring correct behavior for both interactive and piped use cases.
- **Better error handling:**
  - Graceful fallback and clear error messages if /dev/tty is unavailable or navigation input is not possible.

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
