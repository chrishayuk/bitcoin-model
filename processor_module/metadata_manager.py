import os
import json
from datetime import datetime, timedelta

def get_previous_block(output_folder, current_date_string):
    # Convert the date string to a datetime object
    current_date = datetime.strptime(current_date_string, "%Y%m%d")

    # Subtract one day to get the previous date
    previous_date = current_date - timedelta(days=1)

    # Convert back to string format
    previous_date_string = previous_date.strftime("%Y%m%d")

    # Load the metadata file for the previous date
    metadata_file_path = os.path.join(output_folder, f"blocks-metadata-{previous_date_string}.json")

    try:
        with open(metadata_file_path, 'r') as metafile:
            metadata = json.load(metafile)
            return {
                'id': metadata.get('end_block'),
                'chainwork': metadata.get('end_block_hash') # You might need to adjust this if "chainwork" info is stored differently.
            }
    except FileNotFoundError:
        return None
    
def read_metadata(output_folder, date_string):
    try:
        with open(os.path.join(output_folder, f"blocks-metadata-{date_string}.json"), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_metadata(json_data, output_folder, date_string):
    metadata_filename = os.path.join(output_folder, f"blocks-metadata-{date_string}.json")
    
    previous_metadata = read_metadata(output_folder, date_string)
    previous_block_hash = previous_metadata.get("end_block_hash") if previous_metadata else None

    metadata = {
        "description": "Blockchain block details",
        "created_date": datetime.now().strftime('%Y-%m-%d'),
        "total_blocks": len(json_data),
        "start_block": json_data[0]['data']['id'] if json_data else None,
        "end_block": json_data[-1]['data']['id'] if json_data else None,
        "start_block_time": json_data[0]['data']['time'] if json_data else None,
        "end_block_time": json_data[-1]['data']['time'] if json_data else None,
        "previous_block_hash": previous_block_hash,
        "start_block_hash": json_data[0]['data']['hash'] if json_data else None,
        "end_block_hash": json_data[-1]['data']['hash'] if json_data else None
    }

    with open(metadata_filename, "w") as metafile:
        json.dump(metadata, metafile, indent=4)
