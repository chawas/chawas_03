from datetime import datetime, timedelta
import os

# Function to generate LaTeX with dynamic dates
def generate_latex_with_dates(target_dir):
    # Generate current and next day dates
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    outlook = today + timedelta(days=2)

    # Format the dates as strings (e.g., "SATURDAY 19 OCTOBER 2024")
    today_date = today.strftime("%A %d %B %Y").upper()
    tomorrow_date = tomorrow.strftime("%A %d %B %Y").upper()
    outlook_date = outlook.strftime("%A %d %B %Y").upper()
    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Define the output file path
    output_path = os.path.join(target_dir, "forecast_with_dates17_4.tex")

    # Create LaTeX code with dynamic dates
    latex_code = (
        "\\documentclass{article}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\begin{document}\n"
        f"Today's date: {today_date}\n"
        f"Tomorrow's date: {tomorrow_date}\n"
        f"Outlook date: {outlook_date}\n"
        "\\end{document}\n"
    )

    # Return both the LaTeX code and the output file path
    return latex_code, output_path

# Define the target directory
target_dir = '/home/wrf/deployed/webb-downloading/wx_presentation/'

# Generate LaTeX content and the output path
latex_code, output_path = generate_latex_with_dates(target_dir)

# Write the LaTeX code to the file
with open(output_path, "w", encoding="utf-8") as file:
    file.write(latex_code)

print(f"File successfully written to: {output_path}")
