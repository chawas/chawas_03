from datetime import datetime, timedelta

# Function to create a frame with 8 stations per page
def add_station_frames(stations_chunk):
    # Generate the date range dynamically
    start_date = datetime.now()
    end_date = start_date + timedelta(days=4)
    title = f"5-DAY FORECAST FOR HOLIDAY RESORTS: {start_date.strftime('%a %d')} – {end_date.strftime('%a %d %b %Y')}"

    # Initialize the LaTeX content for the frames
    latex_frames = f"""
    \\begin{{frame}}{{{title}}}
    \\scriptsize
    """

    for idx, (station, html_file) in enumerate(stations_chunk.items(), start=1):
        days, max_temps, symbols, min_temps, precipitation = extract_forecast_data(html_file, station)

        # Generate rows for the table
        rows = "\n".join([
            r" & ".join([r"\textbf{Day}"] + days) + r" \\ \hline",
            r" & ".join([r"\textbf{Max Temp (°C)}"] + max_temps) + r" \\ \hline",
            r" & ".join([r"\textbf{Symbol}"] + symbols) + r" \\ \hline",
            r" & ".join([r"\textbf{Min Temp (°C)}"] + min_temps) + r" \\ \hline",
            r" & ".join([r"\textbf{Rainfall (mm)}"] + precipitation) + r" \\ \hline",
        ])

        # Add each station's table
        latex_frames += f"""
        \\textbf{{{station}}} \\\\
        \\renewcommand{{\\arraystretch}}{{1.2}} % Adjust row height
        \\begin{{tabular}}{{|p{{2cm}}|{'p{1.8cm}|' * len(days)}}}
        \\hline
        {rows}
        \\end{{tabular}}
        \\vspace{{0.5cm}} % Add space between stations
        """

        # Add a new frame after every 8 stations
        if idx % 8 == 0 and idx != len(stations_chunk):
            latex_frames += f"\\end{{frame}}\\begin{{frame}}{{{title}}}"

    latex_frames += "\\end{frame}"
    return latex_frames

# Example Usage
def generate_forecast():
    # Sample data structure
    stations = {
        f"Station {i}": f"html_file_{i}" for i in range(1, 21)
    }

    # Divide stations into chunks of 8
    station_chunks = [dict(list(stations.items())[i:i + 8]) for i in range(0, len(stations), 8)]
    full_latex_content = ""

    for chunk in station_chunks:
        full_latex_content += add_station_frames(chunk)

    # Save LaTeX content to file
    with open("station_forecast51.tex", "w", encoding="utf-8") as file:
        file.write(full_latex_content)

# Mock `extract_forecast_data` function
def extract_forecast_data(html_file, station):
    # Example data for testing
    days = ["Fri", "Sat", "Sun", "Mon", "Tue"]
    max_temps = ["30", "31", "32", "33", "34"]
    symbols = ["☀", "☁", "☂", "☃", "☀"]
    min_temps = ["20", "21", "22", "23", "24"]
    precipitation = ["5", "10", "0", "2", "8"]
    return days, max_temps, symbols, min_temps, precipitation

# Main function to generate LaTeX content
if __name__ == "__main__":
    generate_forecast()
