from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask import Blueprint
from models import Produto, Usuario, Movimentacao
from auth import db
from usuarios import usuarios_bp, admin_required

def init_routes(app):
    app.register_blueprint(usuarios_bp)

    @app.route('/', methods=['GET'])
    @login_required
    def home():
        termo = request.args.get('query') or ''
        if termo:
            produtos = Produto.query.filter(
                (Produto.nome.ilike(f'%{termo}%')) |
                (Produto.marca.ilike(f'%{termo}%'))
            ).all()
        else:
            produtos = Produto.query.all()

        return render_template('home.html', produtos=produtos, termo=termo)

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

    @app.route('/produto/movimentar/<int:produto_id>', methods=['GET', 'POST'])
    @login_required
    def movimentar_produto(produto_id):
        produto = Produto.query.get_or_404(produto_id)

        if request.method == 'POST':
            tipo = request.form.get('tipo')  # entrada ou saida
            quantidade = int(request.form.get('quantidade'))

            if tipo == 'saida' and quantidade > produto.quantidade:
                flash("Estoque insuficiente para saída.")
                return redirect(url_for('movimentar_produto', produto_id=produto_id))

            if tipo == 'entrada':
                produto.quantidade += quantidade
            else:
                produto.quantidade -= quantidade

            produto.total = produto.v_u * produto.quantidade

            mov = Movimentacao(
                tipo=tipo,
                quantidade=quantidade,
                produto=produto,
                usuario_id=current_user.id
            )

            db.session.add(mov)
            db.session.commit()
            flash("Movimentação realizada com sucesso.")
            return redirect(url_for('home'))

        return render_template('movimentar_produto.html', produto=produto)

    @app.route('/produto/<int:produto_id>/historico')
    @login_required
    def historico_produto(produto_id):
        produto = Produto.query.get_or_404(produto_id)
        historico = Movimentacao.query.filter_by(produto_id=produto_id).order_by(Movimentacao.data.desc()).all()

        return render_template('historico_produto.html', produto=produto, historico=historico)

    @app.route('/movimentacoes')
    @login_required
    @admin_required
    def movimentacoes():
        movimentacoes = Movimentacao.query.order_by(Movimentacao.data.desc()).all()
        return render_template('movimentacoes.html', movimentacoes=movimentacoes)
