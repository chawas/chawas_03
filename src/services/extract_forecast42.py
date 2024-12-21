import os
import base64
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from downloader import download_images, copy_directory_contents, verify_images_in_folder
from config import url_list
from convert_GIF_to_PNG_and_renaming import convert_and_rename_images
from download_satellite_imgs2 import run_satellite_download

# Define directories
symbols_dir = "/home/wrf/nons/python-plotting-toolbox/local_outdata/symbograms/"
target_dir = '/home/wrf/deployed/webb-downloading/wx_presentation/'
images_dir = '/home/wrf/deployed/webb-downloading/wx_presentation/images/'
os.makedirs(target_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)

output_path = os.path.join(target_dir, "station_forecast42.tex")

# Define stations
stations = {
    "Bulawayo": os.path.join(symbols_dir, "Bulawayo.html"),
    "Bindura": os.path.join(symbols_dir, "Bindura.html"),
    "Chinhoyi": os.path.join(symbols_dir, "Chinhoyi.html"),
    "Gwanda": os.path.join(symbols_dir, "Gwanda.html"),
    "Gweru": os.path.join(symbols_dir, "Gweru.html"),
    "Harare": os.path.join(symbols_dir, "Harare.html"),
    "Kadoma": os.path.join(symbols_dir, "Kadoma.html"),
    "Kwekwe": os.path.join(symbols_dir, "Kwekwe.html"),
    "Lupane": os.path.join(symbols_dir, "Lupane.html"),
    "Marondera": os.path.join(symbols_dir, "Marondera.html"),
    "Masvingo": os.path.join(symbols_dir, "Masvingo.html"),
    "Mutare": os.path.join(symbols_dir, "Mutare.html"),
    "Binga": os.path.join(symbols_dir, "Binga.html"),
    "Chimanimani": os.path.join(symbols_dir, "Chimanimani.html"),
    "ChinhoyiCaves": os.path.join(symbols_dir, "ChinhoyiCaves.html"),
    "GreatZimbabwe": os.path.join(symbols_dir, "GreatZimbabwe.html"),
    "Gonarezhou": os.path.join(symbols_dir, "Gonarezhou.html"),
    "HotSprings": os.path.join(symbols_dir, "HotSprings.html"),
    "HwangeNatPark": os.path.join(symbols_dir, "HwangeNatPark.html"),
    "Matopos": os.path.join(symbols_dir, "Matobo.html"),
    "Karoi": os.path.join(symbols_dir, "Karoi.html"),
    "Nyanga": os.path.join(symbols_dir, "Nyanga.html"),
    "VICTORIA FALLS": os.path.join(symbols_dir, "VicFalls.html"),
    "VUMBA": os.path.join(symbols_dir, "Vumba.html"),
}

# Function to create the title with dates
def generate_title():
    start_date = datetime.now()
    end_date = start_date + timedelta(days=4)
    title = f"5-DAY FORECAST FOR MAJOR CITIES: {start_date.strftime('%a %d %b')} – {end_date.strftime('%a %d %b %Y')}"
    return title

# Function to decode and save images
def decode_and_save_images(image_data_list, station_name):
    decoded_image_paths = []
    for idx, image_data in enumerate(image_data_list):
        image_data = image_data.split(",")[1]
        decoded_image = base64.b64decode(image_data)
        image_path = os.path.join(images_dir, f"{station_name}_decoded_image_{idx + 1}.png")
        with open(image_path, "wb") as img_file:
            img_file.write(decoded_image)
        decoded_image_paths.append(image_path)
    return decoded_image_paths

# Function to extract data from an HTML file
def extract_forecast_data(html_file, station_name):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    days = [th.text.strip() for th in soup.select('tr.days th')]
    max_temps = [td.text.strip() for td in soup.select('tr.max-temps td')]
    min_temps = [td.text.strip() for td in soup.select('tr.min-temps td')]
    precipitation = [td.text.strip() for td in soup.select('tr.precipitation td')]
    symbol_data = [img['src'] for img in soup.select('tr.symbols img')]
    decoded_image_paths = decode_and_save_images(symbol_data, station_name)
    symbols = [f"\\includegraphics[width=0.35cm]{{{path}}}" for path in decoded_image_paths]
    return days, max_temps, symbols, min_temps, precipitation

# Function to add station data to LaTeX frames
def add_station_section(stations_chunk, title):
    """
    Generate LaTeX content for a section in the 'article' class.
    """
    # Start section with the title
    latex_section = f"\\section*{{{title}}}\n\\scriptsize\n"

    for station, html_file in stations_chunk.items():
        days, max_temps, symbols, min_temps, precipitation = extract_forecast_data(html_file, station)

        # Construct rows for the LaTeX table
        rows = [
            r" & ".join([r"\textbf{Day}"] + days) + r" \\ \hline",
            r" & ".join([r"\textbf{Max Temp (°C)}"] + max_temps) + r" \\ \hline",
            r" & ".join([r"\textbf{Symbol}"] + symbols) + r" \\ \hline",
            r" & ".join([r"\textbf{Min Temp (°C)}"] + min_temps) + r" \\ \hline",
            r" & ".join([r"\textbf{Rainfall (mm)}"] + precipitation) + r" \\ \hline",
        ]

        # Add station data without f-string for table structure
        latex_section += (
            r"\subsection*{" + station + r"}" + "\n"
            r"\renewcommand{\arraystretch}{0.8}" + "\n"
            r"\begin{tabular}{|l|" + "c|" * len(days) + r"}" + "\n"
            r"\hline" + "\n"
            + "\n".join(rows) + "\n"
            r"\end{tabular}" + "\n"
            r"\vspace{0.5cm} % Add space between stations" + "\n"
        )

    return latex_section



def generate_station_forecasts():
    # Define the LaTeX document preamble
    preamble = r"""
\documentclass{article}
\usepackage{graphicx}
\usepackage{array}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\geometry{margin=1cm}
\begin{document}
"""

    # Define the document ending
    postamble = r"\end{document}"

    # Split stations into chunks of 10 per page
    station_chunks = [dict(list(stations.items())[i:i + 10]) for i in range(0, len(stations), 10)]

    # Generate the LaTeX content for each chunk
    latex_content = ""
    for i, chunk in enumerate(station_chunks):
        # Generate title for the section using Python
        start_date = datetime.now().strftime("%a %d %b")
        end_date = (datetime.now() + timedelta(days=4)).strftime("%a %d %b %Y")
        title = f"5-DAY FORECAST FOR MAJOR CITIES: {start_date} – {end_date}"
        latex_content += add_station_section(chunk, title)

    # Combine everything into the final LaTeX document
    full_content = preamble + latex_content + postamble

    # Save the content to the LaTeX file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(full_content)

    print(f"LaTeX content saved to {output_path}")

# Main function to generate LaTeX content


def main():
    print("Starting Satellite image download...")
    # run_satellite_download()
    print("Generating station forecasts...")
    generate_station_forecasts()

if __name__ == '__main__':
    main()
