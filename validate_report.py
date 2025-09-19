#!/usr/bin/env python3

import json
import sys
import urllib.request
from jsonschema import validate, ValidationError

def validate_report(report_file, schema_url):
    """Validate a report file against the MultiFlexi schema."""
    
    # Load the schema
    try:
        with urllib.request.urlopen(schema_url) as response:
            schema = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error loading schema from {schema_url}: {e}")
        return False
    
    # Load the report
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            report = json.load(f)
    except Exception as e:
        print(f"Error loading report from {report_file}: {e}")
        return False
    
    # Validate
    try:
        validate(instance=report, schema=schema)
        print(f"✅ Report {report_file} is valid according to MultiFlexi schema")
        return True
    except ValidationError as e:
        print(f"❌ Report {report_file} is NOT valid:")
        print(f"   {e.message}")
        if e.path:
            print(f"   Path: {' -> '.join(str(p) for p in e.path)}")
        return False
    except Exception as e:
        print(f"Error during validation: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 validate_report.py <report.json>")
        sys.exit(1)
    
    report_file = sys.argv[1]
    schema_url = "https://raw.githubusercontent.com/VitexSoftware/php-vitexsoftware-multiflexi-core/refs/heads/main/multiflexi.report.schema.json"
    
    if validate_report(report_file, schema_url):
        sys.exit(0)
    else:
        sys.exit(1)