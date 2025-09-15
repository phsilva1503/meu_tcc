from flask import render_template, request, redirect, flash, url_for

def routes(app, db, Bloco):
    @app.route('/')
    def index():
        blocos = Bloco.query.all()
        return render_template('index-main.html', blocos=blocos)

    @app.route('/cadastro', methods=['GET', 'POST'])
    def cadastro_prod():
        if request.method == 'POST':
            bloco_id = request.form['bloco_id']
            existente = Bloco.query.filter_by(bloco_id=bloco_id).first()

            if existente:
                flash(f"Erro: bloco_id '{bloco_id}' já cadastrado!", "danger")
                return redirect(url_for('cadastro_prod'))

            bloco = Bloco(
                bloco_id=bloco_id,
                tipo_espuma=request.form['tipo_espuma'],
                densidade_real=float(request.form['densidade_real']),
                conformidade=request.form['conformidade'],
                observacoes=request.form.get('observacoes'),
            )
            db.session.add(bloco)
            db.session.commit()
            flash(f"Bloco '{bloco_id}' cadastrado com sucesso!", "success")
            return redirect(url_for('cadastro_prod'))

        blocos = Bloco.query.all()
        return render_template('cadastro_prod.html', blocos=blocos)

    @app.route('/controle-producao')
    def controle_producao():
        blocos = Bloco.query.all()
        return render_template('controle_producao.html', blocos=blocos)

    @app.route('/laudo-tecnico')
    def laudo_tecnico():
        return render_template('laudo-tecnico.html')

    @app.route('/lean_six_sigma')
    def lean_six_sigma():
        return render_template('lean.html')

    @app.route('/analise_preditiva')
    def analise_preditiva():
        return render_template('analise_preditiva.html')

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/relatorios')
    def relatorios():
        return render_template('relatorios.html')
