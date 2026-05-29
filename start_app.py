#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para iniciar a aplicação TalksApp
"""

import subprocess
import sys
import os
import time

print("\n" + "="*60)
print("  INICIANDO TALKSAPP - APLICAÇÃO FLASK")
print("="*60 + "\n")

# Mudar para diretório da aplicação
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Passo 1: Instalar dependências
print("[1/3] Verificando dependências...")
resultado = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"], 
                          capture_output=True)
if resultado.returncode != 0:
    print("❌ Erro ao instalar dependências")
    print(resultado.stderr.decode())
    sys.exit(1)
print("✅ Dependências instaladas\n")

# Passo 2: Limpar banco de dados (opcional)
print("[2/3] Limpando banco de dados antigo...")
if os.path.exists("database.db"):
    try:
        os.remove("database.db")
        print("✅ Banco de dados limpo\n")
    except Exception as e:
        print(f"⚠️  Não foi possível limpar: {e}\n")
else:
    print("ℹ️  Banco de dados não encontrado\n")

# Passo 3: Iniciar aplicação
print("[3/3] Iniciando servidor...\n")
print("="*60)
print("Servidor rodando em: http://127.0.0.1:5000")
print("="*60)
print("\nPressione Ctrl+C para parar o servidor\n")

try:
    # Iniciar app.py
    subprocess.run([sys.executable, "app.py"])
except KeyboardInterrupt:
    print("\n\n✅ Servidor parado pelo usuário")
    sys.exit(0)
except Exception as e:
    print(f"\n❌ Erro ao executar: {e}")
    sys.exit(1)
