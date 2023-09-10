import datetime
import sys
import time
import os

from downloader_module.bitcoin_blocks_file_downloader import download_bitcoin_file_for_date

def next_date(start_date_str):
    """Get the next date to download, starting from the given date."""
    try:
        start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d').date()
    except ValueError:
        print("Invalid date format. Expected format is YYYYMMDD.")
        sys.exit(1)
    
    today = datetime.date.today()
    current_date = start_date

    while current_date <= today:
        yield current_date
        current_date += datetime.timedelta(days=1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py YYYYMMDD")
        sys.exit(1)

    dates = next_date(sys.argv[1])
    for current_date in dates:
        # Create a downloads/blocks sub-directory if it doesn't exist
        download_path = os.path.join('downloads', 'blocks')
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        success = download_bitcoin_file_for_date(current_date, download_path)
        
        if success:
            # Print which file was downloaded
            print(f"Downloaded the file for date: {current_date.strftime('%Y%m%d')}")

            # Rate limit unless it's the last date
            if current_date != datetime.date.today():
                time.sleep(10)

if __name__ == '__main__':
    main()