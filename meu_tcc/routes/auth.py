# routes/auth.py (já fornecida anteriormente)
# Certifique-se de que este arquivo está criado conforme mostrado antes.
# Ele contém as rotas para /auth/login, /auth/logout, /auth/registrar.
# routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from models.usuario import Usuario
from app import db

# Cria um Blueprint chamado 'auth' para as rotas de autenticação.
# A variável é chamada 'bp', que é o nome esperado no app.py pela linha:
# from routes.auth import bp as auth_bp
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Rota para a página de login."""
    # Se o usuário já estiver logado, redireciona para a página inicial
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        # Obtém os dados do formulário de login
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = True if request.form.get('remember') else False

        # Busca o usuário no banco de dados pelo email
        user = Usuario.query.filter_by(email=email).first()

        # Verifica se o usuário existe e se a senha está correta
        if user and user.check_password(password):
            # Faz o login do usuário
            login_user(user, remember=remember_me)
            # Obtém a próxima página (se houver) para redirecionar após o login
            next_page = request.args.get('next')
            # Redireciona para a próxima página ou para a página inicial
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            # Mostra uma mensagem de erro se o login falhar
            flash('Login inválido. Verifique seu email e senha.')

    # Renderiza o template de login para requisições GET ou se o login falhar
    return render_template('login.html')

@bp.route('/logout')
@login_required # Requer que o usuário esteja logado para acessar esta rota
def logout():
    """Rota para logout."""
    # Faz o logout do usuário
    logout_user()
    # Redireciona para a página inicial
    return redirect(url_for('main.index'))

@bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    """Rota para a página de registro."""
    # Se o usuário já estiver logado, redireciona para a página inicial
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        # Obtém os dados do formulário de registro
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Verifica se o nome de usuário ou email já existem
        user_by_email = Usuario.query.filter_by(email=email).first()
        user_by_username = Usuario.query.filter_by(username=username).first()

        if user_by_email:
            flash('Email já cadastrado.')
            return render_template('registrar.html') # Ou redirect(url_for('auth.registrar'))
        if user_by_username:
            flash('Nome de usuário já cadastrado.')
            return render_template('registrar.html') # Ou redirect(url_for('auth.registrar'))

        # Cria um novo usuário
        new_user = Usuario(username=username, email=email)
        # Define a senha (gera o hash)
        new_user.set_password(password)

        # Adiciona o novo usuário à sessão do banco de dados
        db.session.add(new_user)
        # Confirma a transação no banco de dados
        db.session.commit()

        # Mostra uma mensagem de sucesso
        flash('Conta criada com sucesso! Agora você pode fazer login.')
        # Redireciona para a página de login
        return redirect(url_for('auth.login'))

    # Renderiza o template de registro para requisições GET ou se o registro falhar
    return render_template('registrar.html')
