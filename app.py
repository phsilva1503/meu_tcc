from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///producao.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123'

db = SQLAlchemy(app)

# -----------------------
# MODELO feito via --force
# -----------------------
class Bloco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bloco_id = db.Column(db.String(50), unique=True, nullable=False)
    data_producao = db.Column(db.Date, default=datetime.utcnow)
    tipo_espuma = db.Column(db.String(50), nullable=False)
    densidade_real = db.Column(db.Float, nullable=False)
    conformidade = db.Column(db.String(20), nullable=False)
    observacoes = db.Column(db.Text)
    observacao2 = db.Column(db.Text)

# -----------------------
# ROTAS
# -----------------------



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
            observacao2=request.form.get('observacao2'),
        )
        db.session.add(bloco)
        db.session.commit()
        flash(f"Bloco '{bloco_id}' cadastrado com sucesso!", "success")
        return redirect(url_for('cadastro_prod'))

    blocos = Bloco.query.all()
    return render_template('cadastro_prod.html', blocos=blocos)

# criei essas rotas novas
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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registrar')
def registrar():
    return render_template('registrar.html')

# -----------------------
# EXECUÇÃO
# -----------------------
if __name__ == "__main__":
    with app.app_context(): # tem que estar dentro do app context para criar o banco
        db.create_all()  # cria o banco e tabelas se não existirem
    app.run(debug=True)
