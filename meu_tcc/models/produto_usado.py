# models/produto_usado.py
from app import db

class ProdutoUsado(db.Model):
    """Modelo para representar a quantidade de um produto usado em um bloco."""
    id = db.Column(db.Integer, primary_key=True)
    # Nome do produto (Poliol, TDI, etc.)
    nome_produto = db.Column(db.String(100), nullable=False)
    # Quantidade usada em kg
    quantidade_usada_kg = db.Column(db.Float, nullable=False)
    # ID do bloco ao qual este produto está associado (Foreign Key)
    bloco_id = db.Column(db.Integer, db.ForeignKey('bloco.id'), nullable=False)

    def __repr__(self):
        return f'<ProdutoUsado {self.nome_produto} - {self.quantidade_usada_kg}kg no Bloco {self.bloco_id}>'
