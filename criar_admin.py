from app import app, db
from auth import Usuario

def criar_usuario_admin():
    with app.app_context():
        db.create_all()

        # Verifica se o admin já existe
        if not Usuario.query.filter_by(usuario='admin').first():
            admin = Usuario(usuario='admin', senha='1234')
            db.session.add(admin)
            db.session.commit()
            print("Usuário admin criado com sucesso!")
        else:
            print("Usuário admin já existe.")

if __name__ == "__main__":
    criar_usuario_admin()
