import os
import subprocess
from datetime import datetime

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
        return

    # Construct the PDF filename with today's date
    today_date = datetime.now().strftime('%Y%m%d')
    pdf_filename = f"wx_presentation_{today_date}.pdf"

    # Set the QT_QPA_PLATFORM variable to suppress Wayland warnings
    os.environ['QT_QPA_PLATFORM'] = 'xcb'

    # Open TeXstudio for the PDF (after make is done)
    print("Opening TeXstudio to view the PDF...")
    try:
        # Open the PDF in TeXstudio after make
        subprocess.Popen(['texstudio', '--reuse-instance', pdf_filename])  # Use Popen to avoid blocking
    except FileNotFoundError:
        print(f"Error: {pdf_filename} not found.")
    except Exception as e:
        print(f"An error occurred while opening {pdf_filename} in TeXstudio: {e}")


def open_texstudio_for_editing():
    # Open TeXstudio to edit the LaTeX source file
    print("Opening TeXstudio to edit the LaTeX file...")
    subprocess.Popen(['texstudio', '--reuse-instance', 'wx_presentation.tex'])  # Use Popen to avoid blocking


# Run the makefile and open TeXstudio
run_texstudio_makefile()

# Optionally, open TeXstudio for editing the LaTeX file again
#open_texstudio_for_editing()
