from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Bloco(db.Model):
    __tablename__ = "blocos"  # nome explícito da tabela

    id = db.Column(db.Integer, primary_key=True)
    bloco_id = db.Column(db.String(50), unique=True, nullable=False)
    data_producao = db.Column(db.Date, default=date.today, nullable=False)
    tipo_espuma = db.Column(db.String(50), nullable=False)
    densidade_real = db.Column(db.Float, nullable=False)
    conformidade = db.Column(db.String(20), nullable=False)
    observacoes = db.Column(db.Text)


