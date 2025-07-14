from flask import Flask
from models import Usuario
from auth import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def inicializar_banco():
    with app.app_context():
        db.create_all()
        if not Usuario.query.filter_by(usuario='admin').first():
            admin = Usuario(usuario='admin', is_admin=True)
            admin.set_senha("admin1234")
            db.session.add(admin)
            db.session.commit()
            print("Usuário administrador criado com sucesso.")
        else:
            print("Usuário administrador já existe.")
