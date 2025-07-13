from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import check_password_hash
import os
from auth import db, login_manager
from models import Usuario
from routes import init_routes

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
    return Usuario.query.get(int(user_id))

# ✅ Criação do banco e admin no contexto correto
with app.app_context():
    db.create_all()
    if not Usuario.query.filter_by(usuario='admin').first():
        admin = Usuario(usuario='admin', is_admin=True)
        admin.set_senha('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Banco e usuário admin criados com sucesso!')
    else:
        print('Banco já existe. Usuário admin já cadastrado.')

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
    return redirect(url_for('login'))

# Importa rotas principais
init_routes(app)

# Roda o servidor
if __name__ == '__main__':
    app.run(debug=True)
