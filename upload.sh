#!/bin/bash
#
# Upload script for jsonmore package to PyPI
# Author: Jason Cox (jason@jasonacox.com)
#
# This script:
# 1. Cleans previous builds
# 2. Builds the package
# 3. Uploads to TestPyPI first for testing
# 4. Optionally uploads to PyPI
#

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] || [ ! -d "jsonmore" ]; then
    print_error "This script must be run from the jsonmore project root directory"
    exit 1
fi

# Check for required tools
print_status "Checking for required tools..."
command -v python3 >/dev/null 2>&1 || { print_error "python3 is required but not installed"; exit 1; }

# Check if build and twine are installed
python3 -c "import build" 2>/dev/null || {
    print_warning "build module not found, installing..."
    pip install build
}

python3 -c "import twine" 2>/dev/null || {
    print_warning "twine module not found, installing..."
    pip install twine
}

# Get version from package
VERSION=$(python3 -c "from jsonmore import __version__; print(__version__)")
print_status "Building jsonmore version: $VERSION"

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/
print_success "Clean completed"

# Run basic tests
print_status "Running basic tests..."
if python3 test_jsonmore.py; then
    print_success "Tests passed"
else
    print_error "Tests failed"
    exit 1
fi

# Build the package
print_status "Building package..."
if python3 -m build; then
    print_success "Package built successfully"
else
    print_error "Package build failed"
    exit 1
fi

# List built files
print_status "Built files:"
ls -la dist/

# Upload to TestPyPI first
print_status "Uploading to TestPyPI for testing..."
echo -e "${YELLOW}Note: You'll need your TestPyPI API token${NC}"
echo -e "${YELLOW}Get it from: https://test.pypi.org/manage/account/token/${NC}"

if python3 -m twine upload --repository testpypi dist/*; then
    print_success "Successfully uploaded to TestPyPI"
    echo -e "${BLUE}Test installation with:${NC}"
    echo "pip install --index-url https://test.pypi.org/simple/ jsonmore==$VERSION"
    echo ""
else
    print_error "Failed to upload to TestPyPI"
    exit 1
fi

# Ask user if they want to upload to PyPI
echo -e "${YELLOW}Do you want to upload to PyPI? (y/N):${NC} "
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    print_status "Uploading to PyPI..."
    echo -e "${YELLOW}Note: You'll need your PyPI API token${NC}"
    echo -e "${YELLOW}Get it from: https://pypi.org/manage/account/token/${NC}"
    
    if python3 -m twine upload dist/*; then
        print_success "Successfully uploaded to PyPI!"
        echo -e "${GREEN}Package is now available at: https://pypi.org/project/jsonmore/${NC}"
        echo -e "${GREEN}Install with: pip install jsonmore${NC}"
    else
        print_error "Failed to upload to PyPI"
        exit 1
    fi
else
    print_status "Skipping PyPI upload"
fi

print_success "Upload process completed!"

# Optional: Show installation commands
echo ""
print_status "Installation commands:"
echo "pip install jsonmore==$VERSION"
echo "pipx install jsonmore==$VERSION"
echo "uv pip install jsonmore==$VERSION"
