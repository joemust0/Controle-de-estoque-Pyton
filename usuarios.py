from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import Usuario
from auth import db

usuarios_bp = Blueprint('usuarios_bp', __name__)

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Acesso restrito ao administrador.')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

@usuarios_bp.route('/usuarios', methods=['GET', 'POST'])
@login_required
@admin_required
def usuarios():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        admin = 'admin' in request.form

        if Usuario.query.filter_by(usuario=usuario).first():
            flash('Usuário já existe.')
        else:
            novo = Usuario(usuario=usuario, senha=senha, is_admin=admin)
            db.session.add(novo)
            db.session.commit()
            flash('Usuário criado com sucesso.')

    lista = Usuario.query.all()
    return render_template('usuarios.html', usuarios=lista)

@usuarios_bp.route('/usuarios/excluir/<int:id>')
@login_required
@admin_required
def excluir_usuario(id):
    if current_user.id == id:
        flash("Você não pode se excluir.")
        return redirect(url_for('usuarios_bp.usuarios'))
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuário excluído.')
    return redirect(url_for('usuarios_bp.usuarios'))
