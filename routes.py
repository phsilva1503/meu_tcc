from flask import render_template, request, redirect, flash, url_for
from models import *
from datetime import date, datetime
from sqlalchemy import func, case


def routes(app):

    # -----------------------
    # Helper: obter ou criar registro de estoque (não faz commit)
    # -----------------------
    def get_or_create_estoque(componente_id):
        estoque = Estoque.query.filter_by(componente_id=componente_id).first()
        if not estoque:
            estoque = Estoque(componente_id=componente_id, quantidade=0)
            db.session.add(estoque)
            db.session.flush()
        return estoque

    # -----------------------
    # Inicializa componentes pré-cadastrados (uma única vez)
    # -----------------------
    def inicializar_componentes():
        componentes_iniciais = ["COMPO A", "COMPO B", "COMPO C"]
        for nome in componentes_iniciais:
            if not Componente.query.filter_by(nome=nome).first():
                novo = Componente(nome=nome, ativo=True)
                db.session.add(novo)
                db.session.flush()
                db.session.add(Estoque(componente_id=novo.id, quantidade=0))
        db.session.commit()

    with app.app_context():
        inicializar_componentes()

    # -----------------------
    # Função auxiliar: recalcular saldos
    # -----------------------
    def atualizar_saldos():
        saldos_query = (
            db.session.query(
                Movimentacao.componente_id,
                func.sum(
                    case(
                        (Movimentacao.tipo == 'entrada', Movimentacao.quantidade),
                        (Movimentacao.tipo == 'saida', -Movimentacao.quantidade),
                        else_=0
                    )
                ).label('saldo')
            )
            .group_by(Movimentacao.componente_id)
            .all()
        )

        for componente_id, saldo in saldos_query:
            estoque = Estoque.query.filter_by(componente_id=componente_id).first()
            if estoque:
                estoque.quantidade = saldo
            else:
                db.session.add(Estoque(componente_id=componente_id, quantidade=saldo))

        db.session.commit()

    # -----------------------
    # Rota inicial
    # -----------------------
    @app.route('/')
    def index():
        return render_template('index-main.html')

    # -----------------------
    # Cadastro de Componentes
    # -----------------------
    @app.route('/cadastro', methods=['GET', 'POST'], endpoint='cadastro_componente')
    def cadastro_componente():
        todos_componentes = Componente.query.all()
        estoques = Estoque.query.all()
        saldos = {e.componente_id: e.quantidade for e in estoques}

        if request.method == 'POST':
            nome = request.form.get('nome')
            if not nome:
                flash("Informe o nome do componente!", "danger")
                return redirect(url_for('cadastro_componente'))

            if Componente.query.filter_by(nome=nome).first():
                flash(f"Componente '{nome}' já existe!", "warning")
                return redirect(url_for('cadastro_componente'))

            novo = Componente(nome=nome, ativo=True)
            db.session.add(novo)
            db.session.flush()
            db.session.add(Estoque(componente_id=novo.id, quantidade=0))
            db.session.commit()

            flash(f"Componente '{nome}' cadastrado com sucesso!", "success")
            return redirect(url_for('cadastro_componente'))

        return render_template('CadastroComponente.html',
                               todos_componentes=todos_componentes,
                               saldos=saldos)

    # -----------------------
    # Ajuste de Estoque
    # -----------------------
    @app.route("/estoque/ajustar/componente/<int:componente_id>", methods=["GET", "POST"])
    def ajustar_estoque(componente_id):
        componente = Componente.query.get_or_404(componente_id)
        estoque = Estoque.query.filter_by(componente_id=componente.id).first()

        if request.method == "POST":
            try:
                quantidade = float(request.form.get("quantidade", 0))
                tipo = request.form.get("tipo")

                if quantidade <= 0 or tipo not in ["entrada", "saida"]:
                    flash("Informe uma quantidade válida e um tipo de ajuste!", "danger")
                    return redirect(url_for("ajustar_estoque", componente_id=componente.id))

                if not estoque:
                    estoque = Estoque(componente_id=componente.id, quantidade=0)
                    db.session.add(estoque)
                    db.session.flush()

                if tipo == "entrada":
                    estoque.quantidade += quantidade
                else:
                    if estoque.quantidade < quantidade:
                        flash("Saldo insuficiente para saída!", "danger")
                        return redirect(url_for("ajustar_estoque", componente_id=componente.id))
                    estoque.quantidade -= quantidade

                mov = Movimentacao(
                    componente_id=componente.id,
                    quantidade=quantidade,
                    tipo=tipo,
                    data=date.today()
                )
                db.session.add(mov)
                db.session.commit()

                flash(f"{quantidade} unidades {'adicionadas' if tipo=='entrada' else 'retiradas'} do estoque de '{componente.nome}'", "success")
                return redirect(url_for("cadastro_componente"))
            except ValueError:
                flash("Quantidade inválida!", "danger")
                return redirect(url_for("ajustar_estoque", componente_id=componente.id))

        return render_template("AjusteEstoque.html", componente=componente, estoque=estoque)

    # -----------------------
    # Visualizar Movimentações
    # -----------------------
    @app.route("/movimentacoes/<int:componente_id>")
    def movimentacoes(componente_id):
        componente = Componente.query.get_or_404(componente_id)
        movimentacoes = Movimentacao.query.filter_by(componente_id=componente.id).order_by(Movimentacao.id.desc()).all()
        return render_template("movimentacoes.html", componente=componente, movimentacoes=movimentacoes)

    # -----------------------
    # Toggle Ativo/Inativo
    # -----------------------
    @app.route('/toggle_componente/<int:componente_id>')
    def toggle_componente(componente_id):
        componente = Componente.query.get_or_404(componente_id)
        componente.ativo = not componente.ativo
        db.session.commit()
        flash(f"Componente '{componente.nome}' agora está {'ativo' if componente.ativo else 'inativo'}.", "info")
        return redirect(url_for('cadastro_componente'))

    # -----------------------
    # Visualizar Estoque
    # -----------------------
    @app.route("/estoque")
    def ver_estoque():
        atualizar_saldos()
        componentes = Componente.query.all()
        estoques = Estoque.query.all()
        saldos = {e.componente_id: e.quantidade for e in estoques}
        return render_template("Estoque.html", componentes=componentes, saldos=saldos)

