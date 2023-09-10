import os
import json
from datetime import datetime

def save_metadata(json_data, output_folder, datetime_from_previous_file, previous_metadata=None):
    metadata_filename = os.path.join(output_folder, f"blocks-metadata-{datetime_from_previous_file}.json")
    
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
