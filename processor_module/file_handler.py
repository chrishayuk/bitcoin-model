import json

def read_tsv(input_file):
    """Read TSV from file and return headers and data lines."""
    with open(input_file, 'r') as f:
        data = f.read().strip().split("\n")
    headers = data[0].split("\t")
    return headers, data[1:]

def write_jsonl(output_file, json_data):
    """Write a list of JSON objects to a file in JSONL format."""
    with open(output_file, 'w') as outfile:
        for item in json_data:
            outfile.write(json.dumps(item) + "\n")