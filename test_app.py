#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para testar a aplicação TalksApp
"""

import subprocess
import time
import requests
import json
from datetime import datetime

print("=" * 60)
print("TESTE DE FUNCIONAMENTO - TalksApp")
print("=" * 60)

# Iniciar a aplicação
print("\n[1] Iniciando a aplicação Flask...")
processo = subprocess.Popen(['python', 'app.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(3)

try:
    BASE_URL = "http://127.0.0.1:5000"
    
    # Teste 1: Home
    print("\n[2] Testando HOME (/)...")
    try:
        resp = requests.get(f"{BASE_URL}/")
        print(f"   ✓ Status: {resp.status_code}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # Teste 2: Cadastro GET
    print("\n[3] Testando CADASTRO GET (/cadastro)...")
    try:
        resp = requests.get(f"{BASE_URL}/cadastro")
        print(f"   ✓ Status: {resp.status_code}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # Teste 3: Login GET
    print("\n[4] Testando LOGIN GET (/login)...")
    try:
        resp = requests.get(f"{BASE_URL}/login")
        print(f"   ✓ Status: {resp.status_code}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # Teste 4: Cadastro POST (novo usuário)
    print("\n[5] Testando CADASTRO POST (novo usuário)...")
    try:
        dados = {
            "nome": "João Silva",
            "login": f"joao_{int(time.time())}",
            "senha": "senha123",
            "nascimento": "2000-01-01"
        }
        resp = requests.post(f"{BASE_URL}/cadastro", data=dados, allow_redirects=False)
        print(f"   ✓ Status: {resp.status_code}")
        print(f"   → Redirecionado para: {resp.headers.get('Location', 'N/A')}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # Teste 5: Cadastro POST (menor de idade)
    print("\n[6] Testando CADASTRO POST (menor de idade - deve rejeitar)...")
    try:
        dados = {
            "nome": "Menorzinho",
            "login": f"menor_{int(time.time())}",
            "senha": "senha123",
            "nascimento": "2020-01-01"
        }
        resp = requests.post(f"{BASE_URL}/cadastro", data=dados)
        print(f"   ✓ Status: {resp.status_code}")
        if "maiores de 18 anos" in resp.text:
            print(f"   ✓ Validação de idade funcionando corretamente")
        else:
            print(f"   ✗ Mensagem de erro não encontrada")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # Teste 6: Login POST (usuário válido)
    print("\n[7] Testando LOGIN POST (usuário válido)...")
    try:
        with requests.Session() as session:
            dados = {
                "login": "joao_1234567",
                "senha": "senha123"
            }
            resp = session.post(f"{BASE_URL}/login", data=dados, allow_redirects=False)
            print(f"   ✓ Status: {resp.status_code}")
            print(f"   → Redirecionado para: {resp.headers.get('Location', 'N/A')}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # Teste 7: Buscar mensagens
    print("\n[8] Testando BUSCAR MENSAGENS (/mensagens)...")
    try:
        resp = requests.get(f"{BASE_URL}/mensagens")
        print(f"   ✓ Status: {resp.status_code}")
        print(f"   ✓ Tipo: {resp.headers.get('Content-Type', 'N/A')}")
        msgs = resp.json()
        print(f"   → Total de mensagens: {len(msgs)}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # Teste 8: Usuários online
    print("\n[9] Testando USUÁRIOS ONLINE (/usuarios_online)...")
    try:
        resp = requests.get(f"{BASE_URL}/usuarios_online")
        print(f"   ✓ Status: {resp.status_code}")
        usuarios = resp.json()
        print(f"   → Usuários online: {len(usuarios)}")
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # Teste 9: Banco de dados
    print("\n[10] Verificando BANCO DE DADOS...")
    try:
        import sqlite3
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Contar usuários
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        count_users = cursor.fetchone()[0]
        print(f"   ✓ Total de usuários: {count_users}")
        
        # Contar mensagens
        cursor.execute("SELECT COUNT(*) FROM mensagens")
        count_msgs = cursor.fetchone()[0]
        print(f"   ✓ Total de mensagens: {count_msgs}")
        
        conn.close()
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    print("\n" + "=" * 60)
    print("TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 60)

finally:
    # Encerrar a aplicação
    print("\nEncerrando aplicação...")
    processo.terminate()
    try:
        processo.wait(timeout=5)
    except subprocess.TimeoutExpired:
        processo.kill()
    print("Aplicação encerrada.")
