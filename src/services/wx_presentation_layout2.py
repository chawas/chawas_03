\documentclass{beamer}
\usepackage{graphicx} % For images
\usepackage{hyperref} % For clickable links
\usepackage{multicol} % For multi-column layouts
\usepackage[table,xcdraw]{xcolor} % For colors

% Set a light-colored title bar
\usecolortheme{dove} % Light color scheme
\setbeamercolor{frametitle}{bg=blue!10, fg=black} % Light blue title bar background

% Title page customizations
\title[Weather Forecast]{Weather Forecast Presentation}
\author{Meteorological Services Department}
\date{\today}

\begin{document}

% Title Slide
\begin{frame}
    \titlepage
    \begin{center}
        \includegraphics[width=0.15\textwidth]{court_of_arms.png} \hspace{1cm}
        \includegraphics[width=0.2\textwidth]{met_services_logo.png} \hspace{1cm}
        \includegraphics[width=0.15\textwidth]{civil_protection_logo.png}
    \end{center}
\end{frame}

% Weather Overview Slide
\begin{frame}{\textbf{Weather Highlights}}
    \begin{itemize}
        \item \textbf{Heavy rainfall} expected in northern and eastern regions.
        \item \textbf{Dry conditions} to prevail in the southern areas.
        \item \textbf{Moderate winds} in the central region.
        \item \textbf{Cool temperatures} in the western highlands.
    \end{itemize}
\end{frame}

% Satellite Image Slide
\begin{frame}{\textbf{Satellite Imagery}}
    \begin{center}
        \includegraphics[width=0.8\textwidth]{satellite_image.png} % Replace with your satellite image
    \end{center}
    \textbf{Figure:} Satellite image showing cloud cover as of \today.
\end{frame}

% Rainfall Chart Slide
\begin{frame}{\textbf{Rainfall Chart}}
    \begin{center}
        \includegraphics[width=0.8\textwidth]{rainfall_chart.png} % Replace with your rainfall chart image
    \end{center}
    \textbf{Figure:} Rainfall distribution forecast for the next 5 days.
\end{frame}

% Detailed Forecast Slide
\begin{frame}{\textbf{5-Day Weather Forecast}}
    \begin{center}
        \renewcommand{\arraystretch}{1.5}
        \begin{tabular}{|l|c|c|c|c|c|}
            \hline
            \rowcolor[HTML]{D9EAD3}
            \textbf{Station} & \textbf{Day 1} & \textbf{Day 2} & \textbf{Day 3} & \textbf{Day 4} & \textbf{Day 5} \\
            \hline
            Harare & 28°C / 15°C \newline 0mm & 27°C / 14°C \newline 2mm & 25°C / 13°C \newline 15mm & 26°C / 12°C \newline 1mm & 30°C / 16°C \newline 0mm \\
            \hline
            Bulawayo & 29°C / 16°C \newline 3mm & 25°C / 14°C \newline 20mm & 28°C / 15°C \newline 0mm & 27°C / 13°C \newline 2mm & 26°C / 12°C \newline 10mm \\
            \hline
            Victoria Falls & 31°C / 18°C \newline 0mm & 32°C / 20°C \newline 0mm & 28°C / 17°C \newline 25mm & 29°C / 19°C \newline 5mm & 33°C / 22°C \newline 0mm \\
            \hline
        \end{tabular}
    \end{center}
    \vspace{0.3cm}
    \textbf{Note:} Temperatures in °C and rainfall in mm.
\end{frame}

% Useful Links Slide
\begin{frame}{\textbf{Important Resources}}
    \begin{itemize}
        \item \href{https://www.weather.gov/}{National Weather Service}
        \item \href{https://www.satellite-imagery.com/}{Satellite Imagery}
        \item \href{https://www.meteorology.org/forecasts}{Meteorological Department Forecasts}
        \item \href{https://www.civilprotection.org/alerts}{Civil Protection Alerts}
    \end{itemize}
    \vspace{0.5cm}
    \textbf{Contact Us:} \\
    \texttt{email@example.com} \\
    \texttt{+123 456 7890}
\end{frame}

\end{document}
