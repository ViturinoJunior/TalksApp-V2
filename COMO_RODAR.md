# 🚀 COMO RODAR A APLICAÇÃO TALKSAPP

## ⚡ INÍCIO RÁPIDO

### Opção 1: Script Batch (Windows)

```batch
# Duplo clique em:
start_app.bat
```

Ou no terminal:

```cmd
start_app.bat
```

### Opção 2: Script Python (Windows/Linux/Mac)

```bash
python start_app.py
```

Ou:

```bash
py start_app.py
```

### Opção 3: Execução Manual

**Passo 1: Instalar dependências**

```bash
pip install -r requirements.txt
```

**Passo 2: Executar aplicação**

```bash
python app.py
```

---

## 🌐 ACESSO

Após iniciar, abra no navegador:

```
http://127.0.0.1:5000
```

---

## 📋 O QUE ESPERAR

Ao iniciar, você verá:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
 * Restarting with reloader
 * Debugger is active!
```

---

## 🧪 PRIMEIRO TESTE

1. **Abra o navegador:**
   - http://127.0.0.1:5000

2. **Clique em "Cadastro":**
   - Nome: João Silva
   - Login: joao_silva
   - Senha: senha123
   - Nascimento: 2000-01-15

3. **Clique em Cadastrar:**
   - ✅ Deve redirecionar para login

4. **Faça login:**
   - Login: joao_silva
   - Senha: senha123
   - ✅ Deve acessar o chat

5. **Envie uma mensagem:**
   - Digite: "Olá, mundo!"
   - ✅ Mensagem deve aparecer no chat

---

## ⚙️ CONFIGURAÇÕES

### SECRET_KEY (Produção)

Para usar uma chave segura em produção:

**Windows:**

```cmd
set SECRET_KEY=sua_chave_super_secreta_aqui
python app.py
```

**Linux/Mac:**

```bash
export SECRET_KEY=sua_chave_super_secreta_aqui
python app.py
```

---

## 🛑 PARAR A APLICAÇÃO

Pressione: **Ctrl + C** no terminal

---

## 🐛 TROUBLESHOOTING

### Erro: "ModuleNotFoundError: No module named 'flask'"

```bash
pip install flask werkzeug
```

### Erro: "Port 5000 is already in use"

```bash
# Windows - parar processo na porta 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac - parar processo na porta 5000
lsof -ti:5000 | xargs kill -9
```

### Erro: "database.db is locked"

```bash
# Remover arquivo de lock (se houver)
rm database.db-journal

# Ou simplesmente remover o banco
rm database.db
# Ele será recriado ao iniciar a app
```

---

## ✅ VERIFICAÇÃO

Para validar que tudo funciona:

```bash
python validate_fixes.py
```

Este script testa:

- ✅ Cadastro
- ✅ Login
- ✅ Chat
- ✅ Mensagens
- ✅ Segurança

---

## 📊 ESTRUTURA DE ARQUIVOS

```
TalksApp/
├── app.py                    # Aplicação principal (CORRIGIDA)
├── database.db              # Banco de dados (criado automaticamente)
├── requirements.txt         # Dependências (ATUALIZADO)
├── start_app.bat            # Script para iniciar (Windows)
├── start_app.py             # Script para iniciar (Windows/Mac/Linux)
├── validate_fixes.py        # Script de validação
├── run_test.bat             # Outro script de teste
├── templates/               # Templates HTML
│   ├── index.html
│   ├── cadastro.html
│   ├── login.html
│   └── chat.html
└── static/                  # Arquivos estáticos
    ├── style.css
    └── script.js
```

---

## 🔍 MONITORAR REQUISIÇÕES

Durante o desenvolvimento, você verá logs de cada requisição:

```
127.0.0.1 - - [28/May/2026 20:51:48] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [28/May/2026 20:51:49] "POST /cadastro HTTP/1.1" 302 -
127.0.0.1 - - [28/May/2026 20:51:50] "GET /login HTTP/1.1" 200 -
```

---

## 📚 PRÓXIMOS PASSOS

Depois que a aplicação estiver rodando:

1. Testar cadastro e login
2. Validar senhas hasheadas no banco
3. Testar mensagens
4. Testar usuários online
5. Testar logout

---

## 💡 DICAS

- Abra o DevTools (F12) para ver requisições
- Verifique o console do servidor para erros
- Use o banco SQLite Browser para inspecionar database.db
- Em Windows, você pode criar um atalho para start_app.bat

---

**Pronto para rodar! 🚀**

Se tiver problemas, consulte a documentação em ~/.copilot/session-state/
