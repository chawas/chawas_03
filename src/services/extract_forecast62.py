from datetime import datetime, timedelta

# Initialize date variables for the forecast range
base_date = datetime.now()
start_date = base_date
end_date = base_date + timedelta(days=4)  # 5-day range (inclusive)


# Function to generate the title based on the date range
def generate_forecast_title(start_date):
    start_date_str = start_date.strftime("%a %d")
    end_date_str = (start_date + timedelta(days=4)).strftime("%a %d %b")
    return f"5-DAY FORECAST FOR MAJOR CITIES: {start_date_str} – {end_date_str}"


# Initial forecast title
forecast_title = generate_forecast_title(start_date)

# Example loop with station count
station_count = 0
latex_frame = ""

for station in stations:  # Replace 'stations' with your list of stations
    # Add station to the LaTeX frame (example)
    latex_frame += f"{station}\n"

    # Increment station count
    station_count += 1

    # Check if a new frame is needed after 8 stations
    if station_count == 8:
        latex_frame += r"\end{frame}"

        # Update the start date and forecast title after every 12 stations
        if station_count % 12 == 0:
            start_date += timedelta(days=5)  # Move the range by 5 days
            forecast_title = generate_forecast_title(start_date)

        # Add a new frame with the updated title
        latex_frame += rf"""
        \begin{{frame}}{{{forecast_title}}}
        \scriptsize
        """
        station_count = 0  # Reset the station count for the next frame

# Ensure the last frame is properly closed
if station_count > 0:
    latex_frame += r"\end{frame}"

print(latex_frame)  # Output the final LaTeX content
