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
    \\begin{{itemi
