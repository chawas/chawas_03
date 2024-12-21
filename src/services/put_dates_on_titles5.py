from datetime import datetime, timedelta

# Function to generate LaTeX with dynamic dates
def generate_latex_with_dates():
    # Generate current and next day dates
    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    # Format the dates as strings (e.g., "SATURDAY 19 OCTOBER 2024")
    today_date = today.strftime("%A %d %B %Y").upper()
    tomorrow_date = tomorrow.strftime("%A %d %B %Y").upper()

    # Create LaTeX code with dynamic dates
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
\\setlength{{\\parindent}}{{0pt}} % Disable paragraph indentation
\\setlength{{\\parskip}}{{1em}} % Adjust paragraph spacing

% Define header color
\\definecolor{{headerblue}}{{RGB}}{{0, 112, 192}}
\\geometry{{left=0.3cm, right=0.2cm, top=0.0cm, bottom=0.3cm}} % Reduce margins for a compact layout

\\begin{{document}}

% Start of layout
\\noindent
\\begin{{minipage}}[t]{{0.4\\textwidth}} % Left minipage taking 48% of the width
    % Top part of the left minipage
    \\includegraphics[width=1.5cm]{{zim_coat_of_arms}}
    \\textbf{{\\small GOVERNMENT OF ZIMBABWE}} \\\\[0.1cm]
    \\tiny{{MINISTRY OF ENVIRONMENT, CLIMATE AND WILD LIFE}}
    \\hrule 
    \\vspace{{0.2cm}}
    \\includegraphics[width=1.5cm]{{MSD_logo}}
    \\centering
    \\textbf{{\\large Meteorological Services }} \\\\
    \\tiny P.O. Box BE150 BELVEDERE HARARE \\\\[0.3cm]
    \\vspace{{0.5cm}} % Space between top and bottom sections

    % Bottom part of the left minipage
   \\textbf{{\\Large{{WEATHER \\\\ REPORT \& \\\\ [0.2cm]FORECAST}}}} \\\\[0.3cm]
    \\begin{{itemize}}
        \\item Cloud cover forecast.
    \\end{{itemize}}
\\end{{minipage}}
\\hfill % Horizontal space between left and right minipages
\\begin{{minipage}}[t]{{0.6\\textwidth}} % Right minipage taking 48% of the width
    \\textbf{{\\large SATELLITE-BASED GLANCE INTO THIS MORNING, {today_date}}} \\\\[0.3cm]
    \\begin{{wrapfigure}}{{r}}{{0.45\\textwidth}} % Wrapping the image to the right
        \\includegraphics[width=4.0cm]{{nce_today}} % Replace 'satellite_image' with your image name
    \\end{{wrapfigure}}
    The country experienced no rainfall yesterday, attributed to suppressed middle-level atmospheric circulation. As a result, conditions remained predominantly cloudless and hot. Similar weather is expected today, with clear skies prevailing across most regions.
    \\vspace{{0.3cm}}

\\end{{minipage}}

% First Header: WEATHER FORECAST: TOMORROW
\\noindent
\\textcolor{{white}}{{\\colorbox{{headerblue}}{{\\parbox{{\\textwidth}}{{\\centering \\Large \\textbf{{WEATHER FORECAST: {tomorrow_date}}}}}}}}

\\vspace{{0.5cm}}

% Compartment 1: Forecast for Tomorrow
\\noindent
\\begin{{minipage}}[t]{{0.48\\textwidth}} % Image on the left
    \\vspace{{0pt}} % Remove any vertical space before the image
    \\includegraphics[height=5.5cm,keepaspectratio]{{day1_forecast}} % Set image height explicitly
\\end{{minipage}}
\\hfill
\\begin{{minipage}}[t]{{0.48\\textwidth}} % Text on the right
    \\vspace{{0pt}} % Ensure text starts at the very top
    \\raggedright % Align text to the left
    \\textbf{{Morning:}} Mild and cloudless conditions countrywide are expected. \\\\
    \\textbf{{Afternoon:}} All areas should be sunny and very hot except for Matabeleland North were some partly cloudy periods are expected. \\\\
    \\textbf{{Evening:}} Mostly clear skies and mild conditions. \\\\[5cm]
    \\textbf{{Impacts:}}
    \\begin{{itemize}}
        \\item \\scriptsize{{\\textbf{{Secure loose items outdoors to prevent wind damage.}}}}
        \\item \\textbf{{Take precautions during thunderstorms, especially in open areas.}}
    \\end{{itemize}}
\\end{{minipage}}

\\vspace{{1cm}} % Space before the second header

% Second Header: WEATHER FORECAST: OUTLOOK
\\noindent
\\textcolor{{white}}{{\\colorbox{{headerblue}}{{\\parbox{{\\textwidth}}{{\\centering \\Large \\textbf{{WEATHER FORECAST: OUTLOOK}}}}}}}}

\\vspace{{0.5cm}}

% Compartment 2: Forecast for the Outlook
\\noindent
\\begin{{minipage}}[t]{{0.48\\textwidth}} % Image on the left
    \\vspace{{0pt}} % Remove any vertical space before the image
    \\includegraphics[height=5.5cm,keepaspectratio]{{day2_forecast}} % Set imag
