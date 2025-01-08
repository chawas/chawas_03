import os
import base64
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Define directories
symbols_dir = "/home/wrf/nons/python-plotting-toolbox/local_outdata/symbograms/"
target_dir = '/home/wrf/deployed/webb-downloading/wx_presentation/'
images_dir = '/home/wrf/deployed/webb-downloading/wx_presentation/images/'
os.makedirs(target_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)

output_path = os.path.join(target_dir, "station_forecast44.tex")

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
    latex_section = ""  # Empty to avoid unnecessary headers

    for station, html_file in stations_chunk.items():
        days, max_temps, symbols, min_temps, precipitation = extract_forecast_data(html_file, station)

        # Prepare table rows without headers
        rows = [
            " & ".join(days) + " \\ \\hline",  # No raw string, just normal string concatenation
            " & ".join(max_temps) + " \\ \\hline",
            " & ".join(symbols) + " \\ \\hline",
            " & ".join(min_temps) + " \\ \\hline",
            " & ".join(precipitation) + " \\ \\hline"
        ]

        # Add station data wrapped inside a frame environment
        latex_section += f"""
        \\begin{{frame}}{{{station}}}
        \\renewcommand{{\\arraystretch}}{{1.2}} % Adjust row height
        \\begin{{tabular}}{{|p{{1.5cm}}|{'p{{2cm}}|' * len(days)}}}
        \\hline
        {"\\n".join(rows)}
        \\end{{tabular}}
        \\vspace{{0.7cm}} % Add space between stations
        \\end{{frame}}
        """

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
