import datetime
import sys
import time
import os
import logging
from config_manager import ConfigManager
from downloader_module.bitcoin_blocks_file_downloader import download_bitcoin_file_for_date

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def next_date(start_date_str):
    """Get the next date to download, starting from the given date."""
    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d').date()
    except ValueError:
        logging.error("Invalid date format. Expected format is YYYYMMDD.")
        sys.exit(1)
    
    today = datetime.date.today()
    current_date = start_date

    while current_date <= today:
        yield current_date
        current_date += datetime.timedelta(days=1)

def main():
    if len(sys.argv) != 2:
        logging.error("Usage: python script_name.py YYYYMMDD")
        sys.exit(1)

    # Initialize ConfigManager and validate it
    config = ConfigManager()
    download_path = config.downloads_blocks_folder
    rate_limit = config.rate_limit_seconds

    if not download_path:
        logging.error("'downloads_blocks_folder' not set in config.ini.")
        sys.exit(1)

    # Ensure download folder exists
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    dates = next_date(sys.argv[1])
    for current_date in dates:
        success = download_bitcoin_file_for_date(current_date, download_path)

        if success:
            logging.info(f"Downloaded the file for date: {current_date.strftime('%Y%m%d')}")
        else:
            # If a file fails to download even after retries, exit the script
            logging.error(f"Failed to download file for date: {current_date.strftime('%Y%m%d')} after maximum retries.")
            sys.exit(1)

        # Introduce a rate limit delay unless it's the last date
        if current_date != datetime.date.today():
            time.sleep(rate_limit)

if __name__ == '__main__':
    main()
