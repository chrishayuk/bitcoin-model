import os
from .download_utilities import download_file, decompress_gz_file

BASE_URL = "https://gz.blockchair.com/bitcoin/blocks/"

def construct_filename(date):
    """Construct the filename based on the date."""
    return f"blockchair_bitcoin_blocks_{date.strftime('%Y%m%d')}.tsv.gz"

def download_bitcoin_file_for_date(date, download_path, max_retries=10):
    """
    Download the file for the given date.
    Returns True if successful, otherwise False.
    """
    filename = construct_filename(date)
    url = BASE_URL + filename

    # Create the full path where the file will be saved
    full_path = os.path.join(download_path, filename)

    # Download the file
    success = download_file(url, full_path, stream=True, max_retries=max_retries)

    if success:
        # Decompress the .gz file after downloading
        decompressed_path = decompress_gz_file(full_path)

        # Optionally, if you want to remove the .gz file after decompressing
        os.remove(full_path)

        # Return the path of the decompressed file, or True, depending on your needs
        return decompressed_path

    return False
