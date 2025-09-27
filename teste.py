# teste.py
from app import app  # ou o arquivo onde o 'app' Flask está definido
from models import db, Componente

# precisa do contexto do Flask para acessar o banco
with app.app_context():
    componentes = Componente.query.all()
    for c in componentes:
        print(c.id, c.nome)
