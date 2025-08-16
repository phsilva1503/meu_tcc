# routes/main.py
from flask import Blueprint, render_template

# Cria um Blueprint chamado 'main' para as rotas principais
bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """Rota para a página inicial."""
    # Renderiza o template 'index.html'
    return render_template('index.html')

# ---  ROTAS ADICIONADAS ---
@bp.route('/controle-producao')
def controle_producao():
    """Rota para a página de controle de produção."""
    # Renderiza o template 'controle-producao.html'
    return render_template('controle-producao.html')

@bp.route('/laudo-tecnico')
def laudo_tecnico():
    """Rota para a página de laudo técnico."""
    # Renderiza o template 'laudo-tecnico.html'
    return render_template('laudo-tecnico.html')
@bp.route('/lean')
def lean():
    """Rota para a página de Lean Six Sigma."""
    # Renderiza o template 'lean.html'
    return render_template('lean.html')
# --- posso implementar NOVAS ROTAS ---