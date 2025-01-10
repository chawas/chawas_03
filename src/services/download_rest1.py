import os
import json
import requests
import shutil
from datetime import datetime
from PIL import Image
from src.config import CHROMEDRIVER_PATH, MAX_RETRIES, DELAY_SECONDS, URL_LIST, LOGS_DIR, IMAGES_DIR

print("Chromedriver Path:", CHROMEDRIVER_PATH)
print("Max Retries:", MAX_RETRIES)
print("Delay Seconds:", DELAY_SECONDS)
print("URL List:", URL_LIST)
print("LOGS_DIR:", LOGS_DIR)
LOG_FILE = os.path.join(LOGS_DIR, "satellite.log")

def download_images_rest(url_list, save_dir):
    """
    Download images from the provided URL list and save them to the specified directory.
    """
    # Create the directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    for i, url in enumerate(url_list):
        try:
            # Fetch content from the URL
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Check if the request was successful

            # Extract the file name from the URL
            file_name = os.path.join(save_dir, url.split("/")[-1])
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded {url} as {file_name}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")

def verify_images_in_folder(source_dir):
    """
    Verify all images in a given folder and report any issues.
    """
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)

        # Only process files with image extensions
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
            try:
                with Image.open(file_path) as img:
                    img.verify()  # Check for image integrity
                print(f"{filename}: OK")
            except (IOError, SyntaxError) as e:
                print(f"{filename}: Corrupted or unreadable - {e}")

def copy_directory_contents(source_dir, target_dir):
    """
    Copy the contents of the source directory to the target directory.
    """
    try:
        # Check if the target directory exists; if not, create it
        os.makedirs(target_dir, exist_ok=True)
        print(f"Target directory ready: {target_dir}")

        # Copy each item in the source directory to the target directory
        for item in os.listdir(source_dir):
            source_path = os.path.join(source_dir, item)
            target_path = os.path.join(target_dir, item)

            try:
                # Copy file or directory
                if os.path.isdir(source_path):
                    shutil.copytree(source_path, target_path, dirs_exist_ok=True)
                    print(f"Copied directory: {source_path} to {target_path}")
                else:
                    shutil.copy2(source_path, target_path)
                    print(f"Copied file: {source_path} to {target_path}")
            except Exception as copy_error:
                print(f"Error copying {item}: {copy_error}")

    except Exception as e:
        print(f"Error during copy operation: {e}")
    finally:
        print("Copy operation completed.")

if __name__ == "__main__":
    print("1. Starting image download...")
    download_images_rest(URL_LIST, SOURCE_IMAGES_DIR)

    print("2. Verifying downloaded images...")
    verify_images_in_folder(SOURCE_IMAGES_DIR)

    print("3. Copying images to the target directory...")
    copy_directory_contents(SOURCE_IMAGES_DIR, TARGET_DIR)

    print("Process completed.")
