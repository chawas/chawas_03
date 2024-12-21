from datetime import datetime, timedelta
import os
# Date variables
today = datetime.now()
tomorrow = today + timedelta(days=1)
day_after_tomorrow = today + timedelta(days=2)

# Format dates
today_str = today.strftime("%A, %d %B %Y")
tomorrow_str = tomorrow.strftime("%A, %d %B %Y")
day_after_str = day_after_tomorrow.strftime("%A, %d %B %Y")

# Ensure the target directory exists
os.makedirs(target_dir, exist_ok=True)

# Define the output file path
output_path = os.path.join(target_dir, "dynamic_weather_forecast19.tex")


# LaTeX template
latex_content = f"""
\\documentclass{{beamer}}
\\usepackage{{graphicx}}\\graphicspath{{{{gfx/}}}} % For including images
\\usepackage{{caption}}  % For customizing captions
\\usepackage{{subcaption}} % For subfigures and subcaptions
\\usepackage[table,xcdraw]{{xcolor}} % For colored headers
\\usepackage{{array}} % For better alignment
\\usepackage{{multicol}} % Multi-column layouts

\\begin{{document}}

\\begin{{frame}}{{Four Images with Nested Minipages}}
    \\centering
    % Main frame layout: 4 minipages on one page

    % Top-left minipage with nested layout
    \\begin{{minipage}}[t]{{0.48\\textwidth}}
        \\centering
        \\textbf{{Nested Minipages (Court of Arms and Logo)}}\\\\
        % Nested layout
        \\begin{{minipage}}[t]{{0.45\\textwidth}} % Court of Arms on the left
            \\centering
            \\includegraphics[width=0.9\\textwidth]{{court_of_arms}}\\\\
            \\scriptsize \\textbf{{Court of Arms}}
        \\end{{minipage}}
        \\hfill
        \\begin{{minipage}}[t]{{0.45\\textwidth}} % Court of Arms text on the right
            \\scriptsize
            The Court of Arms represents the authority of the government of Zimbabwe.
        \\end{{minipage}}\\\\

        \\rule{{\\linewidth}}{{0.4pt}} % Horizontal line

        \\begin{{minipage}}[t]{{0.45\\textwidth}} % Meteorological logo on the left
            \\centering
            \\includegraphics[width=0.9\\textwidth]{{met_logo}}\\\\
            \\scriptsize \\textbf{{Meteorological Logo}}
        \\end{{minipage}}
        \\hfill
        \\begin{{minipage}}[t]{{0.45\\textwidth}} % Meteorological logo text on the right
            \\scriptsize
            The Meteorological Services logo signifies the authority and services provided in weather forecasting.
        \\end{{minipage}}
    \\end{{minipage}}
    \\hfill

    % Top-right minipage
    \\begin{{minipage}}[t]{{0.48\\textwidth}}
        \\centering
        \\scriptsize \\textbf{{Infrared Image for Today ({today_str})}}\\\\
        \\includegraphics[width=0.9\\textwidth]{{nce_today}}
    \\end{{minipage}}

    \\vspace{{0.3cm}} % Space between rows

    % Bottom-left minipage
    \\begin{{minipage}}[t]{{0.48\\textwidth}}
        \\centering
        \\scriptsize \\textbf{{Water Vapour for Tomorrow ({tomorrow_str})}}\\\\
        \\includegraphics[width=0.9\\textwidth]{{wv_tomorrow}}
    \\end{{minipage}}
    \\hfill

    % Bottom-right minipage
    \\begin{{minipage}}[t]{{0.48\\textwidth}}
        \\centering
        \\scriptsize \\textbf{{Forecast Map for Day After Tomorrow ({day_after_str})}}\\\\
        \\includegraphics[width=0.9\\textwidth]{{forecast_map_day_after}}
    \\end{{minipage}}
\\end{{frame}}

\\end{{document}}
"""

# Save LaTeX content to a file
output_path = "nested_minipages_forecast.tex"
with open(output_path, "w", encoding="utf-8") as file:
    file.write(latex_content)

print(f"LaTeX file successfully created at {output_path}")

# Define the target directory
target_dir = '/home/wrf/deployed/webb-downloading/wx_presentation/'