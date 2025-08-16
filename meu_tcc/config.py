# config.py
import os

class Config:
    """
    Configurações padrão para todas as instâncias da aplicação.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or '75ee48d81a48e393fe35c1aa952aee06'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
