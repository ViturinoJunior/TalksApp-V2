#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para validar as correções realizadas no TalksApp
"""

import subprocess
import time
import requests
import json
import sys

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_api():
    BASE_URL = "http://127.0.0.1:5000"
    
    print_section("INICIANDO TESTES DA APLICAÇÃO")
    
    try:
        # Teste 1: Home
        print("\n[✓] Teste 1: HOME (/)")
        resp = requests.get(f"{BASE_URL}/")
        assert resp.status_code == 200, f"Status esperado 200, recebido {resp.status_code}"
        print(f"    Status: {resp.status_code} - OK")
        
        # Teste 2: Cadastro GET
        print("\n[✓] Teste 2: CADASTRO GET (/cadastro)")
        resp = requests.get(f"{BASE_URL}/cadastro")
        assert resp.status_code == 200, f"Status esperado 200, recebido {resp.status_code}"
        print(f"    Status: {resp.status_code} - OK")
        
        # Teste 3: Login GET
        print("\n[✓] Teste 3: LOGIN GET (/login)")
        resp = requests.get(f"{BASE_URL}/login")
        assert resp.status_code == 200, f"Status esperado 200, recebido {resp.status_code}"
        print(f"    Status: {resp.status_code} - OK")
        
        # Teste 4: Cadastro POST - Menor de idade (deve rejeitar)
        print("\n[✓] Teste 4: CADASTRO - REJEIÇÃO DE MENOR")
        dados = {
            "nome": "Menor Idade",
            "login": f"menor_{int(time.time())}",
            "senha": "senha123",
            "nascimento": "2020-01-01"
        }
        resp = requests.post(f"{BASE_URL}/cadastro", data=dados)
        assert resp.status_code == 200, f"Status esperado 200, recebido {resp.status_code}"
        assert "maiores de 18 anos" in resp.text.lower(), "Mensagem de rejeição não encontrada"
        print(f"    Status: {resp.status_code}")
        print(f"    Mensagem: Rejeição correta de menor - OK")
        
        # Teste 5: Cadastro POST - Usuário válido
        print("\n[✓] Teste 5: CADASTRO - USUÁRIO VÁLIDO")
        timestamp = int(time.time())
        dados = {
            "nome": "João Silva",
            "login": f"joao_{timestamp}",
            "senha": "senha123",
            "nascimento": "2000-01-01"
        }
        resp = requests.post(f"{BASE_URL}/cadastro", data=dados, allow_redirects=False)
        assert resp.status_code in [301, 302, 303, 307, 308], f"Status esperado redirecionamento, recebido {resp.status_code}"
        assert "/login" in resp.headers.get("Location", ""), "Redirecionamento para /login não encontrado"
        print(f"    Status: {resp.status_code}")
        print(f"    Redirecionado para: {resp.headers.get('Location')} - OK")
        
        # Teste 6: Login POST - Usuário válido
        print("\n[✓] Teste 6: LOGIN - USUÁRIO VÁLIDO")
        with requests.Session() as session:
            dados = {
                "login": f"joao_{timestamp}",
                "senha": "senha123"
            }
            resp = session.post(f"{BASE_URL}/login", data=dados, allow_redirects=False)
            assert resp.status_code in [301, 302, 303, 307, 308], f"Status esperado redirecionamento, recebido {resp.status_code}"
            assert "/chat" in resp.headers.get("Location", ""), "Redirecionamento para /chat não encontrado"
            print(f"    Status: {resp.status_code}")
            print(f"    Redirecionado para: {resp.headers.get('Location')} - OK")
            
            # Teste 7: Acessar chat
            print("\n[✓] Teste 7: CHAT (protegido)")
            resp = session.get(f"{BASE_URL}/chat")
            assert resp.status_code == 200, f"Status esperado 200, recebido {resp.status_code}"
            print(f"    Status: {resp.status_code} - OK")
            
            # Teste 8: Enviar mensagem
            print("\n[✓] Teste 8: ENVIAR MENSAGEM")
            dados = {"mensagem": "Olá, mundo!"}
            resp = session.post(f"{BASE_URL}/enviar", data=dados)
            assert resp.status_code == 200, f"Status esperado 200, recebido {resp.status_code}"
            assert "OK" in resp.text, "Resposta esperada 'OK' não encontrada"
            print(f"    Status: {resp.status_code}")
            print(f"    Resposta: {resp.text} - OK")
        
        # Teste 9: Buscar mensagens
        print("\n[✓] Teste 9: BUSCAR MENSAGENS (/mensagens)")
        resp = requests.get(f"{BASE_URL}/mensagens")
        assert resp.status_code == 200, f"Status esperado 200, recebido {resp.status_code}"
        msgs = resp.json()
        assert isinstance(msgs, list), "Esperado JSON array"
        print(f"    Status: {resp.status_code}")
        print(f"    Total de mensagens: {len(msgs)} - OK")
        
        # Teste 10: Usuários online
        print("\n[✓] Teste 10: USUÁRIOS ONLINE (/usuarios_online)")
        resp = requests.get(f"{BASE_URL}/usuarios_online")
        assert resp.status_code == 200, f"Status esperado 200, recebido {resp.status_code}"
        usuarios = resp.json()
        assert isinstance(usuarios, list), "Esperado JSON array"
        print(f"    Status: {resp.status_code}")
        print(f"    Usuários online: {len(usuarios)} - OK")
        
        # Teste 11: Login com senha errada
        print("\n[✓] Teste 11: LOGIN - SENHA ERRADA")
        dados = {
            "login": f"joao_{timestamp}",
            "senha": "senha_errada"
        }
        resp = requests.post(f"{BASE_URL}/login", data=dados)
        assert resp.status_code == 200, f"Status esperado 200, recebido {resp.status_code}"
        assert "inválidos" in resp.text.lower() or "erro" in resp.text.lower(), "Mensagem de erro não encontrada"
        print(f"    Status: {resp.status_code}")
        print(f"    Erro exibido corretamente - OK")
        
        # Teste 12: Mensagem vazia
        print("\n[✓] Teste 12: ENVIAR MENSAGEM VAZIA")
        with requests.Session() as session:
            session.post(f"{BASE_URL}/login", data={"login": f"joao_{timestamp}", "senha": "senha123"})
            resp = session.post(f"{BASE_URL}/enviar", data={"mensagem": ""})
            assert resp.status_code == 400, f"Status esperado 400, recebido {resp.status_code}"
            print(f"    Status: {resp.status_code} - OK")
        
        print_section("TESTES CONCLUÍDOS COM SUCESSO ✅")
        print("\nTodas as correções foram validadas!")
        return True
        
    except AssertionError as e:
        print(f"\n❌ ERRO: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        return False

if __name__ == "__main__":
    print_section("INICIANDO APLICAÇÃO FLASK")
    
    try:
        # Iniciar a aplicação
        print("\nIniciando servidor Flask...")
        processo = subprocess.Popen(
            ['python', 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Aguardar inicialização
        time.sleep(3)
        
        # Testar
        success = test_api()
        
    except KeyboardInterrupt:
        print("\n\nTeste cancelado pelo usuário")
        sys.exit(1)
    finally:
        # Encerrar a aplicação
        print("\nEncerrando aplicação...")
        try:
            processo.terminate()
            processo.wait(timeout=5)
        except:
            processo.kill()
        print("Aplicação encerrada.")
    
    sys.exit(0 if success else 1)
