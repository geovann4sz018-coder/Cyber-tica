from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import hashlib # Nova biblioteca para simular hashes de senhas

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Chave secreta para sessões seguras

# Banco de dados simulado (em memória para simplicidade)
# Em um projeto real, usaríamos um banco de dados como SQLite ou PostgreSQL
usuarios_db = {
    "admin": {
        "senha_hash": generate_password_hash("123456"), # Senha segura!
        "nome": "Administrador do Sistema",
        "email": "admin@exemplo.com",
        "dados_coletados": [
            "Endereço IP de acesso", 
            "Tipo de navegador e sistema operacional", 
            "Horário e data de login"
        ],
        "finalidade": "Garantir a segurança da conta, prevenir fraudes e realizar auditorias de acesso."
    }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        
        user = usuarios_db.get(usuario)
        if user and check_password_hash(user["senha_hash"], senha):
            session["usuario"] = usuario
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Usuário ou senha incorretos.", "danger")
            
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))
    
    user_info = usuarios_db[session["usuario"]]
    return render_template("dashboard.html", user=user_info)

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Você foi desconectado.", "info")
    return redirect(url_for("index"))

# NOVA ROTA: Simulador de Vulnerabilidade de Senhas
@app.route("/simulador_vulnerabilidade", methods=["GET", "POST"])
def simulador_vulnerabilidade():
    senha_digitada = ""
    hash_md5 = ""
    hash_sha256 = ""
    
    if request.method == "POST":
        senha_digitada = request.form.get("senha_simulador")
        if senha_digitada:
            # Simulação de hash fraco (MD5) - NÃO USAR EM PRODUÇÃO!
            hash_md5 = hashlib.md5(senha_digitada.encode()).hexdigest()
            # Simulação de hash mais forte (SHA256) - Melhor, mas ainda não ideal para senhas
            hash_sha256 = hashlib.sha256(senha_digitada.encode()).hexdigest()
            
    return render_template("simulador_vulnerabilidade.html", 
                           senha_digitada=senha_digitada, 
                           hash_md5=hash_md5, 
                           hash_sha256=hash_sha256)

if __name__ == "__main__":
    # Em um ambiente de produção, use um servidor WSGI como Gunicorn ou uWSGI
    # O modo debug NUNCA deve ser usado em produção
    app.run(host="0.0.0.0", port=5000, debug=False)
