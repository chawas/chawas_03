from datetime import datetime, timedelta

# Generate date dynamically
today = datetime.now()
tomorrow = today + timedelta(days=1)

# Format dates as strings
today_date = today.strftime("%A %d %B %Y").upper()  # e.g., "SATURDAY 19 OCTOBER 2024"
tomorrow_date = tomorrow.strftime("%A %d %B %Y").upper()

# Inject the dates into LaTeX
latex_code = f"""
\\textcolor{{white}}{{\\colorbox{{headerblue}}{{\\parbox{{\\textwidth}}{{\\centering \\Large \\textbf{{WEATHER FORECAST: {today_date}}}}}}}}

\\vspace{{0.5cm}}

\\noindent
\\textcolor{{white}}{{\\colorbox{{headerblue}}{{\\parbox{{\\textwidth}}{{\\centering \\Large \\textbf{{WEATHER FORECAST: OUTLOOK ({tomorrow_date})}}}}}}}}
"""
