# models/bloco.py
from app import db
from datetime import datetime

class Bloco(db.Model):
    """Modelo para representar um bloco de espuma produzido."""
    id = db.Column(db.Integer, primary_key=True)
    # ID do Bloco (pode ser string)
    bloco_id = db.Column(db.String(50), unique=True, nullable=False)
    # Data de produção
    data_producao = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    # Tipo de Espuma (Comum, Selada, Especial, Cilíndrica)
    tipo_espuma = db.Column(db.String(50), nullable=False)
    # Densidade Real (kg/m³)
    densidade_real = db.Column(db.Float, nullable=False)
    # Conformidade (Conforme, Não Conforme)
    conformidade = db.Column(db.String(20), nullable=False)
    # Observações
    observacoes = db.Column(db.Text)

    # Relacionamento com os produtos usados (um bloco pode ter muitos registros de produtos usados)
    produtos_usados = db.relationship('ProdutoUsado', backref='bloco', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Bloco {self.bloco_id} - {self.tipo_espuma}>'
