import os
import shutil
from datetime import datetime

# Variables
#img_dir = "/home/wrf/uems/runs/southern_africa/emsprd/grads/d02htm/images"  # Source directory (images directory)
dest_dir = "/home/wrf/deployed/webb-downloading/wx_presentation/images"   # Destination directory (update this path)
img_dir = "/home/wrf/deployed/webb-downloading/src/services/station_images"# Meteograms directory

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')                         # Current timestamp for logging

    # Check if the source directory exists
def copy_eps_to_images_folder(img_dir):
    if os.path.isdir(img_dir):
        print(f"Source directory exists: {img_dir}")

        # Copy the contents of the source directory to the destination directory
        try:
            for item in os.listdir(img_dir):
                src_path = os.path.join(img_dir, item)
                dest_path = os.path.join(dest_dir, item)
                if os.path.isfile(src_path):
                    shutil.copy2(src_path, dest_path)  # Copy file with metadata
                    print(f"Copied file: {src_path} to {dest_path}")
                elif os.path.isdir(src_path):
                    shutil.copytree(src_path, dest_path, dirs_exist_ok=True)  # Copy subdirectory
                    print(f"Copied directory: {src_path} to {dest_path}")

            print(f"Finished copying contents of {img_dir} to {dest_dir} at {now}")
        except Exception as e:
            print(f"Error: Failed to copy contents of {img_dir} to {dest_dir}. Exception: {e}")
    else:
        print(f"Source directory does not exist: {img_dir}")



copy_eps_to_images_folder(img_dir)