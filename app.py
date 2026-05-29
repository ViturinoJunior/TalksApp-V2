from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "talksapp_secret_dev_key_change_in_production")
# CALCULAR IDADE
def calcular_idade(nascimento):

    nascimento = datetime.strptime(
        nascimento,
        "%Y-%m-%d"
    ).date()

    hoje = date.today()

    idade = hoje.year - nascimento.year

    if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
        idade -= 1

    return idade

# CONEXÃO
def conectar():
    return sqlite3.connect("database.db")

# CRIAR BANCO
def criar_banco():

    conexao = conectar()
    cursor = conexao.cursor()

    # TABELA USUÁRIOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        login TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        nascimento TEXT NOT NULL,
        online INTEGER DEFAULT 0
    )
    """)

    # TABELA MENSAGENS (CHAT PÚBLICO)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensagens(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,
        mensagem TEXT NOT NULL,
        horario TEXT NOT NULL
    )
    """)

    # TABELA CONVERSAS PRIVADAS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversas_privadas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario1 TEXT NOT NULL,
        usuario2 TEXT NOT NULL,
        criada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(usuario1, usuario2)
    )
    """)

    # TABELA MENSAGENS PRIVADAS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensagens_privadas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversa_id INTEGER NOT NULL,
        remetente TEXT NOT NULL,
        conteudo TEXT NOT NULL,
        horario TEXT NOT NULL,
        lida INTEGER DEFAULT 0,
        FOREIGN KEY(conversa_id) REFERENCES conversas_privadas(id)
    )
    """)

    conexao.commit()
    conexao.close()

criar_banco()

# HOME
@app.route("/")
def home():
    return render_template("index.html")

# CADASTRO
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form.get("nome", "").strip()
        login = request.form.get("login", "").strip()
        senha = request.form.get("senha", "").strip()
        nascimento = request.form.get("nascimento", "").strip()
        
        if not all([nome, login, senha, nascimento]):
            return "Todos os campos são obrigatórios"
        
        idade = calcular_idade(nascimento)

        if idade < 18:
            return """
        <h1 style='color:red;text-align:center'>
            Cadastro permitido apenas para maiores de 18 anos.
        </h1>
        """
        
        conexao = conectar()
        cursor = conexao.cursor()

        try:
            senha_hash = generate_password_hash(senha)
            cursor.execute("""
            INSERT INTO usuarios(nome, login, senha, nascimento)
            VALUES (?, ?, ?, ?)
            """, (nome, login, senha_hash, nascimento))

            conexao.commit()

        except sqlite3.IntegrityError:
            return "Usuário já existe"
        except Exception as e:
            return f"Erro ao cadastrar: {str(e)}"
        finally:
            conexao.close()

        return redirect("/login")

    return render_template("cadastro.html")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        login = request.form.get("login", "").strip()
        senha = request.form.get("senha", "").strip()
        
        if not login or not senha:
            return render_template("login.html", erro="Login e senha são obrigatórios")

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
        SELECT id, nome, login, senha FROM usuarios
        WHERE login=?
        """, (login,))

        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario[3], senha):
            session["usuario"] = usuario[1]

            cursor.execute("""
            UPDATE usuarios
            SET online=1
            WHERE login=?
            """, (login,))

            conexao.commit()
            conexao.close()

            return redirect("/chat")
        
        conexao.close()
        return render_template("login.html", erro="Login ou senha inválidos")

    return render_template("login.html")

# CHAT
@app.route("/chat")
def chat():

    if "usuario" not in session:
        return redirect("/login")

    return render_template(
        "chat.html",
        usuario=session["usuario"]
    )

# ENVIAR MENSAGEM
@app.route("/enviar", methods=["POST"])
def enviar():

    if "usuario" not in session:
        return redirect("/login")

    mensagem = request.form.get("mensagem", "").strip()
    
    if not mensagem:
        return "Mensagem vazia", 400

    horario = datetime.now().strftime("%H:%M")

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
        INSERT INTO mensagens(usuario, mensagem, horario)
        VALUES (?, ?, ?)
        """, (session["usuario"], mensagem, horario))

        conexao.commit()
    except Exception as e:
        conexao.close()
        return f"Erro ao enviar mensagem: {str(e)}", 500
    finally:
        conexao.close()

    return "OK"

