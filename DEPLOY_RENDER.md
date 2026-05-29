# Deploy no Render

## 1. Criar conta
Acesse:
https://render.com

## 2. Enviar projeto para GitHub
Crie um repositório e envie os arquivos.

## 3. Criar Web Service
No Render:
- New +
- Web Service
- Conecte seu GitHub
- Escolha o repositório

## 4. Configurações

Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app

## 5. Variáveis de Ambiente

SECRET_KEY=sua_chave_super_segura

## 6. Deploy
Clique em:
Create Web Service

Pronto.
