import pandas as pd

# Load CSV data
data = pd.read_csv("forecast.csv")

# LaTeX table template
table_template = r"""
\begin{frame}{5-Day Weather Forecast}
    \small % Adjust font size to fit more rows
    \renewcommand{\arraystretch}{1.5} % Adjust row height for readability
    \begin{tabular}{|l|>{\centering\arraybackslash}m{1.5cm}|>{\centering\arraybackslash}m{1.5cm}|>{\centering\arraybackslash}m{1.5cm}|>{\centering\arraybackslash}m{1.5cm}|>{\centering\arraybackslash}m{1.5cm}|}
        \hline
        \rowcolor[HTML]{D9EAD3} 
        \textbf{Station} & \textbf{Day 1} & \textbf{Day 2} & \textbf{Day 3} & \textbf{Day 4} & \textbf{Day 5} \\
        \hline
%s
    \end{tabular}
\end{frame}
"""

# Generate LaTeX table rows
rows = []
for index, row in data.iterrows():
    station = row["Station"]
    days = [row[f"Day {i}"].replace("\n", r"\\") for i in range(1, 6)]  # Replace line breaks
    row_data = f"        {station} & " + " & ".join(days) + r" \\ \hline"
    rows.append(row_data)

# Combine rows into table
table_content = "\n".join(rows)
latex_table = table_template % table_content

# Save to a LaTeX file
with open("forecast_table.tex", "w") as file:
    file.write(latex_table)

print("LaTeX table generated and saved as 'forecast_table.tex'")