# BUSCAR MENSAGENS
@app.route("/mensagens")
def mensagens():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT usuario, mensagem, horario
    FROM mensagens
    ORDER BY id ASC
    """)

    dados = cursor.fetchall()

    conexao.close()

    mensagens = []

    for msg in dados:

        mensagens.append({
            "usuario": msg[0],
            "mensagem": msg[1],
            "horario": msg[2]
        })

    return jsonify(mensagens)

# USUÁRIOS ONLINE
@app.route("/usuarios_online")
def usuarios_online():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT nome
    FROM usuarios
    WHERE online=1
    """)

    usuarios = cursor.fetchall()

    conexao.close()

    lista = []

    for u in usuarios:
        lista.append(u[0])

    return jsonify(lista)

# LOGOUT
@app.route("/logout")
def logout():

    if "usuario" in session:

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
        UPDATE usuarios
        SET online=0
        WHERE nome=?
        """, (session["usuario"],))

        conexao.commit()
        conexao.close()

    session.clear()

    return redirect("/")

# LIMPAR CONVERSA PÚBLICA
@app.route("/limpar_chat")
def limpar_chat():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    DELETE FROM mensagens
    """)

    conexao.commit()
    conexao.close()

    return redirect("/chat")

# ═══════════════════════════════════════════════════════════════════════════
# CONVERSAS PRIVADAS - NOVOS ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

# INTERFACE DE CONVERSAS PRIVADAS
@app.route("/chat_privado")
def chat_privado():

    if "usuario" not in session:
        return redirect("/login")

    return render_template(
        "chat_privado.html",
        usuario=session["usuario"]
    )

