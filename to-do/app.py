from flask import Flask
from flask import render_template, request, redirect,url_for, flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from forms import CadastroForm




app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config ["SECRET_KEY"] = '_5#y2L"F4Q8z\n\xec]/'
#DATABASE
''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Pedro/git/to-do/db.sqlite' #configura o nome e caminho da banco de dados

app.config['SQLALCHEMY_TRACK_MODIFICTAIONS'] = False
db= SQLAlchemy(app)


#Model : tabela utilizada
class Todo(db.Model):
    task_id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    done = db.Column(db.Boolean)
    



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    





#ROTAS FLASK

@app.route("/")
def index():
    todo_list=Todo.query.all()
    return  render_template('index.html',todo_list = todo_list)

@app.route ('/add',methods=['POST'])
def add():
    name = request.form.get("name")

    if not name:
        flash("O campo acima não pode estar vazio.", 'error')
        return redirect(url_for("index"))
    
    name = request.form.get("name")
    new_task = Todo(name = name, done = False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/editar/<int:todo_id>")
def editar(todo_id):
    todo = Todo.query.get(todo_id)
    
    if todo is None:
         if todo is None:
            return jsonify({'mensagem': 'Registro não encontrado'}), 404

    return render_template('editar.html', todo_id=todo_id,todo = todo )


# Rota para processar a atualização do registro
@app.route('/atualizar/<int:todo_id>', methods=['POST'])
def atualizar(todo_id):

    # Consulte o registro no banco de dados
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'mensagem': 'Registro não encontrado'}), 404
    # Atualize os campos desejados (exemplo: 'nome') com base nos dados do formulário
    if 'name' in request.form:
        todo.name = request.form['name']

    # Salve as alterações no banco de dados
    db.session.commit()

    return redirect(url_for("index"))



@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.get(todo_id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("index"))



@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo= Todo.query.get(todo_id)
    flash(f'O item {todo_id} foi excluído com sucesso.')
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/cadastro')
def cadastro():
    form = CadastroForm
    return render_template('cadastro.html', form = form)
    # return redirect(url_for("cadastro"))




#rodar a aplicação
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug = True)