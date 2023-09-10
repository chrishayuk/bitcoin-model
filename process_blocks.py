import argparse
import os
import json
from processor_module.block_processor import process_block
from processor_module.file_handler import read_tsv, write_jsonl
from processor_module.metadata_manager import save_metadata
from datetime import datetime

def read_previous_metadata(output_folder, datetime_from_previous_file):
    try:
        with open(os.path.join(output_folder, f"metadata-{datetime_from_previous_file}.json"), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def main(args):
    headers, lines = read_tsv(args.input)
    json_data_list = []
    previous_block = None

    for line in lines:
        block_entry = process_block(headers, line, previous_block)
        json_data_list.append(block_entry)
        previous_block = block_entry['data']

    datetime_from_previous_file = datetime.strptime(json_data_list[0]['data']['time'], "%Y-%m-%d %H:%M:%S").strftime('%Y%m%d')
    previous_metadata = read_previous_metadata(args.output, datetime_from_previous_file)
    output_filename = os.path.join(args.output, f"blocks-list-{datetime_from_previous_file}.jsonl")

    write_jsonl(output_filename, json_data_list)
    save_metadata(json_data_list, args.output, datetime_from_previous_file, previous_metadata)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert TSV blockchain data to JSONL format.')
    parser.add_argument('--input', required=True, help='Path to the input TSV file.')
    parser.add_argument('--output', required=True, help='Path to the output folder.')

    args = parser.parse_args()
    main(args)
