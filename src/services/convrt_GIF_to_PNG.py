from PIL import Image
import os


def rename_file(filename):
    name, ext = os.path.splitext(filename)  # Split name and extension
    name = name.replace('.', '_')  # Replace '.' with '_' in the name
    print(name)
    return f"{name}{ext}"  # Rebuild the full file name


# Function to convert GIF to PNG
def convert_gif_to_png(source_folder, output_folder=None):
    # If output folder is not specified, save the PNGs in the source folder
    if output_folder is None:
        output_folder = source_folder

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the source folder
    for filename in os.listdir(source_folder):
        if filename.endswith(".gif"):  # Check if the file is a GIF
            gif_path = os.path.join(source_folder, filename)

            # Open the GIF file
            with Image.open(gif_path) as gif_image:
                # Extract the base name (without extension) of the file
                base_name = os.path.splitext(filename)[0]

                # Convert and save as PNG
                png_path = os.path.join(output_folder, f"{base_name}.png")
                gif_image.convert("RGBA").save(png_path, "PNG")

                print(f"Converted {filename} to {base_name}.png")
            # filename = f"{base_name}.png"
            # print(filename)

            # # Rename the file (GIFs are now PNGs, and we rename PNG files too)
            # new_filename = rename_file(filename)
            # new_file_path = os.path.join(folder_path, new_filename)
            #
            # # Rename the file by replacing '.' with '_' in the filename
            # os.rename(os.path.join(folder_path, filename), new_file_path)
            # print(f"Renamed and processed: {filename} -> {new_filename}")
# Specify the source folder where your GIF and PNG files are located
source_folder = "/home/wrf/deployed/webb-downloading/wx_presentation/images"  # Update this with the correct path
print(source_folder)

convert_gif_to_png(source_folder,output_folder=None)
# (Optional) Specify the output folder to save the PNGs (If different from source folder)
# output_folder = "/path/to/output/folder"