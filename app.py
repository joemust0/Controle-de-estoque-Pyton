from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import check_password_hash
import os

from auth import db, login_manager
from models import Usuario
from routes import init_routes
import criar_admin  # Importa o script responsável pela criação do admin

app = Flask(__name__)  
app.secret_key = 'chave-secreta'

# Configuração do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user = Usuario.query.get(int(user_id))
    if not user:
        logout_user()  # Encerra a sessão do usuário "fantasma"
    return user

# Executa a inicialização do banco e criação do admin
criar_admin.inicializar_banco()

# Rotas de login/logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        user = Usuario.query.filter_by(usuario=usuario).first()

        if user and user.verificar_senha(senha):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha inválidos')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear() 
    return redirect(url_for('login'))

# Importa rotas principais
init_routes(app)

# Roda o servidor
if __name__ == '__main__':
    app.run(debug=True)
