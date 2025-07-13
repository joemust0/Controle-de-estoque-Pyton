from flask_login import UserMixin
from datetime import datetime
from auth import db  # ✅ tudo certo aqui

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def get_id(self):
        return str(self.id)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    v_u = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)

    movimentacoes = db.relationship('Movimentacao', backref='produto', lazy=True)

class Movimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    usuario = db.relationship('Usuario', backref='movimentacoes')
