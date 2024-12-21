from bs4 import BeautifulSoup
import os
import base64

# Directory for symbols and HTML files
symbols_dir = "/home/wrf/nons/python-plotting-toolbox/local_outdata/symbograms/"
target_dir = '/home/wrf/deployed/webb-downloading/wx_presentation/'
images_dir = '/home/wrf/deployed/webb-downloading/wx_presentation/images/'
os.makedirs(target_dir, exist_ok=True)  # Ensure the target directory exists
os.makedirs(images_dir, exist_ok=True)  # Ensure the images directory exists

output_path = os.path.join(target_dir, "station_forecasts.tex")

# Dictionary of stations and their corresponding HTML filenames
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
        # Decode the base64 image
        image_data = image_data.split(",")[1]  # Assumes format: "data:image/png;base64,..."
        decoded_image = base64.b64decode(image_data)
        image_path = os.path.join(images_dir, f"{station_name}_decoded_image_{idx + 1}.png")

        # Save the image
        with open(image_path, "wb") as img_file:
            img_file.write(decoded_image)

        decoded_image_paths.append(image_path)
    return decoded_image_paths


# Function to extract data from an HTML file
def extract_forecast_data(html_file, station_name):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Extract data
    days = [th.text.strip() for th in soup.select('tr.days th')]
    max_temps = [td.text.strip() for td in soup.select('tr.max-temps td')]
    min_temps = [td.text.strip() for td in soup.select('tr.min-temps td')]
    precipitation = [td.text.strip() for td in soup.select('tr.precipitation td')]

    # Extract and decode symbols
    symbol_data = [img['src'] for img in soup.select('tr.symbols img')]
    decoded_image_paths = decode_and_save_images(symbol_data, station_name)

    # Prepare LaTeX includegraphics commands for the saved images
    symbols = [f"\\includegraphics[width=0.35cm]{{{path}}}" for path in decoded_image_paths]

    return days, max_temps, symbols, min_temps, precipitation


# Function to add station data to LaTeX frame
def add_station_frame(stations_chunk):
    latex_frame = r"""
    \begin{frame}{4-Station Weather Forecast}
    \scriptsize % Use a smaller font size for compact tables
    """

    # Loop through stations and arrange them in two rows with two minipages per row
    minipage_count = 0
    for station, html_file in stations_chunk.items():
        # Extract data from HTML
        days, max_temps, symbols, min_temps, precipitation = extract_forecast_data(html_file, station)

        # Generate LaTeX table rows
        rows = [
            " & ".join(["\\textbf{Day}"] + days) + " \\\\ \\hline",
            " & ".join(["\\textbf{Max Temp (°C)}"] + max_temps) + " \\\\ \\hline",
            " & ".join(["\\textbf{Symbol}"] + symbols) + " \\\\ \\hline",
            " & ".join(["\\textbf{Min Temp (°C)}"] + min_temps) + " \\\\ \\hline",
            " & ".join(["\\textbf{Rainfall (mm)}"] + precipitation) + " \\\\ \\hline",
        ]

        # Add the table to the minipage
        latex_frame += r"""
        \begin{minipage}[t]{0.48\textwidth} % Adjust width for compact layout
        \textbf{""" + station + r"""} \\ % Station name
        \renewcommand{\arraystretch}{0.8} % Adjust row height to reduce spacing between rows
        \begin{tabular}{|l|""" + "c|" * len(days) + r"""}
        \hline
        """ + "\n".join(rows) + r"""
        \end{tabular}
        \end{minipage}
        """

        minipage_count += 1

        # Add horizontal spacing or move to a new row
        if minipage_count % 2 == 0 and minipage_count < len(stations_chunk):
            latex_frame += r"""
        \vspace{0.3cm} % End row and add vertical space
        """
        elif minipage_count % 2 == 1 and minipage_count < len(stations_chunk):
            latex_frame += r"""
        \hfill % Add horizontal spacing between minipages
        """

    latex_frame += r"""
    \end{frame}
    """

    return latex_frame


# Split stations into chunks (4 stations per frame)
station_chunks = [dict(list(stations.items())[i:i + 4]) for i in range(0, len(stations), 4)]

# Add the frames for each chunk
latex_content = ""
for chunk in station_chunks:
    latex_content += add_station_frame(chunk)

# Save the LaTeX content to a file
with open(output_path, 'w', encoding='utf-8') as file:
    file.write(latex_content)

print(f"LaTeX content saved to {output_path}")
