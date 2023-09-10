import re
from datetime import datetime
import random

def extract_tags_from_coinbase(coinbase_hex):
    try:
        # Convert hex to ASCII
        coinbase_ascii = bytes.fromhex(coinbase_hex).decode('ascii', 'ignore')
        
        # Use regex to extract human-readable strings that are longer than, let's say, 5 characters
        tags = re.findall(r"[A-Za-z0-9!@#$%^&*()_+{}:\[\];'<>,.?~\\\-]{5,}", coinbase_ascii)
        
        return tags
    except Exception as e:
        return []
    
def process_block(headers, line, previous_block=None):
    included_columns = ["id", "hash", "time", "median_time", "size", "version", "merkle_root", "nonce", 
                        "bits", "difficulty", "chainwork", "coinbase_data_hex","transaction_count", "input_count", 
                        "output_count", "input_total", "output_total", "fee_total", "cdd_total", "generation", 
                        "reward", "guessed_miner"]

    values = line.split("\t")
    block_data = {headers[i]: values[i] for i in range(len(values)) if headers[i] in included_columns}
    
    block_data["chainwork"] = int(block_data["chainwork"], 16)
    for key in ["reward", "input_total", "output_total", "fee_total", "generation"]:
        block_data[key] = float(block_data[key])

    # Coinbase Data Analysis
    coinbase_tags = extract_tags_from_coinbase(block_data["coinbase_data_hex"])
    if coinbase_tags:
        block_data["coinbase_tags"] = coinbase_tags

    # Add the length of the coinbase data
    block_data["coinbase_length"] = len(block_data["coinbase_data_hex"])

    miner_features_dict = miner_features(block_data, previous_block if previous_block else None)
    for key, value in miner_features_dict.items():
        block_data[key] = value

    if block_data.get("guessed_miner") == "Unknown":
        del block_data["guessed_miner"]

    description = generate_description(block_data, previous_block)
    block_entry = {
        "data": block_data,
        "description": description
    }

    return block_entry

def generate_description(block, previous_block):
    descriptions = [
        f"The block with ID {block['id']} has the hash value of {block['hash']}. It was created on {block['time']} with a median time of {block['median_time']}. This block contains {block['transaction_count']} transactions with {block['input_count']} inputs and {block['output_count']} outputs.",
        f"Block {block['id']} with hash {block['hash']} was timestamped at {block['time']}. Its median time is {block['median_time']}. It comprises {block['transaction_count']} transactions, {block['input_count']} inputs, and {block['output_count']} outputs.",
    ]

    chosen_description = random.choice(descriptions)
    if previous_block:
        time_diff = block['time_diff_seconds']
        chosen_description += f" Following block {previous_block['id']}, block {block['id']} was created {time_diff} seconds later."
        
        chainwork_diff = block['chainwork'] - previous_block['chainwork']
        chosen_description += f" The computational effort increased by {chainwork_diff} units from block {previous_block['id']} to block {block['id']}."

    return chosen_description

def miner_features(block, previous_block):
    features = {}
    time_format = "%Y-%m-%d %H:%M:%S"
    block_time = datetime.strptime(block["time"], time_format)
    median_time = datetime.strptime(block["median_time"], time_format)
    features["time_diff_seconds"] = (block_time - median_time).seconds

    current_chainwork = block["chainwork"]
    if previous_block:
        features["chainwork_diff"] = current_chainwork - previous_block["chainwork"]
        
        # 1. Difference Analysis
        features["nonce_diff_from_last"] = int(block["nonce"]) - int(previous_block["nonce"])
        
        # 2. Cycle Patterns
        features["starts_from_known_reset_value"] = block["nonce"] == '0'
        
        # 3. Time-based Analysis
        features["avg_nonce_per_second"] = features["nonce_diff_from_last"] / features["time_diff_seconds"]
        
    return features
