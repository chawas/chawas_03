from bs4 import BeautifulSoup
import os
import itertools

# Directory for symbols and HTML files
symbols_dir = "/home/wrf/nons/python-plotting-toolbox/local_outdata/symbograms/"
target_dir = '/home/wrf/deployed/webb-downloading/wx_presentation/'
os.makedirs(target_dir, exist_ok=True)  # Ensure the directory exists
output_path = os.path.join(target_dir, "station_forecasts_debugged.tex")

# Dictionary of stations and their corresponding HTML filenames
stations = {
    "Beitbridge": os.path.join(symbols_dir, "BeitBridge.html"),
    "Bulawayo": os.path.join(symbols_dir, "Bulawayo.html"),
    "Binga": os.path.join(symbols_dir, "Binga.html"),
    "Chinhoyi": os.path.join(symbols_dir, "Chinhoyi.html"),
    "Gwanda": os.path.join(symbols_dir, "Gwanda.html"),
    "Gweru": os.path.join(symbols_dir, "Gweru.html"),
    "Harare": os.path.join(symbols_dir, "Harare.html"),
    "Kadoma": os.path.join(symbols_dir, "Kadoma.html"),
}

# Function to extract data from an HTML file
def extract_forecast_data(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Extract data
    days = [th.text.strip() for th in soup.select('tr.days th')]
    max_temps = [td.text.strip() for td in soup.select('tr.max-temps td')]
    min_temps = [td.text.strip() for td in soup.select('tr.min-temps td')]
    precipitation = [td.text.strip() for td in soup.select('tr.precipitation td')]

    # Prepare weather symbols (decoded images)
    symbols = [
        f"\\includegraphics[width=0.35cm]{{decoded_image_{i+1}.png}}"
        for i in range(len(days))
    ]

    return days, max_temps, symbols, min_temps, precipitation

# Function to generate LaTeX for a frame
def generate_frame_content(stations_chunk):
    frame_content = r"\begin{frame}{4-Station Weather Forecast}\n\scriptsize"
    minipage_count = 0

    for station, html_file in stations_chunk:
        days, max_temps, symbols, min_temps, precipitation = extract_forecast_data(html_file)

        # Escape special characters in station names
        station_name = station.replace("&", r"\&").replace("_", r"\_")

        # Generate LaTeX table rows
        rows = [
            " & ".join(["\\textbf{Day}"] + days) + " \\\\ \\hline",
            " & ".join(["\\textbf{Max Temp (°C)}"] + max_temps) + " \\\\ \\hline",
            " & ".join(["\\textbf{Symbol}"] + symbols) + " \\\\ \\hline",
            " & ".join(["\\textbf{Min Temp (°C)}"] + min_temps) + " \\\\ \\hline",
            " & ".join(["\\textbf{Rainfall (mm)}"] + precipitation) + " \\\\ \\hline",
        ]

        # Add the table to the minipage
        frame_content += r"""
        \begin{minipage}[t]{0.48\textwidth}
        \textbf{""" + station_name + r"""} \\ % Station name
        \renewcommand{\arraystretch}{0.8} % Adjust row height to reduce spacing between rows
        \begin{tabular}{|l|""" + "c|" * len(days) + r"""}
\hline
""" + "\n".join(rows) + r"""
        \end{tabular}
        \end{minipage}
        """

        minipage_count += 1

        # Add horizontal spacing or move to a new row
        if minipage_count % 2 == 0:
            frame_content += r"""
        \vspace{0.3cm}
        """
        else:
            frame_content += r"""
        \hfill
        """

    frame_content += r"\end{frame}"
    return frame_content

# Split stations into chunks of 4
station_chunks = [list(chunk) for chunk in itertools.zip_longest(*[iter(stations.items())] * 4, fillvalue=None)]
latex_content = ""

# Generate frames for each chunk of stations
for chunk in station_chunks:
    # Remove None values caused by zip_longest
    filtered_chunk = [(k, v) for k, v in chunk if k is not None]
    latex_content += generate_frame_content(filtered_chunk)

# Save the LaTeX content to a file
with open(output_path, 'w', encoding='utf-8') as file:
    file.write(latex_content)

print(f"LaTeX input content saved to {output_path}")
