import datetime
import os


#variables
# Target directory and filename
target_dir = '/home/wrf/deployed/webb-downloading/wx_presentation/'
os.makedirs(target_dir, exist_ok=True)  # Ensure the directory exists
output_path = os.path.join(target_dir, "weather_forecast_with_dates12.tex")

# Get yesterday's and tomorrow's date
yesterday = datetime.date.today() - datetime.timedelta(days=1)
today = datetime.date.today()
tomorrow = datetime.date.today() + datetime.timedelta(days=1)

# Format the dates as strings
yesterday_str = yesterday.strftime('%B %d, %Y')
today_str = today.strftime('%B %d, %Y')
tomorrow_str = tomorrow.strftime('%B %d, %Y')
# Format the dates with specific times
yesterday_infrared_str = yesterday.strftime('%B %d, %Y') + " 06:00Z"
yesterday_water_vapour_str = yesterday.strftime('%B %d, %Y') + " 00:00Z"
today_infrared_str = today.strftime('%B %d, %Y') + " 06:00Z"
today_water_vapour_str = today.strftime('%B %d, %Y') + " 00:00Z"
tomorrow_infrared_str = tomorrow.strftime('%B %d, %Y') + " 06:00Z"
tomorrow_water_vapour_str = tomorrow.strftime('%B %d, %Y') + " 00:00Z"
# Prepare the LaTeX content
latex_content = f"""
\\PassOptionsToPackage{{table,xcdraw}}{{xcolor}} % Add required xcolor options before the class

\\documentclass{{beamer}}
\\usepackage{{graphicx}}\\graphicspath{{{{images/}}}} % Path to graphics folder
\\usepackage[table,xcdraw]{{xcolor}} % For colored tables
\\usepackage{{array}} % For table column alignment
\\usepackage{{hyperref}} % For clickable links
\\usepackage{{multicol}} % For multi-column layouts
\\usepackage{{colortbl}} % For colored rows in tables
\\usepackage{{textpos}} % For absolute positioning
\\usetheme{{default}}

% Customize theme
\\setbeamercolor{{frametitle}}{{bg=blue!10, fg=black}} % Light blue title bar
\\setbeamerfont{{frametitle}}{{size=\\large, series=\\bfseries}} % Font for the title bar

% Title and metadata
\\title[Weather Forecast]{{Weather Forecast Presentation}}
\\author{{Meteorological Services Department}}
\\date{{\\today}}

% Adjust margins and spacing
\\geometry{{left=0.2cm, right=0.2cm, top=-0.2cm, bottom=0.3cm}} % Reduce margins for a compact layout

\\begin{{document}}

% Title Slide
\\begin{{frame}}
    \\titlepage
    \\begin{{center}}
        \\includegraphics[width=0.15\\textwidth]{{zim_coat_of_arms}} \\hspace{{0.5cm}}
        \\includegraphics[width=0.2\\textwidth]{{MSD_Logo}} \\hspace{{0.5cm}}
        \\includegraphics[width=0.15\\textwidth]{{zim_civil_protection}}
    \\end{{center}}
\\end{{frame}}

% Satellite Image Slide - Four images in two rows
\\begin{{frame}}\centering{{IR}}{' '}{yesterday_infrared_str}{' '}{{Water Vapour}}{'  '}{yesterday_water_vapour_str}% Title

    \\begin{{columns}}[T] % Align columns at the top
        % First row with Yesterday images
        \\begin{{column}}{{0.48\\textwidth}}
        	\\vspace{{-0.5cm}} % Move image up closer to the title
            \\begin{{center}}
                \\includegraphics[width=\\linewidth]{{infra_radiation_yesterday}} % Replace with your image
                \\vspace{{-1cm}} % Move image up closer to the title
                \\textbf{{Infrared Radiation}} (Data from: {yesterday_str}) % Title
            \\end{{center}}
        \\end{{column}}

        \\begin{{column}}{{0.48\\textwidth}}
	        \\vspace{{-0.5cm}} % Move image up closer to the title
            \\begin{{center}}
                \\includegraphics[width=\\linewidth]{{water_vapour_yesterday}} % Replace with your image
                \\vspace{{-1cm}} % Move image up closer to the title
                \\textbf{{Water Vapour}} (Data from: {yesterday_str}) % Title
            \\end{{center}}
        \\end{{column}}
    \\end{{columns}}

    \\vspace{{0.6cm}} % Add less vertical space between rows to close the gap

    \\begin{{columns}}[T] % Second row with Tomorrow images
        % Second row with Tomorrow images
        \\begin{{column}}{{0.48\\textwidth}}
            \\begin{{center}}
                \\textbf{{Infrared Radiation}} (Data for: {today_str}) % Title
                \\includegraphics[width=\\linewidth]{{infra_radiation_today}} % Replace with your image
                \\vspace{{-0.5cm}} % Reduce space between image and title
                
            \\end{{center}}
        \\end{{column}}

        \\begin{{column}}{{0.48\\textwidth}}
            \\begin{{center}}
                \\includegraphics[width=\\linewidth]{{water_vapour_today}} % Replace with your image
                \\vspace{{-0.5cm}} % Reduce space between image and title
                \\textbf{{Water Vapour}} (Data for: {tomorrow_str}) % Title
            \\end{{center}}
        \\end{{column}}
    \\end{{columns}}

\\end{{frame}}

\\end{{document}}
"""

# Save LaTeX content to a file

with open(output_path, "w", encoding="utf-8") as file:
    file.write(latex_content)

print(f"LaTeX document saved to {output_path}")
