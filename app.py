from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__)

produtos = []

@app.route('/')

def home():
    return render_template('home.html', produtos=produtos)

@app.route('/estoque', methods=['GET', 'POST'])

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

        produto = {
            'id' : len(produtos)+1,
            'nome' : nome,
            'marca' : marca,
            'v_u' : v_u,
            'quantidade' : quantidade,
            'total' : total
        }

        produtos.append(produto)

        return redirect(url_for('home'))
    return render_template('estoque.html')

@app.route('/baixa', methods=['GET', 'POST'])
def baixa():
    if request.method == 'POST':
        ids = request.form.getlist('produtos_selecionados')

        for produto_id_str in ids:
            produto_id = int(produto_id_str)
            quantidade_baixa_str = request.form.get(f'quantidade_{produto_id}')
            if quantidade_baixa_str:
                quantidade_baixa = int(quantidade_baixa_str)

                for produto in produtos[:]:  # copia da lista para poder remover com segurança
                    if produto['id'] == produto_id:
                        if 0 < quantidade_baixa <= produto['quantidade']:
                            produto['quantidade'] -= quantidade_baixa
                            produto['total'] = produto['quantidade'] * produto['v_u']
                            if produto['quantidade'] == 0:
                                produtos.remove(produto)
                        break


            return redirect(url_for('home'))
    
    return render_template('baixa.html', produtos=produtos)

if __name__ == '__main__':
    app.run(debug=True)