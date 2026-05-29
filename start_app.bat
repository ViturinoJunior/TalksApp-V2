@echo off
REM Script para iniciar a aplicação TalksApp
cd /d "%~dp0"

echo.
echo ════════════════════════════════════════════════════════════
echo              INICIANDO TALKSAPP - APLICAÇÃO FLASK
echo ════════════════════════════════════════════════════════════
echo.

REM Instalar dependências
echo [1/3] Verificando dependências...
py -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências
    pause
    exit /b 1
)
echo ✅ Dependências instaladas

echo.
echo [2/3] Limpando banco de dados antigo...
if exist database.db del database.db
echo ✅ Banco de dados limpo

echo.
echo [3/3] Iniciando servidor...
echo.
echo ════════════════════════════════════════════════════════════
echo Servidor rodando em: http://127.0.0.1:5000
echo ════════════════════════════════════════════════════════════
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

REM Iniciar a aplicação
py app.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Erro ao executar a aplicação
    pause
    exit /b 1
)
