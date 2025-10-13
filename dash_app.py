from flask import render_template
from models import Producao, Componente
import pandas as pd
import plotly.express as px
import json
import plotly

# dash_app.py
from flask import render_template
from models import Producao, Componente

def registrar_rotas_dash(app):
    @app.route('/dashboard')
    def dashboard():
        producoes = Producao.query.order_by(Producao.id.desc()).all()
        componentes = Componente.query.filter_by(ativo=True).all()
        return render_template('dashboard.html', producoes=producoes, componentes=componentes)
ff