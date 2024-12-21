import os
import shutil
from datetime import datetime

# Variables
src_dir = "/home/wrf/uems/runs/southern_africa/emsprd/grads/d02htm"  # Source directory
grads_dir = "/home/wrf/uems/runs/southern_africa/emsprd/grads"       # GrADS directory
dest_dir = "/path/to/destination_directory"
img_dir = "/home/wrf/deployed/webb-downloading/src/services/station_images"# Meteograms directory
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')                  # Current timestamp for logging

# Check if the source directory exists
if os.path.isdir(src_dir):
    print(f"Source directory exists: {src_dir}")

    # Change to the GrADS directory
    try:
        os.chdir(grads_dir)
        print(f"Changed to directory: {grads_dir}")

        # Copy the source directory to the destination
        try:
            shutil.copytree(src_dir, os.path.join(dest_dir, "d02htm"), dirs_exist_ok=True)
            print(f"Finished copying {src_dir} to {dest_dir} at {now}")
        except Exception as e:
            print(f"Error: Failed to copy {src_dir} to {dest_dir}. Exception: {e}")
    except FileNotFoundError:
        print(f"Error: Directory {grads_dir} does not exist.")
else:
    print(f"Source directory does not exist: {src_dir}")
