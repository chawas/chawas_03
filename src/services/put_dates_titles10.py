from datetime import datetime, timedelta
import os
# Function to generate LaTeX with dynamic dates
def generate_latex_with_dates():
    # Generate current and next day dates
    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    # Format the dates as strings (e.g., "SATURDAY 19 OCTOBER 2024")
    today_date = today.strftime("%A %d %B %Y").upper()
    tomorrow_date = tomorrow.strftime("%A %d %B %Y").upper()

    #Directory for tex file
    target_dir = '/home/wrf/deployed/webb-downloading/wx_presentation/'
    os.makedirs(target_dir, exist_ok=True)  # Ensure the directory exists
    output_path = os.path.join(target_dir, "forecast_with_dates17_2.tex")

    # Create LaTeX code with dynamic dates
    latex_code = (
        "\\documentclass{article}\n"
        "\\usepackage[utf8]{inputenc}  % Allows Unicode characters\n"
        "\\usepackage{newunicodechar}  % Allows defining new Unicode characters\n"
        "\\newunicodechar{☀}{\\sun}     % Replace ☀ with a macro or similar symbol\n"
        "\n"
        "\\usepackage{graphicx}\\graphicspath{{images/}}\n"
        "\\usepackage[a4paper,margin=1in]{geometry} % Adjust page layout\n"
        "\\usepackage{wrapfig} % For wrapping text around images\n"
        "\\setlength{\\parindent}{0pt} % Disable paragraph indentation\n"
        "\n"
        "\\usepackage[table,xcdraw]{xcolor} % For colored headers\n"
        "\\usepackage{multicol} % For multi-column layouts\n"
        "\\setlength{\\parindent}{0pt} % Disable paragraph indentation\n"
        "\\setlength{\\parskip}{1em} % Adjust paragraph spacing\n"
        "\n"
        "% Define header color\n"
        "\\definecolor{headerblue}{RGB}{0, 112, 192}\n"
        "\\geometry{left=0.3cm, right=0.2cm, top=0.0cm, bottom=0.3cm} % Reduce margins for a compact layout\n"
        "\n"
        "\\begin{document}\n"
        "\n"
        "% Start of layout\n"
        "\\noindent\n"
        "\\begin{minipage}[t]{0.4\\textwidth} % Left minipage taking 48% of the width\n"
        "    % Top part of the left minipage\n"
        "    \\includegraphics[width=1.5cm]{zim_coat_of_arms}\n"
        "    \\textbf{\\small GOVERNMENT OF ZIMBABWE} \\\\[0.1cm]\n"
        "    \\tiny{MINISTRY OF ENVIRONMENT, CLIMATE AND WILD LIFE}\n"
        "    \\hrule \n"
        "    \\vspace{0.2cm}\n"
        "    \\includegraphics[width=1.5cm]{MSD_logo}\n"
        "    \\centering\n"
        "    \\textbf{\\large Meteorological Services } \\\\\n"
        "    \\tiny P.O. Box BE150 BELVEDERE HARARE \\\\[0.3cm]\n"
        "    \\vspace{0.5cm} % Space between top and bottom sections\n"
        "\n"
        "    % Bottom part of the left minipage\n"
        "   \\textbf{\\Large{WEATHER \\\\ REPORT \& \\\\ [0.2cm]FORECAST}} \\\\[0.3cm]\n"
        "    \\begin{itemize}\n"
        "        \\item Cloud cover forecast.\n"
        "    \\end{itemize}\n"
        "\\end{minipage}\n"
        "\\hfill % Horizontal space between left and right minipages\n"
        "\\begin{minipage}[t]{0.6\\textwidth} % Right minipage taking 48% of the width\n"
        "    \\textbf{\\large SATELLITE-BASED GLANCE INTO THIS MORNING, " + today_date + "} \\\\[0.3cm]\n"
        "    \\begin{wrapfigure}{r}{0.45\\textwidth} % Wrapping the image to the right\n"
        "        \\includegraphics[width=4.0cm]{nce_today} % Replace 'satellite_image' with your image name\n"
        "    \\end{wrapfigure}\n"
        "    The country experienced no rainfall yesterday, attributed to suppressed middle-level atmospheric circulation. As a result, conditions remained predominantly cloudless and hot. Similar weather is expected today, with clear skies prevailing across most regions.\n"
        "    \\vspace{0.3cm}\n"
        "\n"
        "\\end{minipage}\n"
        "\n"
        "% First Header: WEATHER FORECAST: TOMORROW\n"
        "\\noindent\n"
        "\\textcolor{white}{\\colorbox{headerblue}{\\parbox{\\textwidth}{\\centering \\Large \\textbf{WEATHER FORECAST: " + tomorrow_date + "}}}}\n"
        "\n"
        "\\vspace{0.5cm}\n"
        "\n"
        "% Compartment 1: Forecast for Tomorrow\n"
        "\\noindent\n"
        "\\begin{minipage}[t]{0.48\\textwidth} % Image on the left\n"
        "    \\vspace{0pt} % Remove any vertical space before the image\n"
        "    \\includegraphics[height=5.5cm,keepaspectratio]{day1_forecast} % Set image height explicitly\n"
        "\\end{minipage}\n"
        "\\hfill\n"
        "\\begin{minipage}[t]{0.48\\textwidth} % Text on the right\n"
        "    \\vspace{0pt} % Ensure text starts at the very top\n"
        "    \\raggedright % Align text to the left\n"
        "    \\textbf{Morning:} Mild and cloudless conditions countrywide are expected. \\\\\n"
        "    \\textbf{Afternoon:} All areas should be sunny and very hot except for Matabeleland North were some partly cloudy periods are expected. \\\\\n"
        "    \\textbf{Evening:} Mostly clear skies and mild conditions. \\\\[5cm]\n"
        "    \\textbf{Impacts:}\n"
        "    \\begin{itemize}\n"
        "        \\item \\scriptsize{\\textbf{Secure loose items outdoors to prevent wind damage.}}\n"
        "        \\item \\textbf{Take precautions during thunderstorms, especially in open areas.}\n"
        "    \\end{itemize}\n"
        "\\end{minipage}\n"
        "\n"
        "\\vspace{1cm} % Space before the second header\n"
        "\n"
        "% Second Header: WEATHER FORECAST: OUTLOOK\n"
        "\\noindent\n"
        "\\textcolor{white}{\\colorbox{headerblue}{\\parbox{\\textwidth}{\\centering \\Large \\textbf{WEATHER FORECAST: OUTLOOK}}}}\n"
        "\n"
        "\\vspace{0.5cm}\n"
        "\n"
        "% Compartment 2: Forecast for the Outlook\n"
        "\\noindent\n"
        "\\begin{minipage}[t]{0.48\\textwidth} % Image on the left\n"
        "    \\vspace{0pt} % Remove any vertical space before the image\n"
        "    \\includegraphics[height=5.5cm,keepaspectratio]{day2_forecast} % Set image height explicitly\n"
        "\\end{minipage}\n"
        "\\hfill\n"
        "\\begin{minipage}[t]{0.48\\textwidth} % Text on the right\n"
        "    \\vspace{0pt} % Ensure text starts at the very top\n"
        "    \\raggedright % Align text to the left\n"
        "    \\textbf{Morning:} Anticipate brief cloudy periods and cool in Masvingo and Matabeleland South. \\textbf{Afternoon:} All areas are expected to remain cloudless, except for Masvingo and Matabeleland South, where partly cloudy conditions may develop. Daytime temperatures will be hot across the country. \\\\\n"
        "    \\textbf{Evening:} Mostly clear skies and mild conditions.\n"
        "\\end{minipage}\n"
        "\n"
        "\\end{document}\n"
    )

    return latex_code

# Save LaTeX content to file
with open(output_path, "w" , encoding="utf-8") as file:
    file.write(generate_latex_with_dates())
