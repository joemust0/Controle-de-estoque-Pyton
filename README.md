# Sistema de Controle de Estoque

## Tecnologias
- Python
- Flask
- Flask-Login
- SQLite (ou PostgreSQL)
- HTML / CSS

## Funcionalidades
- Login com sessão de usuário
- Cadastro de produtos
- Edição de estoque (entrada/saída)
- Cadastro de usuários (apenas admin)
- Criptografia de senha
- Alerta de produtos com estoque baixo

## Perfis de Usuário
- Administrador: acesso total
- Comum: visualização e movimentação de estoque

## Execução
1. Crie um ambiente virtual
2. Instale dependências: `pip install -r requirements.txt`
3. Rode o app: `flask run`