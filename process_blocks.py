import os
import json
import argparse
from datetime import datetime
from processor_module.block_processor import process_block
from processor_module.file_handler import read_tsv, write_jsonl
from config_manager import ConfigManager
from processor_module.metadata_manager import save_metadata, get_previous_block

def main(date_string):
    config = ConfigManager()
    input_file = os.path.join(config.downloads_blocks_folder, f"blockchair_bitcoin_blocks_{date_string}.tsv")

    # Use the 'processed_blocks_folder' for the processed blocks output
    output_folder = config.processed_blocks_folder 

    # Fetch the previous block from the metadata of the day before
    previous_block = get_previous_block(output_folder, date_string)

    headers, lines = read_tsv(input_file)
    json_data_list = []

    for line in lines:
        block_entry = process_block(headers, line, previous_block)
        json_data_list.append(block_entry)
        previous_block = block_entry['data']

    datetime_from_current_file = datetime.strptime(json_data_list[0]['data']['time'], "%Y-%m-%d %H:%M:%S").strftime('%Y%m%d')
    output_filename = os.path.join(output_folder, f"blocks-list-{datetime_from_current_file}.jsonl")

    write_jsonl(output_filename, json_data_list)
    save_metadata(json_data_list, output_folder, date_string)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert TSV blockchain data to JSONL format.')
    parser.add_argument('date', help='Start date in YYYYMMDD format.')

    args = parser.parse_args()
    main(args.date)
