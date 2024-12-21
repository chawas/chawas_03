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
    output_path = os.path.join(target_dir, "dynamic_weather_forecast.tex")

    # LaTeX template with date variables integrated
    latex_code = f"""
\\documentclass{{article}}

\\usepackage[utf8]{{inputenc}}  % Allows Unicode characters
\\usepackage{{newunicodechar}}  % Allows defining new Unicode characters
\\newunicodechar{{☀}}{{\\sun}}     % Replace ☀ with a macro or similar symbol

\\usepackage{{graphicx}}\\graphicspath{{{{images/}}}}
\\usepackage[a4paper,margin=1in]{{geometry}} % Adjust page layout
\\usepackage{{wrapfig}} % For wrapping text around images
\\setlength{{\\parindent}}{{0pt}} % Disable paragraph indentation

\\usepackage[table,xcdraw]{{xcolor}} % For colored headers
\\usepackage{{multicol}} % For multi-column layouts
\\setlength{{\\parskip}}{{1em}} % Adjust paragraph spacing

% Define header color
\\definecolor{{headerblue}}{{RGB}}{{0, 112, 192}}
\\geometry{{left=0.3cm, right=0.2cm, top=0.0cm, bottom=0.3cm}} % Reduce margins for a compact layout

\\begin{{document}}

% Header Section with Images
\\noindent
\\begin{{minipage}}[t]{{0.4\\textwidth}}
    \\includegraphics[width=1.5cm]{{zim_coat_of_arms}}
    \\textbf{{\\small GOVERNMENT OF ZIMBABWE}} \\\\[0.1cm]
    \\tiny{{MINISTRY OF ENVIRONMENT, CLIMATE AND WILD LIFE}}
    \\hrule 
    \\vspace{{0.2cm}}
    \\includegraphics[width=1.5cm]{{MSD_logo}}
    \\centering
    \\textbf{{\\large Meteorological Services }} \\\\[0.3cm]
    \\textbf{{\\Large{{WEATHER \\\\ REPORT \& \\\\[0.2cm]FORECAST}}}} \\\\[0.3cm]
\\end{{minipage}}
\\hfill
\\begin{{minipage}}[t]{{0.6\\textwidth}}
    \\textbf{{\\large SATELLITE-BASED GLANCE INTO THIS MORNING, {today_date}}} \\\\[0.3cm]
    \\begin{{wrapfigure}}{{r}}{{0.45\\textwidth}}
        \\includegraphics[width=4.0cm]{{nce_today}}
    \\end{{wrapfigure}}
    The country experienced no rainfall yesterday, attributed to suppressed middle-level atmospheric circulation. 
    Conditions remained predominantly cloudless and hot. Similar weather is expected today, with clear skies prevailing across most regions.
\\end{{minipage}}

% WEATHER FORECAST: TOMORROW
\\noindent
\\textcolor{{white}}{{\\colorbox{{headerblue}}{{\\parbox{{\\textwidth}}{{\\centering \\Large \\textbf{{WEATHER FORECAST: {tomorrow_date}}}}}}}}}

% Forecast for Tomorrow
\\noindent
\\begin{{minipage}}[t]{{0.48\\textwidth}}
    \\includegraphics[height=5.5cm,keepaspectratio]{{day1_forecast}}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}[t]{{0.48\\textwidth}}
    \\textbf{{Morning:}} Mild and cloudless conditions countrywide are expected. \\\\
    \\textbf{{Afternoon:}} All areas should be sunny and very hot except for Matabeleland North were some partly cloudy periods are expected. \\\\
    \\textbf{{Evening:}} Mostly clear skies and mild conditions. \\\\[5cm]
\\end{{minipage}}

% WEATHER FORECAST: OUTLOOK
\\noindent
\\textcolor{{white}}{{\\colorbox{{headerblue}}{{\\parbox{{\\textwidth}}{{\\centering \\Large \\textbf{{WEATHER FORECAST: {outlook_date}}}}}}}}}

% Forecast for Outlook
\\noindent
\\begin{{minipage}}[t]{{0.48\\textwidth}}
    \\includegraphics[height=5.5cm,keepaspectratio]{{day2_forecast}}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}[t]{{0.48\\textwidth}}
    \\textbf{{Morning:}} Anticipate brief cloudy periods and cool in Masvingo and Matabeleland South. \\\\
    \\textbf{{Afternoon:}} All areas are expected to remain cloudless, except for Masvingo and Matabeleland South, where partly cloudy conditions may develop. \\\\
    \\textbf{{Evening:}} Mostly clear skies and mild conditions. \\\\
\\end{{minipage}}

\\newpage
\\input{{station_forecast60.tex}}

\\end{{document}}
    """

    # Write LaTeX code to the output file
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(latex_code)

    print(f"LaTeX file successfully written to: {output_path}")

# Define the target directory
target_dir = '/home/wrf/deployed/webb-downloading/wx_presentation/'

# Generate LaTeX content and write to the file
generate_latex_with_dates(target_dir)
