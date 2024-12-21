from datetime import datetime, timedelta

# Function to create a frame with 8 stations per page
def add_station_frames(stations_chunk):
    # Generate the date range dynamically
    start_date = datetime.now()
    end_date = start_date + timedelta(days=4)
    title = f"5-DAY FORECAST FOR HOLIDAY RESORTS: {start_date.strftime('%a %d')} – {end_date.strftime('%a %d %b %Y')}"

    # Initialize the LaTeX content for the frames
    latex_frames = rf"""
    \begin{{frame}}{{{title}}}
    \scriptsize
    """

    for idx, (station, html_file) in enumerate(stations_chunk.items(), start=1):
        days, max_temps, symbols, min_temps, precipitation = extract_forecast_data(html_file, station)

        # Generate rows for the table
        rows = [
            r" & ".join([r"\textbf{Day}"] + days) + r" \\ \hline",
            r" & ".join([r"\textbf{Max Temp (°C)}"] + max_temps) + r" \\ \hline",
            r" & ".join([r"\textbf{Symbol}"] + symbols) + r" \\ \hline",
            r" & ".join([r"\textbf{Min Temp (°C)}"] + min_temps) + r" \\ \hline",
            r" & ".join([r"\textbf{Rainfall (mm)}"] + precipitation) + r" \\ \hline",
        ]

        # Add each station's table
        latex_frames += rf"""
        \textbf{{{station}}} \\
        \renewcommand{{\arraystretch}}{{1.2}} % Adjust row height
        \begin{{tabular}}{{|p{{2cm}}|{'p{1.8cm}|' * len(days)}}}
        \hline
        {"\n".join(rows)}
        \end{{tabular}}
        \vspace{{0.5cm}} % Add space between stations
        """

        # Add a new frame after every 8 stations
        if idx % 8 == 0 and idx != len(stations_chunk):
            latex_frames += rf"\end{{frame}}\begin{{frame}}{{{title}}}"

    latex_frames += r"\end{frame}"
    return latex_frames

# Example Usage
def generate_forecast():
    station_chunks = [dict(list(stations.items())[i:i + 8]) for i in range(0, len(stations), 8)]
    full_latex_content = ""

    for chunk in station_chunks:
        full_latex_content += add_station_frames(chunk)

    # Save LaTeX content to file
    with open("station_forecast.tex", "w", encoding="utf-8") as file:
        file.write(full_latex_content)

# Main function to generate LaTeX content
if __name__ == "__main__":
    generate_forecast()
