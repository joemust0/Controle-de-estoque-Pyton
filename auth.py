from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()
login_manager = LoginManager()

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(80), unique=True, nullable=False)
    
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))