# -----------------------
# Controle de Produção
# -----------------------

    # -----------------------
    # Controle de Produção
    # -----------------------
    @app.route('/controle-producao')
    def controle_producao():
        ##producoes = Producao.query.all()
        producoes = Producao.query.order_by(Producao.id.desc()).all()
        componentes = Componente.query.filter_by(ativo=True).all()
        hoje = date.today().strftime('%Y-%m-%d')
        todos_componentes = Componente.query.all()
        return render_template('controle_producao.html',
                               producoes=producoes,
                               componentes=componentes,
                               hoje=hoje,
                               todos_componentes=todos_componentes)
    
# -----------------------
# Cadastro de Produção
    @app.route("/cadastro_producao")
    def mostrar_cadastro_producao():
        producoes = Producao.query.all()
        componentes = Componente.query.filter_by(ativo=True).all()
        hoje = date.today().strftime("%Y-%m-%d")
        return render_template(
            "controle_producao.html",
            producoes=producoes,
            componentes=componentes,
            hoje=hoje
        )

    # Rota POST: processa o formulário
    @app.route("/cadastro_producao", methods=["POST"])
    def cadastro_producao():
        try:
            producao_id = request.form['producao_id']
            data_producao = request.form.get('data_producao') or date.today().strftime('%Y-%m-%d')
            tipo_espuma = request.form['tipo_espuma']
            densidade_real = float(request.form['densidade_real'])
            altura = float(request.form.get('altura', 0))
            conformidade = request.form['conformidade']
            observacoes = request.form.get('observacoes', '')

            data_producao = datetime.strptime(data_producao, "%Y-%m-%d").date()

            # Verifica duplicidade
            if Producao.query.filter_by(producao_id=producao_id).first():
                flash(f"Número de bloco '{producao_id}' já cadastrado!", "danger")
                return redirect(url_for("mostrar_cadastro_producao"))

            nova_producao = Producao(
                producao_id=producao_id,
                data_producao=data_producao,
                tipo_espuma=tipo_espuma,
                densidade_real=densidade_real,
                altura=altura,
                conformidade=conformidade,
                observacoes=observacoes
            )
            db.session.add(nova_producao)
            db.session.flush()  # pega o id antes de commit

            # Componentes usados na produção
            for componente in Componente.query.filter_by(ativo=True).all():
                campo_nome = f"componente_{componente.id}"
                if campo_nome in request.form:
                    quantidade = float(request.form[campo_nome])
                    if quantidade > 0:
                        estoque = Estoque.query.filter_by(componente_id=componente.id).first()
                        if not estoque or estoque.quantidade < quantidade:
                            db.session.rollback()
                            flash(f"Saldo insuficiente do componente '{componente.nome}'", "danger")
                            return redirect(url_for("mostrar_cadastro_producao"))

                        cp = ComponenteProducao(
                            producao_id=nova_producao.id,
                            componente_id=componente.id,
                            quantidade_usada=quantidade
                        )
                        db.session.add(cp)
                        estoque.quantidade -= quantidade

                        nova_movimentacao = Movimentacao(
                        componente_id=componente.id,
                        data=datetime.now(),
                        tipo="SAÍDA",
                        quantidade=quantidade,
                        producao_id=nova_producao.id  # <-- vincula à produção
                        )
                        db.session.add(nova_movimentacao)

            db.session.commit()
            flash("Produção cadastrada com sucesso!", "success")
            return redirect(url_for("mostrar_cadastro_producao"))

        except (KeyError, ValueError) as e:
            db.session.rollback()
            flash(f"Erro ao cadastrar produção: {str(e)}", "danger")
            return redirect(url_for("mostrar_cadastro_producao"))



    # -----------------------
    # Visualizar Componentes de uma Produção
    # -----------------------
    @app.route('/ComponentesProducao/<int:producao_id>')
    def ver_componentes_producao(producao_id):
        producao = Producao.query.get_or_404(producao_id)
        componentes = ComponenteProducao.query.filter_by(producao_id=producao_id).all()
        return render_template('ComponentesProducao.html', producao=producao, componentes=componentes)

    # -----------------------
    # Páginas estáticas
    # -----------------------
    @app.route('/laudo-tecnico')
    def laudo_tecnico():
        return render_template('laudo_tecnico.html')

    @app.route('/lean-six-sigma')
    def lean_six_sigma():
        return render_template('lean_six_sigma.html')

    @app.route('/analise_preditiva')
    def analise_preditiva():
        return render_template('analise_preditiva.html')

    @app.route('/dashboard')
    def dashboard():
         # Pega todas as produções, do mais recente para o mais antigo
        producoes = Producao.query.order_by(Producao.id.desc()).all()
    
    # Também pode pegar componentes ativos, se quiser mostrar info extra
        componentes = Componente.query.filter_by(ativo=True).all()
    
    # Passa os dados para o template
        return render_template(
        'Dash.html',
        producoes=producoes,
        componentes=componentes
        )
        return render_template('Dash.html')

    @app.route('/relatorios')
    def relatorios():
        return render_template('relatorios.html')
