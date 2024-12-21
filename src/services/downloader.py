import os
import requests
import shutil
from datetime import datetime
from PIL import Image


def download_images(url_list, save_dir):
    # Create the directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
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
    """Verify all images in a given folder and report any issues."""
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


# Example usage
#folder_path = "/home/wrf/deployed/webb-downloading/wx_presentation/images"
#verify_images_in_folder(folder_path)




def copy_directory_contents(source_dir, target_dir):
    try:
        # Change to the source directory
        os.chdir(source_dir)
        print(f"Changed to directory: {source_dir}")

        # Check if target directory exists, if not, create it
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            print(f"Created target directory: {target_dir}")

        # Copy each item in the source directory to the target directory
        for item in os.listdir(source_dir):
            source_path = os.path.join(source_dir, item)
            target_path = os.path.join(target_dir, item)

            try:
                # Copy file or directory
                if os.path.isdir(source_path):
                    shutil.copytree(source_path, target_path)
                    print(f"Copied directory: {source_path} to {target_path}")
                else:
                    shutil.copy2(source_path, target_path)
                    print(f"Copied file: {source_path} to {target_path}")
            except Exception as copy_error:
                print(f"Error copying {item}: {copy_error}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Print completion message
        print("Copy operation completed.")


# Define source and target directories
#'/home/wrf/deployed/webb-downloading/wx_presentation/images/' + datetime.now().strftime("%Y%m%d")
source_directory = '/home/wrf/deployed/webb-downloading/wx_presentation/images/' + datetime.now().strftime("%Y%m%d")
target_directory = '/home/wrf/deployed/webb-downloading/wx_presentation/images/'

# Run the copy function
#copy_directory_contents(source_directory, target_directory)
