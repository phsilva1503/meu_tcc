from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Componente(db.Model):
    __tablename__ = "componente"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Componente {self.nome}>"


class Producao(db.Model):
    __tablename__ = "producao"

    id = db.Column(db.Integer, primary_key=True)
    producao_id = db.Column(db.String(50), unique=True, nullable=False)
    data_producao = db.Column(db.Date, default=date.today, nullable=False)
    tipo_espuma = db.Column(db.String(50), nullable=False)
    densidade_real = db.Column(db.Float, nullable=False)
    conformidade = db.Column(db.String(20), nullable=False)
    observacoes = db.Column(db.Text)
    altura = db.Column(db.Float, nullable=True, default=0.0)

    componentes = db.relationship('ComponenteProducao',back_populates='producao',cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Producao {self.producao_id}>"


class ComponenteProducao(db.Model):
    __tablename__ = "componenteproducao"  # ou manter maiúsculo, mas deve bater com FK
    id = db.Column(db.Integer, primary_key=True)
    producao_id = db.Column(db.Integer, db.ForeignKey("producao.id"), nullable=False)
    componente_id = db.Column(db.Integer, db.ForeignKey("componente.id"), nullable=False)
    quantidade_usada = db.Column(db.Float, nullable=False)

    componente = db.relationship("Componente")
    producao = db.relationship("Producao", back_populates="componentes")
    def __repr__(self):
        return f"<ComponenteProducao Produção:{self.producao_id} Componente:{self.componente_id} Qtd:{self.quantidade_usada}>"



__all__ = ["db", "Componente", "Producao", "ComponenteProducao"].