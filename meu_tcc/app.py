# app.py
from flask import Flask
# Importe SQLAlchemy e LoginManager no topo
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# Importe sua classe de configuração
from config import Config



# --- CRIA A INSTÂNCIA DO DB AQUI, FORA DA FUNÇÃO ---
# Esta é a mudança principal para evitar a importação circular entre app.py e models/
# db é criado no escopo global deste módulo, mas só é inicializado com um app Flask dentro de create_app.
db = SQLAlchemy()
# --- FIM DA CRIAÇÃO ---

# Cria a instância do LoginManager
login_manager = LoginManager()
# Define a view de login (certifique-se de que o endpoint 'auth.login' existe nos seus blueprints)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

def create_app(config_class=Config):
    """Fábrica de aplicação para configurar o app Flask."""
    # Cria a instância do app Flask
    app = Flask(__name__)
    
    # Carrega as configurações da classe Config
    app.config.from_object(config_class)
    # Se quiser manter TEMPLATES_AUTO_RELOAD, mova para sua Config.py ou adicione aqui:
    # app.config['TEMPLATES_AUTO_RELOAD'] = True 

    # Inicializa as extensões com o app criado
    db.init_app(app) # Associa a instância db criada globalmente com este app específico
    login_manager.init_app(app) # Associa o LoginManager com este app

    # --- REGISTRA OS BLUEPRINTS ---
    # Certifique-se de que os arquivos routes/... existem e definem 'bp'
    try:
        from routes.main import bp as main_bp
        app.register_blueprint(main_bp)
    except ImportError as e:
        app.logger.error(f"Erro ao importar routes.main: {e}") # Usa o logger do app

    try:
        from routes.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
    except ImportError as e:
        app.logger.error(f"Erro ao importar routes.auth: {e}")

    try:
        from routes.producao import bp as producao_bp
        app.register_blueprint(producao_bp, url_prefix='/producao')
    except ImportError as e:
         app.logger.warning(f"Aviso: Blueprint routes.producao não encontrado ou erro na importação: {e}. Continuando sem ele.")
    try:
        from routes.lean import bp as lean_bp
        app.register_blueprint(lean_bp)
    except ImportError as e:
        app.logger.error(f"Erro ao importar routes.lean: {e}")

    # --- FIM DO REGISTRO DOS BLUEPRINTS ---

    # --- GARANTE QUE OS MODELOS ESTÃO CARREGADOS ANTES DE CRIAR AS TABELAS ---
    # Importar os modelos aqui garante que eles sejam lidos e registrem suas tabelas com o 'db'
    # antes de db.create_all() ser chamado. Isso é crucial.
    from models import usuario, bloco, produto_usado, estoque
    # Nota: Certifique-se de que cada um desses arquivos models/... existe e define suas classes de modelo.
    # Se algum modelo estiver faltando, você receberá um ImportError aqui, o que é útil para depuração.
    
    # Cria as tabelas do banco de dados
    with app.app_context():
        # Agora, como os modelos foram importados, db.create_all() conhece todas as tabelas definidas.
        db.create_all()
    # --- FIM DA CRIAÇÃO DAS TABELAS ---

    return app

# --- FUNÇÃO PARA CARREGAR O USUÁRIO LOGADO ---
# Esta função é usada pelo Flask-Login para recarregar um usuário a partir do ID armazenado na sessão.
@login_manager.user_loader
def load_user(user_id):
    # Importação dentro da função para evitar importação circular no nível do módulo
    # e garantir que ocorre somente quando necessário (durante uma requisição que envolve login).
    # Como 'db' foi inicializado com o app em create_app(), ele está pronto para uso aqui.
    try:
        from models.usuario import Usuario # Importa o modelo Usuario
        return Usuario.query.get(int(user_id)) # Retorna o objeto Usuario ou None se não encontrado
    except Exception as e:
        # Em produção, registre o erro em um sistema de logging
        print(f"[ERRO] Erro em load_user ao carregar usuário ID {user_id}: {e}")
        return None # Retorna None se houver qualquer erro
# --- FIM DA FUNÇÃO DE CARREGAMENTO DE USUÁRIO ---

# Ponto de entrada para o servidor de desenvolvimento
if __name__ == '__main__':
    # Cria a aplicação usando a função fábrica
    app = create_app()
    # Inicia o servidor de desenvolvimento do Flask
    # debug=True é útil para desenvolvimento, mas deve ser False em produção
    app.run(debug=True)


