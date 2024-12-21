
import os
import subprocess
from datetime import datetime
import time

# Define the working directory
tex_directory = "/home/wrf/deployed/webb-downloading/wx_presentation"
os.chdir(tex_directory)

# Print the current working directory
print("Current working directory:", os.getcwd())


def run_texstudio_makefile():
    # Run 'make' to compile the LaTeX file
    try:
        print("Running 'make' to compile the LaTeX document...")
        subprocess.run(['make'], check=True)  # Ensure make is successful
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running make: {e}")
        # Skip opening TeXstudio if make fails
        return


    # Construct the PDF filename with today's date
    today_date = datetime.now().strftime('%Y%m%d')
    pdf_filename = f"wx_presentation_{today_date}.pdf"
    pdf_path = os.path.join(tex_directory, pdf_filename)

    # Check if PDF is created after `make`
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_filename} not found. Compilation might have failed.")
        return

    # Set the QT_QPA_PLATFORM variable to suppress Wayland warnings
    os.environ['QT_QPA_PLATFORM'] = 'xcb'

    # Open TeXstudio for the PDF (after make is done)
    print("Opening TeXstudio to view the PDF...")
    try:
        subprocess.Popen(['texstudio', '--reuse-instance', pdf_filename])  # Use Popen to avoid blocking
    except Exception as e:
        print(f"An error occurred while opening {pdf_filename} in TeXstudio: {e}")

def open_texstudio_for_editing():
    # Open TeXstudio to edit the LaTeX source file
    print("Opening TeXstudio to edit the LaTeX file...")
    subprocess.Popen(['texstudio', '--reuse-instance', 'wx_presentation.tex'])  # Use Popen to avoid blocking

# Run the makefile and open TeXstudio
run_texstudio_makefile()

# Optionally, open TeXstudio for editing the LaTeX file again
# open_texstudio_for_editing()
open_texstudio_for_editing()