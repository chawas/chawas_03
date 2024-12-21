import os
import base64
from bs4 import BeautifulSoup
from datetime import datetime
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

output_path = os.path.join(target_dir, "station_forecast37.tex")

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
}

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
def add_station_frame(stations_chunk):
    latex_frame = r"""
    \begin{frame}{4-Station Weather Forecast}
    \scriptsize
    """
    minipage_count = 0
    for station, html_file in stations_chunk.items():
        days, max_temps, symbols, min_temps, precipitation = extract_forecast_data(html_file, station)
        rows = [
            " & ".join(["\\textbf{Day}"] + days) + " \\\\ \\hline",
            " & ".join(["\\textbf{Max Temp (°C)}"] + max_temps) + " \\\\ \\hline",
            " & ".join(["\\textbf{Symbol}"] + symbols) + " \\\\ \\hline",
            " & ".join(["\\textbf{Min Temp (°C)}"] + min_temps) + " \\\\ \\hline",
            " & ".join(["\\textbf{Rainfall (mm)}"] + precipitation) + " \\\\ \\hline",
        ]
        latex_frame += r"""
        \begin{minipage}[t]{0.48\textwidth}
        \textbf{""" + station + r"""} \\
        \renewcommand{\arraystretch}{0.8}
        \begin{tabular}{|l|""" + "c|" * len(days) + r"""}
        \hline
        """ + "\n".join(rows) + r"""
        \end{tabular}
        \end{minipage}
        """
        minipage_count += 1
        if minipage_count % 2 == 0 and minipage_count < len(stations_chunk):
            latex_frame += r"\vspace{0.3cm}"
        elif minipage_count % 2 == 1 and minipage_count < len(stations_chunk):
            latex_frame += r"\hfill"
    latex_frame += r"\end{frame}"
    return latex_frame

# Main function
def generate_station_forecasts():
    station_chunks = [dict(list(stations.items())[i:i + 4]) for i in range(0, len(stations), 4)]
    latex_content = ""
    for chunk in station_chunks:
        latex_content += add_station_frame(chunk)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(latex_content)
    print(f"LaTeX content saved to {output_path}")

def main():
    print("Starting Satellite image download...")
    run_satellite_download()
    print("Generating station forecasts...")
    generate_station_forecasts()

if __name__ == '__main__':
    main()
