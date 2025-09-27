from flask import render_template, request, redirect, flash, url_for
from models import *
from datetime import date, datetime

def routes(app):

    # -----------------------
    # Inicializa componentes pré-cadastrados (uma única vez)
    # -----------------------
    def inicializar_componentes():
        componentes_iniciais = ["COMPO A", "COMPO B", "COMPO C"]
        for nome in componentes_iniciais:
            if not Componente.query.filter_by(nome=nome).first():
                db.session.add(Componente(nome=nome))
        db.session.commit()

    with app.app_context():
        inicializar_componentes()

    # -----------------------
    # Rota inicial
    # -----------------------
    @app.route('/')
    def index():
        return render_template('index-main.html')

    # -----------------------
    # Cadastro de Produção + Componentes
    # -----------------------
    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro_producao():
        todos_componentes = Componente.query.all()          # todos os componentes para lista
        componente_ativo = Componente.query.filter_by(ativo=True).all()  # apenas ativos para form
        producoes = Producao.query.all()
        hoje = date.today()

        if request.method == 'POST':
            producao_id = request.form.get('producao_id')

            # Verifica se já existe a produção
            if Producao.query.filter_by(producao_id=producao_id).first():
                flash(f"Erro: Produção ID '{producao_id}' já cadastrada!", "danger")
                return render_template(
                    'controle_producao.html',
                    componentes=componente_ativo,
                    todos_componentes=todos_componentes,
                    producoes=producoes,
                    hoje=hoje
                )

            # Converte a data
            data_str = request.form.get('data_producao')
            data_producao = datetime.strptime(data_str, '%Y-%m-%d').date() if data_str else hoje

            # Cria a produção
            producao = Producao(
                producao_id=producao_id,
                data_producao=data_producao,
                tipo_espuma=request.form.get('tipo_espuma'),
                densidade_real=float(request.form.get('densidade_real', 0)),
                altura=float(request.form.get('altura', 0)),
                conformidade=request.form.get('conformidade'),
                observacoes=request.form.get('observacoes', '')
            )
            db.session.add(producao)
            db.session.flush()  # garante que producao.id esteja disponível

            # Cria registros de ComponenteProducao apenas para ativos
            for comp in componente_ativo:
                qtd = float(request.form.get(f"componente_{comp.id}", 0))
                if qtd > 0:
                    comp_producao = ComponenteProducao(
                        producao_id=producao.id,
                        componente_id=comp.id,
                        quantidade_usada=qtd
                    )
                    db.session.add(comp_producao)

            db.session.commit()
            flash(f"Produção '{producao_id}' cadastrada com sucesso!", "success")

            producoes = Producao.query.all()
            return render_template(
                'controle_producao.html',
                componentes=componente_ativo,
                todos_componentes=todos_componentes,
                producoes=producoes,
                hoje=hoje
            )

        # GET: apenas renderiza a página
        return render_template(
            'controle_producao.html',
            componentes=componente_ativo,
            todos_componentes=todos_componentes,
            producoes=producoes,
            hoje=hoje
        )

    # -----------------------
    # Controle de Produção
    # -----------------------
    @app.route('/controle')
    def controle_producao():
        componentes = Componente.query.all()
        producoes = Producao.query.all()
        hoje = date.today()
        return render_template(
            'controle_producao.html',
            componentes=componentes,
            producoes=producoes,
            hoje=hoje
        )

    # -----------------------
    # Cadastro de Componentes
    # -----------------------
    @app.route("/cadastro_componente", methods=["GET", "POST"])
    def cadastro_componente():
        if request.method == "POST":
            nome = request.form.get("nome")
            if nome and not Componente.query.filter_by(nome=nome).first():
                db.session.add(Componente(nome=nome, ativo=True))
                db.session.commit()
                flash(f"Componente '{nome}' cadastrado com sucesso!", "success")
            else:
                flash("Componente já existe ou nome inválido!", "danger")
            return redirect(url_for("cadastro_componente"))

        todos_componentes = Componente.query.all()
        return render_template("CadastroComponente.html", todos_componentes=todos_componentes)
    


    @app.route('/toggle_componente/<int:componente_id>')
    def toggle_componente(componente_id):
        componente = Componente.query.get_or_404(componente_id)
        componente.ativo = not componente.ativo
        db.session.commit()
        flash(f"Componente '{componente.nome}' agora está {'ativo' if componente.ativo else 'inativo'}.", "info")
        return redirect(url_for('cadastro_componente'))

    # -----------------------
    # Componentes de uma produção
    # -----------------------
    @app.route('/ComponentesProducao/<int:producao_id>', methods=['POST', 'GET'])
    def ver_componentes_producao(producao_id):
        producao = Producao.query.get_or_404(producao_id)
        componentes = ComponenteProducao.query.filter_by(producao_id=producao_id).all()
        return render_template('ComponentesProducao.html', producao=producao, componentes=componentes)

    # -----------------------
    # Outras rotas existentes
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
        return render_template('dashboard.html')

    @app.route('/relatorios')
    def relatorios():
        return render_template('relatorios.html')
