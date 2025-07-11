# routes.py
from flask import render_template, request, redirect, url_for
from models import Produto
from auth import db
from flask_login import login_required
from flask import Blueprint
from usuarios import usuarios_bp

def init_routes(app):
    app.register_blueprint(usuarios_bp)

def init_routes(app):
    @app.route('/')
    @login_required
    def home():
        produtos = Produto.query.all()
        return render_template('home.html', produtos=produtos)

    @app.route('/estoque', methods=['GET', 'POST'])
    @login_required
    def estoque():
        if request.method == 'POST':
            nomes = request.form.getlist('nome[]')
            marcas = request.form.getlist('marca[]')
            valores = request.form.getlist('v_u[]')
            quantidades = request.form.getlist('quantidade[]')

            for i in range(len(nomes)):
                nome = nomes[i]
                marca = marcas[i]
                v_u_str = valores[i].replace('.', '').replace(',', '.')
                v_u = float(v_u_str)
                quantidade = int(quantidades[i])
                total = v_u * quantidade

                produto = Produto(nome=nome, marca=marca, v_u=v_u, quantidade=quantidade, total=total)
                db.session.add(produto)

            db.session.commit()
            return redirect(url_for('home'))

        return render_template('estoque.html')

    @app.route('/baixa', methods=['GET', 'POST'])
    @login_required
    def baixa():
        produtos = Produto.query.all()

        if request.method == 'POST':
            ids = request.form.getlist('produtos_selecionados')

            for produto_id_str in ids:
                produto_id = int(produto_id_str)
                quant_baixa_str = request.form.get(f'quantidade_{produto_id}')
                if quant_baixa_str:
                    quant_baixa = int(quant_baixa_str)
                    produto = Produto.query.get(produto_id)
                    if produto and 0 < quant_baixa <= produto.quantidade:
                        produto.quantidade -= quant_baixa
                        produto.total = produto.v_u * produto.quantidade
                        if produto.quantidade == 0:
                            db.session.delete(produto)
                    db.session.commit()

            return redirect(url_for('home'))

        return render_template('baixa.html', produtos=produtos)
