import os
import subprocess
from datetime import datetime
import time

# Define the working directory
tex_directory = "/home/wrf/deployed/chawas_03/wx_presentation"
os.chdir(tex_directory)  # Set working directory to LaTeX files

# Suppress Wayland warnings by setting the display environment for X11
os.environ["QT_QPA_PLATFORM"] = "xcb"

# Path to TeXstudio (update this if necessary)
texstudio_path = '/home/wrf/uems/util/grads/bin/texstudio'

# Check if TeXstudio exists at the specified path
if not os.path.isfile(texstudio_path):
    print("Error: TeXstudio application not found at the specified path.")
    exit(1)

    # Run `make` to compile the LaTeX document
def run_texstudio_makefile():
    try:
        subprocess.run(['make'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running make: {e}")
        exit(1)

    # Construct the PDF filename with today's date
    today_date = datetime.now().strftime('%Y%m%d')
    pdf_filename = f"wx_presentation_{today_date}.pdf"

    # Check if PDF was created successfully
    pdf_path = os.path.join(tex_directory, pdf_filename)
    if os.path.isfile(pdf_path):
        print(f"PDF file {pdf_filename} created successfully at {pdf_path}.")

        try:
            # Open the `.tex` and PDF files together in a single TeXstudio instance
            texstudio_process = subprocess.Popen([texstudio_path, '--reuse-instance', 'wx_presentation.tex', pdf_filename])

            # Focus on TeXstudio if `wmctrl` is available
            time.sleep(1)
            subprocess.run(['wmctrl', '-a', 'TeXstudio'])

        except Exception as e:
            print(f"An error occurred while opening files in TeXstudio: {e}")
    else:
        print(f"Error: {pdf_filename} not found. Compilation might have failed.")

run_texstudio_makefile()