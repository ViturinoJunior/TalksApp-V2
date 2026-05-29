# 💬 TalksApp - Chat em Tempo Real

Aplicação de mensageria online desenvolvida com **Flask**, **HTML5**, **JavaScript** e **CSS3**.

## ⚡ Características

- ✅ Cadastro e login de usuários com senha hasheada
- ✅ Chat público em tempo real
- ✅ Chat privado entre usuários
- ✅ Controle de usuários online
- ✅ Interface responsiva
- ✅ Banco de dados SQLite integrado

---

## 🚀 Deploy Rápido (Recomendado)

A aplicação está **pronta para produção** e pode ser deployada em minutos!

### Plataformas Suportadas

| Plataforma                             | Custo            | Setup      |
| -------------------------------------- | ---------------- | ---------- |
| **[Render.com](https://render.com)**   | Gratuito         | 2-3 min ⚡ |
| **[Railway.app](https://railway.app)** | Gratuito (trial) | 2-3 min    |
| **[Heroku](https://heroku.com)**       | $5+/mês          | 2-3 min    |

👉 **[Guia Completo de Deploy](DEPLOY.md)**

---

## 💻 Executar Localmente

### Pré-requisitos

- Python 3.7+
- pip (gerenciador de pacotes)

### Instalação

```bash
# 1. Clone o repositório
git clone <seu-repositorio>
cd TalksApp

# 2. Instale dependências
pip install -r requirements.txt

# 3. Execute a aplicação
python app.py
```

### Acesso

Abra o navegador em: **http://localhost:5000**

---

## 📝 Primeiro Uso

1. **Cadastre um novo usuário:**
   - Nome: João Silva
   - Login: joao_silva
   - Senha: senha123
   - Nascimento: 2000-01-15

2. **Faça login** com suas credenciais

3. **Envie mensagens** no chat público

4. **Inicie conversas privadas** com outros usuários online

---

## 📂 Estrutura do Projeto

```
TalksApp/
├── app.py                 # Aplicação principal (Flask)
├── requirements.txt       # Dependências (pip)
├── Procfile              # Configuração de deploy
├── runtime.txt           # Versão do Python
├── .gitignore            # Arquivos ignorados
├── templates/            # Templates HTML
│   ├── index.html        # Homepage
│   ├── cadastro.html     # Página de registro
│   ├── login.html        # Página de login
│   ├── chat.html         # Chat público
│   └── chat_privado.html # Chat privado
├── static/               # Arquivos estáticos
│   ├── style.css         # Estilos
│   └── script.js         # JavaScript
├── README.md             # Este arquivo
└── DEPLOY.md             # Guia de deploy
```

---

## 🔒 Segurança

- ✅ Senhas hasheadas com werkzeug
- ✅ Sessões Flask seguras
- ✅ Validação de entrada de dados
- ✅ Proteção de rotas autenticadas
- ✅ Variáveis de ambiente para secrets

---

## 📚 Tecnologias

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Banco de Dados:** SQLite
- **Deploy:** Gunicorn + Render/Railway

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flask'"

```bash
pip install -r requirements.txt
```

### Porta 5000 já em uso

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Banco de dados corrompido

```bash
# Remover e recriar
rm database.db
python app.py
```

---

## 📖 Documentação

- [Guia de Deploy](DEPLOY.md) - Passo a passo para colocar em produção
- [Flask Docs](https://flask.palletsprojects.com/) - Documentação do Flask
- [Python Docs](https://docs.python.org/) - Documentação do Python

---

## 📄 Licença

Este projeto é de código aberto. Sinta-se livre para usar, modificar e distribuir.

---

**Desenvolvido com ❤️ em Flask**
