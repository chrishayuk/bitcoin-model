import requests
import logging
import time
import gzip
import os

# Initialize logging for the module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_file(url, filepath, stream=False, max_retries=3):
    retry_count = 0
    while retry_count < max_retries:
        response = requests.get(url, stream=stream)
        if response.status_code == 200:
            if stream:
                with open(filepath, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
            else:
                with open(filepath, 'wb') as file:
                    file.write(response.content)
            return True
        else:
            print(f"Failed to download {url}. Status code: {response.status_code}")
            retry_count += 1
            time.sleep(2**retry_count)  # Exponential backoff

    print(f"Failed to download {url} after {max_retries} attempts.")
    return False


def decompress_gz_file(gz_filepath, output_filepath=None):
    """
    Decompress a .gz file. 
    If output_filepath is not provided, the decompressed file will be saved with the original name without the .gz extension.
    """
    if not output_filepath:
        output_filepath = os.path.splitext(gz_filepath)[0]  # remove the .gz extension

    with gzip.open(gz_filepath, 'rb') as f_in:
        with open(output_filepath, 'wb') as f_out:
            f_out.write(f_in.read())

    return output_filepath  # return the path of the decompressed file
