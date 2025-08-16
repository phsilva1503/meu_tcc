# routes/lean.py
from flask import Blueprint, render_template
import pandas as pd

bp = Blueprint('lean', __name__, url_prefix='/lean')

@bp.route('/')
def index():
    # ID da planilha - colocar o id da planilha de assistencia técnica
    sheet_id = "1cDVoNKstbLKWZrjBgCb6cVNHutXw06H4fuwdsO8p15o"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

    # Leitura da planilha
    df = pd.read_csv(url)

    # processar dados para gráficos do Lean
    dados_graficos = df.to_dict(orient='records')

    return render_template('lean.html', dados=dados_graficos)

