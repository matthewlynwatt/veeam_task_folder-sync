import os
import shutil
import time
import argparse
import logging


def sync_folders(source_folder, replica_folder, log_folder):
    # check to see if folder exists
    if not os.path.exists(source_folder):
        raise FileNotFoundError(
            f"Source folder '{source_folder}' does not exist")

    # check to see if replica folder exists. If not, create one
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    # Configure logging
    logging.basicConfig(filename=log_file, levvel=logging.INFO,
                        format='%(asctime)s - %(message)s')

    # Sync folders
    for root, dirs, files in os.walk(source_folder):
        relative_path = os.path.relpath(root, source_folder)
        replica_path = os.path.join(replica_folder, replica_path)

        # Check to see if replica folder structure matches source
        if not os.path.exists(relative_path):
        os.makedirs(relative_path)

        # Copy files
        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_path, file)

            if not os.path.exists(replica_file) or os.path.getmtime(source_file) > os.path.getmtime(replica_file)
            shutil.copy2(source_file, replica_file)
            logging.info(f"Copied '{source_file}' to '{replica_file}'")

        for file in os.listdir(replica_path):
            replica_file = os.path.join(replica_path, file)
            source_file = os.path.join(root, file)

            if not os.path.exists(source_file):
                os.remove(replica_file)
                logging.info(f"Removed '{replica_file}'")


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Folder synchronization program')
    parser.add_argument('source_folder', help='Path to source folder')
    parser.add_argument('replica_folder', help='Path to replica folder')
    parser.add_argument('sync_interval', type=int,
                        help='Synchronization interval in seconds')
    parser.add_argument('log_file', help='Path to log file')
    args = parser.parse_args()

    while True:
        sync_folders(args.source_folder,
                     args.replica_folder, args.log_file)
        time.sleep(args.sync_interval)


if _name_ == "_main_":
    main()

# python folder_sync.py /path/to/source/folder /path/to/replica/folder 60 path/to/logfile.log
