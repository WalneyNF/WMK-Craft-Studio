@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  py -3 studio_web.py --open
  goto :end
)
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  python studio_web.py --open
  goto :end
)
echo.
echo Python 3 nao foi encontrado.
echo Instale o Python 3.12 ou superior e marque a opcao para adiciona-lo ao PATH.
echo Endereco oficial: https://www.python.org/downloads/
echo.
pause
:end
endlocal