# LISTAR CONVERSAS ATIVAS DO USUÁRIO
@app.route("/conversas_ativas")
def conversas_ativas():

    if "usuario" not in session:
        return redirect("/login")

    usuario_atual = session["usuario"]
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT c.id, 
           CASE 
               WHEN c.usuario1 = ? THEN c.usuario2
               ELSE c.usuario1
           END as outro_usuario,
           c.criada_em
    FROM conversas_privadas c
    WHERE c.usuario1 = ? OR c.usuario2 = ?
    ORDER BY c.criada_em DESC
    """, (usuario_atual, usuario_atual, usuario_atual))

    conversas = cursor.fetchall()
    conexao.close()

    lista = []
    for conv in conversas:
        lista.append({
            "id": conv[0],
            "outro_usuario": conv[1],
            "criada_em": conv[2]
        })

    return jsonify(lista)

# LISTAR USUÁRIOS DISPONÍVEIS PARA CONVERSA
@app.route("/usuarios_disponiveis")
def usuarios_disponiveis():

    if "usuario" not in session:
        return redirect("/login")

    usuario_atual = session["usuario"]
    conexao = conectar()
    cursor = conexao.cursor()

    # Buscar todos os usuários exceto o atual
    cursor.execute("""
    SELECT nome FROM usuarios
    WHERE nome != ?
    ORDER BY nome ASC
    """, (usuario_atual,))

    usuarios = cursor.fetchall()
    conexao.close()

    lista = [u[0] for u in usuarios]
    return jsonify(lista)

# INICIAR CONVERSA PRIVADA
@app.route("/iniciar_conversa/<outro_usuario>")
def iniciar_conversa(outro_usuario):

    if "usuario" not in session:
        return redirect("/login")

    usuario_atual = session["usuario"]
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        # Verificar se o outro usuário existe
        cursor.execute("SELECT id FROM usuarios WHERE nome = ?", (outro_usuario,))
        if not cursor.fetchone():
            conexao.close()
            return "Usuário não encontrado", 404

        # Verificar ou criar conversa (ordem alfabética para evitar duplicatas)
        usuarios_ordenados = tuple(sorted([usuario_atual, outro_usuario]))
        
        cursor.execute("""
        SELECT id FROM conversas_privadas
        WHERE usuario1 = ? AND usuario2 = ?
        """, usuarios_ordenados)

        conversa = cursor.fetchone()

        if not conversa:
            # Criar nova conversa
            cursor.execute("""
            INSERT INTO conversas_privadas(usuario1, usuario2)
            VALUES (?, ?)
            """, usuarios_ordenados)
            conexao.commit()
            conversa_id = cursor.lastrowid
        else:
            conversa_id = conversa[0]

        conexao.close()
        return redirect(f"/conversa/{conversa_id}")

    except Exception as e:
        conexao.close()
        return f"Erro ao iniciar conversa: {str(e)}", 500

# ABRIR CONVERSA PRIVADA ESPECÍFICA
@app.route("/conversa/<int:conversa_id>")
def conversa(conversa_id):

    if "usuario" not in session:
        return redirect("/login")

    usuario_atual = session["usuario"]
    conexao = conectar()
    cursor = conexao.cursor()

    # Verificar se o usuário pertence a esta conversa
    cursor.execute("""
    SELECT usuario1, usuario2 FROM conversas_privadas
    WHERE id = ?
    """, (conversa_id,))

    conv = cursor.fetchone()

    if not conv:
        conexao.close()
        return "Conversa não encontrada", 404

    if conv[0] != usuario_atual and conv[1] != usuario_atual:
        conexao.close()
        return "Acesso negado", 403

    # Determinar o outro usuário
    outro_usuario = conv[1] if conv[0] == usuario_atual else conv[0]

    conexao.close()

    return render_template(
        "conversa_privada.html",
        usuario=usuario_atual,
        outro_usuario=outro_usuario,
        conversa_id=conversa_id
    )

# BUSCAR MENSAGENS PRIVADAS DE UMA CONVERSA
@app.route("/mensagens_privadas/<int:conversa_id>")
def mensagens_privadas(conversa_id):

    if "usuario" not in session:
        return redirect("/login")

    usuario_atual = session["usuario"]
    conexao = conectar()
    cursor = conexao.cursor()

    # Verificar se o usuário pertence a esta conversa
    cursor.execute("""
    SELECT usuario1, usuario2 FROM conversas_privadas
    WHERE id = ?
    """, (conversa_id,))

    conv = cursor.fetchone()

    if not conv or (conv[0] != usuario_atual and conv[1] != usuario_atual):
        conexao.close()
        return jsonify([])

    # Buscar mensagens
    cursor.execute("""
    SELECT remetente, conteudo, horario
    FROM mensagens_privadas
    WHERE conversa_id = ?
    ORDER BY id ASC
    """, (conversa_id,))

    dados = cursor.fetchall()
    conexao.close()

    mensagens = []
    for msg in dados:
        mensagens.append({
            "remetente": msg[0],
            "conteudo": msg[1],
            "horario": msg[2]
        })

    return jsonify(mensagens)

# ENVIAR MENSAGEM PRIVADA
@app.route("/enviar_privada", methods=["POST"])
def enviar_privada():

    if "usuario" not in session:
        return redirect("/login")

    try:
        conversa_id = int(request.form.get("conversa_id", 0))
        conteudo = request.form.get("conteudo", "").strip()

        if not conteudo:
            return "Mensagem vazia", 400

        usuario_atual = session["usuario"]
        conexao = conectar()
        cursor = conexao.cursor()

        # Verificar se o usuário pertence a esta conversa
        cursor.execute("""
        SELECT usuario1, usuario2 FROM conversas_privadas
        WHERE id = ?
        """, (conversa_id,))

        conv = cursor.fetchone()

        if not conv or (conv[0] != usuario_atual and conv[1] != usuario_atual):
            conexao.close()
            return "Acesso negado", 403

        # Inserir mensagem
        horario = datetime.now().strftime("%H:%M")
        cursor.execute("""
        INSERT INTO mensagens_privadas(conversa_id, remetente, conteudo, horario)
        VALUES (?, ?, ?, ?)
        """, (conversa_id, usuario_atual, conteudo, horario))

        conexao.commit()
        conexao.close()

        return "OK"

    except Exception as e:
        return f"Erro ao enviar mensagem: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)