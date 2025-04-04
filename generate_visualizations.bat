@echo off
echo AI Heat Map Visualization Generator
echo ================================
echo.

if "%1"=="" (
    echo Usage: generate_visualizations.bat [year]
    echo Example: generate_visualizations.bat 2023
    echo Example: generate_visualizations.bat all
    echo.
    echo Generating visualizations for all available years...
    python generate_heatmap.py
) else if "%1"=="all" (
    echo Generating visualizations for all available years...
    python generate_heatmap.py
) else (
    echo Generating visualizations for year %1...
    python generate_heatmap.py %1
)

echo.
echo All visualizations have been saved to the 'visualizations' folder.
echo. 