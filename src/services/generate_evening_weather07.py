from datetime import datetime, timedelta
import os
import subprocess


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
    output_path = os.path.join(target_dir, "dynamic_weather_forecast23.tex")

    # LaTeX template with date variables integrated
    latex_code = f"""
\\PassOptionsToPackage{{table,xcdraw}}{{xcolor}}
\\documentclass{{beamer}}
\\usepackage{{graphicx}}\\graphicspath{{{{images/}}}} % For including images
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
            \\includegraphics[width=0.9\\textwidth]{{zim_court_of_arms}}\\\\
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
            \\includegraphics[width=0.9\\textwidth]{{MSD_Logo}}\\\\
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
        \\scriptsize \\textbf{{Infrared Image for Today ({today_date})}}\\\\
        \\includegraphics[width=0.9\\textwidth]{{nce_today}}
    \\end{{minipage}}

    \\vspace{{0.3cm}} % Space between rows

    % Bottom-left minipage
    \\begin{{minipage}}[t]{{0.48\\textwidth}}
        \\centering
        \\scriptsize \\textbf{{Water Vapour for Tomorrow ({tomorrow_date})}}\\\\
        \\includegraphics[width=0.9\\textwidth]{{water_vapour_today}}
    \\end{{minipage}}
    \\hfill

    % Bottom-right minipage
    \\begin{{minipage}}[t]{{0.48\\textwidth}}
        \\centering
        \\scriptsize \\textbf{{Forecast Map for Day After Tomorrow ({outlook_date})}}\\\\
        \\includegraphics[width=0.9\\textwidth]{{water_vapour_yesterday}}
    \\end{{minipage}}
\\end{{frame}}

\\end{{document}}
"""

    # Write LaTeX code to the output file
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(latex_code)

    print(f"LaTeX file successfully written to: {output_path}")
    return output_path  # Return the file path


# Define the target directory
target_dir = '/home/wrf/deployed/webb-downloading/wx_presentation/'


def create_pdf_from_latex(tex_file):
    """
    Compiles a LaTeX file into a PDF using pdflatex.
    """
    try:
        # Run pdflatex twice to ensure all references are updated
        subprocess.run(['pdflatex', tex_file], check=True)
        subprocess.run(['pdflatex', tex_file], check=True)

        print(f"PDF successfully created for {tex_file}.")

    except subprocess.CalledProcessError as e:
        print(f"Error during LaTeX compilation: {e}")
    finally:
        # Clean up auxiliary files
        base_name = os.path.splitext(tex_file)[0]
        for ext in ['.aux', '.log', '.out']:
            aux_file = f"{base_name}{ext}"
            if os.path.exists(aux_file):
                os.remove(aux_file)
                print(f"Deleted auxiliary file: {aux_file}")


# Generate LaTeX content and write to the file
latex_file = generate_latex_with_dates(target_dir)

# Compile the LaTeX file into PDF
create_pdf_from_latex(latex_file)
