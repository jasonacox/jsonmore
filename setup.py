"""
jsonmore - Setup script for package installation

Setup script for building and installing the jsonmore package.
Provides backward compatibility with older Python packaging tools.

Features:
- Package discovery and metadata configuration
- Console script entry point registration
- Development dependencies specification
- Cross-platform compatibility

Requirements:
- Python 3.8+
- setuptools for package building
- Standard library modules

Author: Jason Cox
Date: July 2, 2025
Repository: https://github.com/jasonacox/jsonmore
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

# Read version from package
def get_version():
    version_file = os.path.join('jsonmore', '__init__.py')
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('=')[1].strip().strip('"\'')
    return "1.0.0"

setup(
    name="jsonmore",
    version=get_version(),
    description="A powerful command-line tool for reading, formatting, and analyzing JSON files with beautiful syntax highlighting, automatic error repair, and smart paging",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Jason Cox",
    author_email="jason@jasonacox.com",
    url="https://github.com/jasonacox/jsonmore",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    keywords=["json", "cli", "formatting", "syntax-highlighting", "repair", "validator"],
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        'console_scripts': [
            'jsonmore=jsonmore.cli:main',
        ],
    },
    extras_require={
        'dev': [
            'pytest>=6.0',
            'black',
            'flake8',
            'mypy',
        ],
    },
    project_urls={
        'Homepage': 'https://github.com/jasonacox/jsonmore',
        'Documentation': 'https://github.com/jasonacox/jsonmore#readme',
        'Repository': 'https://github.com/jasonacox/jsonmore.git',
        'Bug Tracker': 'https://github.com/jasonacox/jsonmore/issues',
    },
)
