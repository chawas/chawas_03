import os
import base64
from bs4 import BeautifulSoup

# Define directories
symbols_dir = "/home/wrf/nons/python-plotting-toolbox/local_outdata/symbograms/"
target_dir = '/home/wrf/deployed/chawas_03/wx_presentation/'
images_dir = '/home/wrf/deployed/chawas_03/wx_presentation/images/'
os.makedirs(target_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)

output_path = os.path.join(target_dir, "station_forecast61.tex")

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
    "VUMBA": os.path.join(symbols_dir, "Vumba.html")
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
    \begin{frame}{WEATHER OUTLOOK : SATURDAY 07 DECEMBER 2024}
    \scriptsize
    """

    station_count = 0  # To keep track of the number of stations per frame
    for station, html_file in stations_chunk.items():
        days, max_temps, symbols, min_temps, precipitation = extract_forecast_data(html_file, station)

        rows = [
            " & ".join(["\\textbf{Day}"] + days) + " \\\\ \\hline",
            " & ".join(["\\textbf{Max Temp (°C)}"] + max_temps) + " \\\\ \\hline",
            " & ".join(["\\textbf{Symbol}"] + symbols) + " \\\\ \\hline",
            " & ".join(["\\textbf{Min Temp (°C)}"] + min_temps) + " \\\\ \\hline",
            " & ".join(["\\textbf{Rainfall (mm)}"] + precipitation) + " \\\\ \\hline",
        ]

        # Add station data below one another with increased table size
        latex_frame += r"""
        \textbf{""" + station + r"""} \\
        \renewcommand{\arraystretch}{1.2} % Increased row height for bigger table
        \begin{tabular}{|l|""" + "c|" * len(days) + r"""}
        \hline
        """ + "\n".join(rows) + r"""
        \end{tabular}
        \vspace{0.7cm} % Add space between stations
        """

        # Increment station count, and add a new frame after 8 stations
        station_count += 1
        if station_count == 8:
            latex_frame += r"\end{frame}"
            latex_frame += r"""
            \begin{frame}{WEATHER OUTLOOK : SATURDAY 07 DECEMBER 2024}
            \scriptsize
            """
            station_count = 0  # Reset the station count for the next frame

    latex_frame += r"\end{frame}"
    return latex_frame

# Main function to generate LaTeX content
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
  #  run_satellite_download()
    print("Generating station forecasts...")
    generate_station_forecasts()


if __name__ == '__main__':
    main()
