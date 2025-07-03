#!/usr/bin/env python3

import os
from jsonmore.core import JSONReader

def main():
    reader = JSONReader()
    
    # Test file size formatting
    test_file = "examples/test.json"
    file_size_bytes = os.path.getsize(test_file)
    print(f"File: {test_file}")
    print(f"Size in bytes: {file_size_bytes}")
    print(f"Formatted size: {reader.format_file_size(file_size_bytes)}")
    
    # Test different sizes
    test_sizes = [
        10,  # bytes
        1500,  # ~1.5KB
        1500000,  # ~1.5MB
        1500000000  # ~1.5GB
    ]
    
    for size in test_sizes:
        print(f"\nTest size: {size} bytes")
        print(f"Formatted: {reader.format_file_size(size)}")

if __name__ == "__main__":
    main()
