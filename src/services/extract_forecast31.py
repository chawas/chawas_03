from bs4 import BeautifulSoup
import os

# Directory for symbols and HTML files
symbols_dir = "/home/wrf/nons/python-plotting-toolbox/local_outdata/symbograms/"
target_dir = '/home/wrf/deployed/webb-downloading/wx_presentation/'
os.makedirs(target_dir, exist_ok=True)  # Ensure the directory exists
output_path = os.path.join(target_dir, "station_forecasts31.tex")

# Dictionary of stations and their corresponding HTML filenames
stations = {
    "Beitbridge": os.path.join(symbols_dir, "BeitBridge.html"),
    "Bulawayo": os.path.join(symbols_dir, "Bulawayo.html"),
    "Binga": os.path.join(symbols_dir, "Binga.html"),
    "Chinhoyi": os.path.join(symbols_dir, "Chinhoyi.html"),

    "Gwanda": os.path.join(symbols_dir, "Gwanda.html"),
    "Gweru": os.path.join(symbols_dir, "Gweru.html"),
    "Harare": os.path.join(symbols_dir, "Harare.html"),
    "Kadoma": os.path.join(symbols_dir, "Kadoma.html")
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
        f"\\includegraphics[width=0.35cm]{{decoded_image_{i+1}.png}}"  # Keep image size reasonable
        for i in range(len(days))
    ]

    return days, max_temps, symbols, min_temps, precipitation

# Initialize LaTeX content
latex_content = r"""
\documentclass{beamer}
\usepackage{graphicx}
\graphicspath{{images/}} % Path to graphics folder
\usepackage[table,xcdraw]{xcolor} % For colored tables
\usepackage{array} % For table column alignment
\usepackage{hyperref} % For clickable links
\usepackage{multicol} % For multi-column layouts
\usepackage{colortbl} % For colored rows in tables
\usepackage{textpos} % For absolute positioning

\geometry{left=0.2cm, right=0.2cm, top=0.3cm, bottom=0.3cm} % Reduce margins for a compact layout

\begin{document}
"""

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
        days, max_temps, symbols, min_temps, precipitation = extract_forecast_data(html_file)

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

# Split stations into two chunks (4 stations per frame)
stations_chunk_1 = {k: stations[k] for k in list(stations)[:4]}
stations_chunk_2 = {k: stations[k] for k in list(stations)[4:]}

# Add the frames for both chunks
latex_content += add_station_frame(stations_chunk_1)
latex_content += add_station_frame(stations_chunk_2)

# Close the LaTeX document
latex_content += r"""
\end{document}
"""

# Save the LaTeX content to a file
with open(output_path, 'w', encoding='utf-8') as file:
    file.write(latex_content)

print(f"LaTeX content saved to {output_path}")
