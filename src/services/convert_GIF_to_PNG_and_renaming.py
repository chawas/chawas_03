import os

import sys
from PIL import Image
sys.path.append('/home/wrf/deployed/webb-downloading/src/services')
#from texstudio_makefile11 import run_texstudio_makefile
#from texstudio_makefile import run_texstudio_makefile

sys_path = sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(sys_path)
#from src.services.convrt_GIF_to_PNG import source_folder

# Define the path to your image folder
#image_folder = 'path/to/your/image_folder'
image_folder = "/home/wrf/deployed/webb-downloading/wx_presentation/images"  # Update this with the correct path
print(image_folder)
#source_folder = "/home/wrf/deployed/webb-downloading/wx_presentation"

# Function to rename files by replacing '.' with '_', except for the extension
def rename_file(filename):
    name, ext = os.path.splitext(filename)  # Split name and extension
    name = name.replace('.', '_')  # Replace '.' with '_' in the name
    print(name)
    return f"{name}{ext}"  # Rebuild the full file name


# Function to convert GIF to PNG and rename files
def convert_and_rename_images(folder_path):
    for filename in os.listdir(folder_path):
        # Full path to the file
        file_path = os.path.join(folder_path, filename)

        # If the file is a GIF, convert it to PNG
        if filename.lower().endswith('.gif'):
            # Open the GIF file
            with Image.open(file_path) as img:
                # Convert the image to PNG
                png_filename = filename.replace('.gif', '.png')
                png_file_path = os.path.join(folder_path, png_filename)
                img.save(png_file_path, 'PNG')  # Save as PNG

                # Optionally, remove the original GIF file after conversion
                os.remove(file_path)  # Delete the original GIF

            # Update the filename for renaming
            filename = png_filename
            print(filename)

        # Rename the file (GIFs are now PNGs, and we rename PNG files too)
        new_filename = rename_file(filename)
        new_file_path = os.path.join(folder_path, new_filename)

        # Rename the file by replacing '.' with '_' in the filename
        os.rename(os.path.join(folder_path, filename), new_file_path)
        print(f"Renamed and processed: {filename} -> {new_filename}")


if __name__ == "__main__":
    convert_and_rename_images(image_folder)
 #   run_texstudio_makefile()