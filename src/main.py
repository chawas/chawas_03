from datetime import datetime
from services.download_rest import download_images, copy_directory_contents, verify_images_in_folder
from src.config import url_list
from services.convert_GIF_to_PNG_and_renaming import convert_and_rename_images
from services.download_satellite_imgs4 import run_satellite_download
import os
import sys
from services.extract_forecast61 import generate_station_forecasts


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#sys.path.append('/home/wrf/deployed/webb-downloading/src')
source_directory = '/home/wrf/deployed/chawas_03/wx_presentation/images/' + datetime.now().strftime("%Y%m%d")
target_directory = '/home/wrf/deployed/chawas_03/wx_presentation/images/'


def main():
    print("1. Starting Satellite image download...")
    run_satellite_download()

    from services.download_eps4 import run_eps_download
    print("2. Starting EPS download...")
    run_eps_download()

    print("3. Starting image download...")  # Debug: Confirm download start
    # Run the function to download the images
    download_images(url_list, source_directory)
    print(f"Images downloaded to {source_directory}")

    # Verify downloaded images
    print("4. Verifying images...")
    verify_images_in_folder(source_directory)

    # Copy images to the main images directory
    print("5. Copying images...")
    copy_directory_contents(source_directory, target_directory)

    # Convert GIF images to PNG and rename them
    print("6. Converting and renaming images...")
    convert_and_rename_images(folder_path=target_directory)

    # Extract station forecasts
    print("7. Converting and renaming images...")
    convert_and_rename_images(folder_path=target_directory)

    # Generate station forecasts
    print("8. Generating station forecasts...")
    generate_station_forecasts()  # Call the function to generate the LaTeX content

if __name__ == '__main__':
    main()
    from services.texstudio_makefile11 import run_texstudio_makefile
    run_texstudio_makefile()
    print("Opening TeXstudio for editing...")
    from services.texstudioMakefile21 import open_texstudio_for_editing
    open_texstudio_for_editing()