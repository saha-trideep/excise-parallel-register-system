@echo off
echo ========================================
echo   UNINSTALL UNUSED PDF PACKAGES
echo ========================================
echo.
echo This will uninstall:
echo   - WeasyPrint (doesn't work on Windows without GTK)
echo   - Related dependencies
echo.
echo KEEPING (useful for future):
echo   - jinja2 (templates)
echo   - plotly (charts)
echo.
pause
echo.
echo Uninstalling WeasyPrint...
pip uninstall weasyprint -y

echo.
echo Uninstalling WeasyPrint dependencies...
pip uninstall pycairo -y
pip uninstall PyGObject -y
pip uninstall cairocffi -y
pip uninstall cffi -y
pip uninstall pycparser -y
pip uninstall tinycss2 -y
pip uninstall cssselect2 -y
pip uninstall Pyphen -y

echo.
echo ========================================
echo   CLEANUP COMPLETE!
echo ========================================
echo.
echo Uninstalled: WeasyPrint + dependencies
echo Kept: jinja2, plotly (useful for future)
echo.
echo Your ReportLab PDF system works perfectly!
echo No other packages needed.
echo.
pause
