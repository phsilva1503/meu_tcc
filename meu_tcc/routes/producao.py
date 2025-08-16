# routes/producao.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
# Importa funcionalidades do Flask-Login
from flask_login import login_required, current_user
# Importa os modelos
from models.bloco import Bloco
from models.produto_usado import ProdutoUsado
from models.estoque import Estoque
from app import db
from datetime import datetime

bp = Blueprint('producao', __name__)

# --- Rotas que retornam páginas HTML ---
# (Se você quiser que /controle-producao seja gerenciada aqui também)
# @bp.route('/controle-producao')
# @login_required # Exemplo: requer login
# def controle_producao():
#     return render_template('controle-producao.html')

# --- Rotas da API (para AJAX do frontend) ---

@bp.route('/api/blocos', methods=['GET'])
@login_required
def get_blocos():
    """API: Obter lista de blocos (ex: para histórico)."""
    # Exemplo : pega os últimos 20 blocos
    blocos = Bloco.query.order_by(Bloco.data_producao.desc()).limit(20).all()
    blocos_data = []
    for bloco in blocos:
        blocos_data.append({
            'id': bloco.id,
            'bloco_id': bloco.bloco_id,
            'data_producao': bloco.data_producao.strftime('%Y-%m-%d'),
            'tipo_espuma': bloco.tipo_espuma,
            'densidade_real': bloco.densidade_real,
            'conformidade': bloco.conformidade
            # posso adicionar outros campos conforme necessário
        })
    return jsonify(blocos_data)

@bp.route('/api/estoque', methods=['GET'])
@login_required
def get_estoque():
    """API: Obter lista de estoque atual."""
    estoques = Estoque.query.all()
    estoque_data = []
    for item in estoques:
        estoque_data.append({
            'id': item.id,
            'nome_produto': item.nome_produto,
            'quantidade_estoque_kg': item.quantidade_estoque_kg,
            'estoque_minimo_kg': item.estoque_minimo_kg,
            'abaixo_do_minimo': item.abaixo_do_minimo()
        })
    return jsonify(estoque_data)

@bp.route('/api/blocos', methods=['POST'])
@login_required
def create_bloco():
    """API: Cadastrar um novo bloco."""
    try:
        data = request.get_json()

        # Validação básica
        bloco_id = data.get('bloco_id')
        if not bloco_id:
             return jsonify({'message': 'ID do Bloco é obrigatório.'}), 400

        # Verifica se o ID já existe
        if Bloco.query.filter_by(bloco_id=bloco_id).first():
             return jsonify({'message': 'ID do Bloco já cadastrado.'}), 400

        # Cria o novo bloco
        novo_bloco = Bloco(
            bloco_id=bloco_id,
            data_producao=datetime.strptime(data.get('data_producao'), '%Y-%m-%d').date() if data.get('data_producao') else datetime.today().date(),
            tipo_espuma=data.get('tipo_espuma'),
            densidade_real=float(data.get('densidade_real', 0)),
            conformidade=data.get('conformidade'),
            observacoes=data.get('observacoes', '')
        )

        db.session.add(novo_bloco)
        db.session.flush() # Para obter o ID do novo_bloco antes do commit

        # Processa os produtos quimicos usados
        produtos_usados_data = data.get('produtos_usados', {})
        for nome_produto, quantidade_str in produtos_usados_data.items():
            try:
                quantidade = float(quantidade_str) if quantidade_str else 0.0
                if quantidade > 0: # Só salva se a quantidade for > 0
                    produto_usado = ProdutoUsado(
                        nome_produto=nome_produto,
                        quantidade_usada_kg=quantidade,
                        bloco_id=novo_bloco.id
                    )
                    db.session.add(produto_usado)

                    # Atualiza o estoque 
                    item_estoque = Estoque.query.filter_by(nome_produto=nome_produto).first()
                    if item_estoque:
                        item_estoque.quantidade_estoque_kg -= quantidade
                    else:
                        # Se o item não existir no estoque, cria com quantidade negativa
                        # ou decide como tratar isso
                        novo_item_estoque = Estoque(
                            nome_produto=nome_produto,
                            quantidade_estoque_kg=-quantidade, # Começa negativo
                            estoque_minimo_kg=0 # Pode ser definido depois
                        )
                        db.session.add(novo_item_estoque)

            except ValueError:
                # Handle invalid quantity format if needed
                pass # Ou logar erro

        db.session.commit()
        return jsonify({'message': 'Bloco cadastrado com sucesso!', 'id': novo_bloco.id}), 201

    except Exception as e:
        db.session.rollback()
        # Em produção, logue o erro e retorne uma mensagem genérica
        print(f"Erro ao cadastrar bloco: {e}")
        return jsonify({'message': 'Erro interno ao cadastrar bloco.'}), 500

@bp.route('/api/estoque', methods=['PUT'])
@login_required
def update_estoque():
    """API: Atualizar estoque manualmente."""
    try:
        data = request.get_json()
        # Espera uma lista de itens para atualizar

        itens_atualizados = 0
        for item_data in data:
            item_id = item_data.get('id')
            estoque_item = Estoque.query.get(item_id)
            if estoque_item:
                estoque_item.quantidade_estoque_kg = float(item_data.get('quantidade_estoque_kg', estoque_item.quantidade_estoque_kg))
                estoque_item.estoque_minimo_kg = float(item_data.get('estoque_minimo_kg', estoque_item.estoque_minimo_kg))
                itens_atualizados += 1
            # Se item_id não existir, ignora ou loga

        db.session.commit()
        return jsonify({'message': f'{itens_atualizados} itens de estoque atualizados com sucesso!'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Erro ao atualizar estoque: {e}")
        return jsonify({'message': 'Erro interno ao atualizar estoque.'}), 500

# posso add mais rotas conforme necessário para outras funcionalidades
# posso gerar laudos (PDF), exportar para Excel, obter dados para gráficos, etc...
