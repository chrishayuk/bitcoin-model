import re
from datetime import datetime
import random

def extract_tags_from_coinbase(coinbase_hex):
    try:
        coinbase_ascii = bytes.fromhex(coinbase_hex).decode('ascii', 'ignore')
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

    coinbase_tags = extract_tags_from_coinbase(block_data["coinbase_data_hex"])
    if coinbase_tags:
        block_data["coinbase_tags"] = coinbase_tags

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
    
    if previous_block and 'id' in previous_block:
        time_diff = block.get('time_diff_seconds', 0)
        chosen_description += f" Following block {previous_block['id']}, block {block['id']} was created {time_diff} seconds later."

        prev_chainwork = previous_block.get('chainwork', "0")
        if isinstance(prev_chainwork, str):
            try:
                prev_chainwork = int(prev_chainwork, 16)
            except ValueError:
                prev_chainwork = 0
        elif prev_chainwork is None:
            prev_chainwork = 0

        chainwork_diff = block['chainwork'] - prev_chainwork
        chosen_description += f" The computational effort increased by {chainwork_diff} units from block {previous_block['id']} to block {block['id']}."

        print(f"Current block's chainwork: {block['chainwork']}")
        print(f"Previous block's chainwork: {prev_chainwork}")
        print(f"Computed chainwork_diff: {chainwork_diff}")

    return chosen_description


def miner_features(block, previous_block):
    features = {}
    time_format = "%Y-%m-%d %H:%M:%S"
    block_time = datetime.strptime(block["time"], time_format)
    median_time = datetime.strptime(block["median_time"], time_format)
    features["time_diff_seconds"] = (block_time - median_time).seconds

    if previous_block:
        prev_chainwork = previous_block.get("chainwork", "0")  # Default to "0" if chainwork is missing
        if isinstance(prev_chainwork, str):
            try:
                prev_chainwork = int(prev_chainwork, 16)
            except ValueError:
                prev_chainwork = 0  # Set to 0 if conversion fails
        elif prev_chainwork is None:  # Handle case where chainwork is explicitly set to None
            prev_chainwork = 0

        features["chainwork_diff"] = block["chainwork"] - prev_chainwork

        # 1. Difference Analysis
        features["nonce_diff_from_last"] = int(block.get("nonce", 0)) - int(previous_block.get("nonce", 0))
        
        # 2. Cycle Patterns
        features["starts_from_known_reset_value"] = block.get("nonce") == '0'
        
        # 3. Time-based Analysis
        features["avg_nonce_per_second"] = features["nonce_diff_from_last"] / (features["time_diff_seconds"] or 1) # Avoid division by zero
    else:
        features["chainwork_diff"] = 0  # Assigning 0 when there's no previous block

    return features

