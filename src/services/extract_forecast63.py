from datetime import datetime, timedelta
import os

# Define directories
symbols_dir = "/home/wrf/nons/python-plotting-toolbox/local_outdata/symbograms/"
target_dir = '/home/wrf/deployed/chawas_03/wx_presentation/'
images_dir = '/home/wrf/deployed/chawas_03/wx_presentation/images/'
os.makedirs(target_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)

output_path = os.path.join(target_dir, "station_forecast61.tex")


# Define stationsx
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




# Function to generate the dynamic frame title
def generate_forecast_title(start_date):
    start_date_str = start_date.strftime("%a %d")
    end_date_str = (start_date + timedelta(days=4)).strftime("%a %d %b")
    return f"5-DAY FORECAST FOR MAJOR CITIES: {start_date_str} – {end_date_str}"


# Function to add station data to LaTeX frames with dynamic titles
def add_station_frame(stations_chunk, current_start_date):
    latex_frame = rf"""
    \begin{{frame}}{{{generate_forecast_title(current_start_date)}}}
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

        # Increment station count, and start a new frame after 8 stations
        station_count += 1
        if station_count == 8:
            latex_frame += r"\end{frame}"
            current_start_date += timedelta(days=5)  # Increment the start date for the next title
            latex_frame += rf"""
            \begin{{frame}}{{{generate_forecast_title(current_start_date)}}}
            \scriptsize
            """
            station_count = 0  # Reset the station count for the next frame

    latex_frame += r"\end{frame}"
    return latex_frame, current_start_date


# Main function to generate LaTeX content
def generate_station_forecasts():
    station_chunks = [dict(list(stations.items())[i:i + 4]) for i in range(0, len(stations), 4)]
    latex_content = ""
    current_start_date = datetime.now()  # Initialize the start date

    for chunk in station_chunks:
        frame_content, current_start_date = add_station_frame(chunk, current_start_date)
        latex_content += frame_content

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(latex_content)
    print(f"LaTeX content saved to {output_path}")

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



def main():
    print("Starting Satellite image download...")
    # run_satellite_download()
    print("Generating station forecasts...")
    generate_station_forecasts()


if __name__ == '__main__':
    main()
