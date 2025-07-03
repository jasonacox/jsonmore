#!/bin/bash
#
# Version bump script for jsonmore package
# Usage: ./bump_version.sh [major|minor|patch] [new_version]
#
# Examples:
#   ./bump_version.sh patch        # 1.0.0 -> 1.0.1
#   ./bump_version.sh minor        # 1.0.1 -> 1.1.0  
#   ./bump_version.sh major        # 1.1.0 -> 2.0.0
#   ./bump_version.sh 1.2.3        # Set to specific version
#

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "jsonmore/__init__.py" ]; then
    print_error "This script must be run from the jsonmore project root directory"
    exit 1
fi

# Get current version
CURRENT_VERSION=$(python3 -c "from jsonmore import __version__; print(__version__)")
print_status "Current version: $CURRENT_VERSION"

# Parse current version
IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

# Determine new version
if [ $# -eq 0 ]; then
    echo "Usage: $0 [major|minor|patch|VERSION]"
    echo "Current version: $CURRENT_VERSION"
    exit 1
fi

case $1 in
    major)
        NEW_VERSION="$((MAJOR + 1)).0.0"
        ;;
    minor)
        NEW_VERSION="$MAJOR.$((MINOR + 1)).0"
        ;;
    patch)
        NEW_VERSION="$MAJOR.$MINOR.$((PATCH + 1))"
        ;;
    *)
        # Assume it's a specific version
        if [[ $1 =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            NEW_VERSION=$1
        else
            print_error "Invalid version format. Use major|minor|patch or X.Y.Z format"
            exit 1
        fi
        ;;
esac

print_status "New version will be: $NEW_VERSION"

# Confirm with user
echo -n "Continue? (y/N): "
read -r response
if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    print_status "Version bump cancelled"
    exit 0
fi

# Update version in __init__.py
print_status "Updating jsonmore/__init__.py..."
sed -i.bak "s/__version__ = \"$CURRENT_VERSION\"/__version__ = \"$NEW_VERSION\"/" jsonmore/__init__.py

# Update version in pyproject.toml
print_status "Updating pyproject.toml..."
sed -i.bak "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml

# Clean up backup files
rm -f jsonmore/__init__.py.bak pyproject.toml.bak

# Verify the changes
NEW_VERSION_CHECK=$(python3 -c "from jsonmore import __version__; print(__version__)")
if [ "$NEW_VERSION_CHECK" = "$NEW_VERSION" ]; then
    print_success "Version successfully updated to $NEW_VERSION"
    
    # Show git status
    print_status "Git status:"
    git status --porcelain
    
    echo ""
    print_status "Next steps:"
    echo "1. Review changes: git diff"
    echo "2. Commit changes: git add . && git commit -m 'Bump version to $NEW_VERSION'"
    echo "3. Create tag: git tag v$NEW_VERSION"
    echo "4. Push changes: git push && git push --tags"
    echo "5. Upload to PyPI: ./upload.sh"
else
    print_error "Version update failed. Expected $NEW_VERSION, got $NEW_VERSION_CHECK"
    exit 1
fi
