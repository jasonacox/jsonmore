#!/usr/bin/env python3

from jsonmore.core import JSONRepair
import json

# The problematic JSON string
json_text = '{"id": 123, "name": "Jason", nerd: true}'
print(f"Original JSON: {json_text}")

# Try to repair using our class
try:
    repaired_text = JSONRepair.attempt_repair(json_text)
    print(f"Repaired JSON: {repaired_text}")
    
    # Try to parse
    data = json.loads(repaired_text)
    print(f"Successfully parsed: {data}")
except Exception as e:
    print(f"Error: {e}")
