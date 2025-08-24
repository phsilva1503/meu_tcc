from flask import Flask, render_template, request, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///producao.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123'

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # habilita as migrações

# -----------------------
# MODELOS
# -----------------------
class Bloco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bloco_id = db.Column(db.String(50), unique=True, nullable=False)
    data_producao = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    tipo_espuma = db.Column(db.String(50), nullable=False)
    densidade_real = db.Column(db.Float, nullable=False)
    conformidade = db.Column(db.String(20), nullable=False)
    observacoes = db.Column(db.Text)
    observacao2 = db.Column(db.Text)  # nova coluna adicionada

# -----------------------
# ROTAS
# Página principal - mostra o formulário + lista de blocos
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        bloco_id = request.form['bloco_id']
        existente = Bloco.query.filter_by(bloco_id=bloco_id).first()
        if existente:
            flash(f"Erro: bloco_id '{bloco_id}' já cadastrado!", "erro")
            return redirect('/')  # volta para o formulário sem sair da página

        bloco = Bloco(
            bloco_id=bloco_id,
            tipo_espuma=request.form['tipo_espuma'],
            densidade_real=float(request.form['densidade_real']),
            conformidade=request.form['conformidade'],
            observacoes=request.form['observacoes'],
            observacao2=request.form.get('observacao2')
        )
        db.session.add(bloco)
        db.session.commit()
        flash(f"Bloco '{bloco_id}' cadastrado com sucesso!", "sucesso")
        return redirect('/')
    
    blocos = Bloco.query.all()
    return render_template('index.html', blocos=blocos)

# -----------------------
# EXECUÇÃO
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
