#!/bin/bash

echo "=============================="
echo "Instalador - Sistema de Estoque"
echo "=============================="

# 1. Criação de ambiente virtual
echo "Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# 2. Instalação de dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# 3. Criação do banco e usuário admin
echo "Inicializando banco e criando admin..."
python criar_admin.py

# 4. Rodar a aplicação
echo "Inicializando servidor Flask..."
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
