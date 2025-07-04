#!/bin/bash

# Run lint test
flake8 ./jsonmore

# Run format fix
black ./jsonmore

# Run all tests
pytest -v --tb=short --disable-warnings --maxfail=1

