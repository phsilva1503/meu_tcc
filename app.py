from flask import Flask
from models import *
from flask_migrate import Migrate
from routes import routes  # Importa suas rotas definidas

# -----------------------
# CONFIGURAÇÃO DO APP
# -----------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///producao.db'  # Banco SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123'  # Para produção, gerar uma chave mais segura

# -----------------------
db.init_app(app)
migrate = Migrate(app,db)
# Registrando rotas
routes(app)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # útil para testes, mas migrations é o ideal
    app.run(host="0.0.0.0", port=5000, debug=True)
