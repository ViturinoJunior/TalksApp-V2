@echo off
cd /d "%~dp0"
echo ====================================================
echo   TESTE DE FUNCIONAMENTO - TalksApp
echo ====================================================
echo.
echo [1] Verificando dependencias...
py -m pip install flask requests --quiet 2>nul
if %errorlevel% neq 0 (
    echo Erro ao instalar dependencias
    exit /b 1
)
echo OK - Dependencias instaladas
echo.
echo [2] Executando testes...
py test_app.py
echo.
pause
