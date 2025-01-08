from datetime import datetime
from services.download_rest import download_images, copy_directory_contents, verify_images_in_folder
from services.convert_GIF_to_PNG_and_renaming import convert_and_rename_images
from services.download_satellite_imgs5 import run_satellite_download
from services.extract_forecast61 import generate_station_forecasts
from services.download_eps4 import run_eps_download
from config import BASE_DIR, IMAGES_DIR, OUTPUT_DIR

import os
import sys
import time

# Add BASE_DIR to the system path to locate modules
sys.path.append(BASE_DIR)

# Derive dynamic paths
SOURCE_DIR = os.path.join(IMAGES_DIR, datetime.now().strftime("%Y%m%d"))
TARGET_DIR = IMAGES_DIR


def main():
    start_time = time.time()
    print("1. Starting Satellite image download...")
    run_satellite_download()

    print("2. Starting EPS download...")
    #run_eps_download()

    print("3. Starting image download...")
    #download_images(url_list=None, source_directory=SOURCE_DIR)  # Assuming url_list is defined in the module
    print(f"Images downloaded to {SOURCE_DIR}")

    print("4. Verifying images...")
    #verify_images_in_folder(SOURCE_DIR)

    print("5. Copying images...")
    #copy_directory_contents(SOURCE_DIR, TARGET_DIR)

    print("6. Converting and renaming images...")
    #convert_and_rename_images(folder_path=TARGET_DIR)

    print("7. Generating station forecasts...")
    #generate_station_forecasts()



    end_time = time.time()
    print(f"Script completed in {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    main()
    print("8. Running TeXstudio Makefile...")
    from services.texstudio_makefile11 import run_texstudio_makefile
    #run_texstudio_makefile()

    from services.texstudioMakefile21 import open_texstudio_for_editing
    print("9. Opening TeXstudio for editing...")
    #open_texstudio_for_editing()