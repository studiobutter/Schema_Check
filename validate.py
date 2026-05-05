import json
import sys

SCHEMA_DIR = "schema/"

UIGF_SCHEMA_v3 = "UIGF_v3.0_Schema.json"
UIGF_SCHEMA_v4 = "UIGF_v4.2_Schema.json"
SRGF_SCHEMA_v1 = "SRGF_v1.0_Schema.json"

UIGF_SCHEMA_v4a = "UIGF_v4.2a_Schema.json"

def check_schema(schema_path, data_path):
    try:
        import jsonschema
    except ImportError:
        print("jsonschema not installed, installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonschema"])
        import jsonschema

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    validator = jsonschema.Draft7Validator(schema)
    errors = list(validator.iter_errors(data))
    if not errors:
        print("Schema is valid.")
    else:
        for error in errors:
            print(f"Error at {error.json_path}: {error.message}")

if __name__ == "__main__":
    schemas = [
        UIGF_SCHEMA_v3,
        UIGF_SCHEMA_v4,
        SRGF_SCHEMA_v1,
        UIGF_SCHEMA_v4a
    ]
    
    print("Available schemas:")
    for i, schema_file in enumerate(schemas):
        print(f"{i + 1}: {schema_file}")
    
    schema_choice = input(f"Select a schema to check against (1-{len(schemas)}): ")
    try:
        schema_idx = int(schema_choice) - 1
        if schema_idx < 0 or schema_idx >= len(schemas):
            print("Invalid schema choice.")
            sys.exit(1)
        selected_schema = SCHEMA_DIR + schemas[schema_idx]
    except ValueError:
        print("Invalid input.")
        sys.exit(1)

    data_path = input("Enter the path to the JSON file to check: ")
    
    import os
    if not os.path.exists(data_path):
        print("File not found.")
        sys.exit(1)

    check_schema(selected_schema, data_path)
