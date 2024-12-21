import datetime
import os

# Get yesterday's and tomorrow's date
yesterday = datetime.date.today() - datetime.timedelta(days=1)
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
outlook = datetime.date.today() + datetime.timedelta(days=1)

# Format the dates with specific times
yesterday_infrared_str = yesterday.strftime('%B %d, %Y') + " 06:00Z"
yesterday_water_vapour_str = yesterday.strftime('%B %d, %Y') + " 00:00Z"
tomorrow_infrared_str = tomorrow.strftime('%B %d, %Y') + " 06:00Z"
tomorrow_water_vapour_str = tomorrow.strftime('%B %d, %Y') + " 00:00Z"

# Directory for symbols and HTML files
symbols_dir = "/home/wrf/nons/python-plotting-toolbox/local_outdata/symbograms/"
target_dir = '/home/wrf/deployed/webb-downloading/wx_presentation/'
os.makedirs(target_dir, exist_ok=True)  # Ensure the directory exists
output_path = os.path.join(target_dir, "dates4.tex")


# Generate LaTeX content
latex_content = r"""
\begin{frame}{}

    \begin{columns}[T] % Align columns at the top
        % First column with Infrared Radiation title
        \begin{column}{0.48\textwidth}
            \begin{center}
                \tiny \textbf{Infrared Radiation (Yesterday)} % First title for the first column
            \end{center}
            \vspace{-0.5cm} % Adjust space between title and image
            \begin{center}
                \includegraphics[width=\linewidth]{infra_radiation_yesterday} % Replace with your image
                \vspace{-1cm} % Move image up closer to the title
            \end{center}
        \end{column}

        % Second column with Water Vapour title
        \begin{column}{0.48\textwidth}
            \begin{center}
                \tiny \textbf{Water Vapour (Yesterday)} % Second title for the second column
            \end{center}
            \vspace{-0.5cm} % Adjust space between title and image
            \begin{center}
                \includegraphics[width=\linewidth]{water_vapour_yesterday} % Replace with your image
                \vspace{-1cm} % Move image up closer to the title
            \end{center}
        \end{column}
    \end{columns}

    \vspace{0.45cm} % Add less vertical space between rows to close the gap

    % Add images for the second row
    \begin{columns}[T] % Second row with Tomorrow images
        % First column for Today image
        \begin{column}{0.48\textwidth}
            \begin{center}
                \tiny\textbf{Today} % Title for the image
                \includegraphics[width=\linewidth]{infra_radiation_today} % Replace with your image
                \vspace{-0.5cm} % Reduce space between image and title
            \end{center}
        \end{column}

        % Second column for Tomorrow image
        \begin{column}{0.48\textwidth}
            \begin{center}
                \tiny\textbf{Today} % Title for the image
                \includegraphics[width=\linewidth]{water_vapour_today} % Replace with your image
                \vspace{-0.5cm} % Reduce space between image and title
            \end{center}
        \end{column}
    \end{columns}

\end{frame}
"""

# Save LaTeX content to a file
#output_path = "weather_forecast_with_dates_and_times.tex"
with open(output_path, "w", encoding="utf-8") as file:
    file.write(latex_content)

print(f"LaTeX document saved to {output_path}")
