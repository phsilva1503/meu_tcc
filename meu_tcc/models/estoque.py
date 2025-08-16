# models/estoque.py
from app import db

class Estoque(db.Model):
    """Modelo para representar o estoque de um produto."""
    id = db.Column(db.Integer, primary_key=True)
    # Nome do produto (Poliol, TDI, etc.)
    nome_produto = db.Column(db.String(100), unique=True, nullable=False)
    # Quantidade em estoque (kg)
    quantidade_estoque_kg = db.Column(db.Float, nullable=False, default=0.0)
    # Estoque mínimo (kg)
    estoque_minimo_kg = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f'<Estoque {self.nome_produto} - {self.quantidade_estoque_kg}kg (Min: {self.estoque_minimo_kg}kg)>'

    def abaixo_do_minimo(self):
        """Verifica se o estoque está abaixo do mínimo."""
        return self.quantidade_estoque_kg <= self.estoque_minimo_kg
