from datetime import datetime, timedelta
import os


def generate_latex(today_forecast, tomorrow_forecast, notable_rainfall, cyclone_name=None):
    # Get today's and tomorrow's dates dynamically
    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    today_date = today.strftime("%A %d %B %Y")
    tomorrow_date = tomorrow.strftime("%A %d %B %Y")


    # Create output directory and file
    output_dir = '/home/wrf/deployed/chawas_03/wx_presentation/'
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

    today_date_filename = datetime.now().strftime("%Y-%m-%d")  # Format date for the filename
    output_path = os.path.join(output_dir, f"evening_weather_report_{today_date_filename}.tex")

    # Start building the LaTeX document
    latex_code = f"""
\\PassOptionsToPackage{{table,xcdraw}}{{xcolor}}
\\documentclass[a4paper]{{article}}
\\usepackage[left=1.5cm, right=1.5cm, top=1.5cm, bottom=2cm]{{geometry}}
\\usepackage{{xcolor}}
\\usepackage{{graphicx}}\\graphicspath{{{{images/}}}}
\\usepackage{{multicol}}
\\usepackage{{titlesec}}
\\usepackage{{tcolorbox}}
\\usepackage{{fontawesome5}}

% Custom title formatting
\\titleformat{{\\section}}
  {{\\normalfont\\sffamily\\bfseries\\color{{blue!80!black}}}}
  {{\\thesection}}{{1em}}{{}}

% Custom box for section headers
\\newtcolorbox{{sectionbox}}[1][]{{colback=blue!10!white,
  colframe=blue!80!black, fontupper=\\bfseries\\sffamily, 
  sharp corners, boxrule=0.8pt, #1}}

\\begin{{document}}

% Header with Logos and Title
\\noindent
\\begin{{minipage}}[t]{{0.15\\textwidth}}
    \\includegraphics[width=0.9\\textwidth]{{zim_coat_of_arms}} % Replace with your image path
\\end{{minipage}}
\\hfill
\\begin{{minipage}}[t]{{0.6\\textwidth}}
    \\centering
    \\textbf{{\\Large GOVERNMENT OF ZIMBABWE}} \\\\
    \\textbf{{\\large Ministry of Environment, Climate, and Wildlife}} \\\\
    \\textbf{{\\large METEOROLOGICAL SERVICES DEPARTMENT}} \\\\
    \\scriptsize \\textit{{10 King George Road, Avondale, Harare | Tel: (+263) 4 123456}}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}[t]{{0.15\\textwidth}}
    \\includegraphics[width=0.9\\textwidth]{{msd_logo.png}} % Replace with your image path
\\end{{minipage}}

\\vspace{{0.5cm}}
\\hrule
\\vspace{{0.5cm}}

% Satellite-Based Glance Section
\\begin{{sectionbox}}[title={{SATELLITE-BASED GLANCE INTO TODAY, {today_date}}}]
\\noindent
\\begin{{multicols}}{{2}} % Two-column layout

Remnant moisture from \\textbf{{{cyclone_name or "Tropical Cyclone"}}} and a cloud band moving eastwards from Botswana resulted in widespread thunderstorms across the country.

\\textbf{{Notable rainfall amounts}} were recorded in:
\\begin{{itemize}}
"""
    # Add notable rainfall amounts dynamically
    for location, amount in notable_rainfall.items():
        latex_code += f"    \\item \\textbf{{{location} ({amount} mm)}}\n"

    latex_code += f"""
\\end{{itemize}}

Cloudy and mild conditions were experienced nationwide in the morning, with rain and thunderstorms reported in some areas. By the afternoon, cloudy and warm conditions continued, accompanied by isolated thunderstorms.

\\columnbreak

\\centering
\\includegraphics[width=0.95\\linewidth]{{water_vapour_today}} % Replace with actual image path
\\end{{multicols}}
\\end{{sectionbox}}

\\vspace{{-0.05cm}}

% Weather Outlook Section
\\begin{{sectionbox}}[title=WEATHER OUTLOOK FOR : {tomorrow_date}]

% Forecast for Tomorrow
\\noindent
\\begin{{minipage}}[t]{{0.48\\textwidth}}
    \\includegraphics[height=6.0cm,keepaspectratio]{{day1_forecast}}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}[t]{{0.48\\textwidth}}
    \\vspace{{-6cm}}
    \\raggedright
    {tomorrow_forecast}
\\end{{minipage}}
\\end{{sectionbox}}


\\noindent
\\begin{{minipage}}[t]{{0.48\\textwidth}}
    \\includegraphics[height=6.0cm,keepaspectratio]{{day1_forecast}}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}[t]{{0.48\\textwidth}}
    \\vspace{{-6cm}}
    \\raggedright
    {tomorrow_forecast}
\\end{{minipage}}
\\end{{sectionbox}}

\\end{{document}}
"""

    return latex_code


# Example usage:
if __name__ == "__main__":
    notable_rainfall = {
        "Nyanyadzi": 58,
        "Kutsaga": 45,
        "West Nicholson": 44,
        "Kadoma": 43,
        "Guruve": 33,
        "Chimanimani": 32,
        "Harare Airport": 31,
    }

    today_forecast = """
    Cloudy and mild conditions were experienced nationwide in the morning, with rain and thunderstorms reported in some areas. By the afternoon, cloudy and warm conditions continued, accompanied by isolated thunderstorms.
    """

    tomorrow_forecast = """
    \\textbf{Morning:} Mild and cloudless conditions countrywide are expected. \\\\
    \\textbf{Afternoon:} All areas should be sunny and very hot except for Matabeleland North where some partly cloudy periods are expected.
    """

    latex_code = generate_latex(today_forecast, tomorrow_forecast, notable_rainfall,
                                cyclone_name="Tropical Cyclone Chido")

    # Save to a file
    with open(output_path, "w") as file:
        file.write(latex_code)

    print("LaTeX document has been generated as 'weather_report_{today_date}.tex'")
