from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class CadastroForm(FlaskForm):
    usuario = StringField('Username:')
    email = StringField('E-mail:')
    senha1 = PasswordField('Senha:')
    senha2 = PasswordField('Confirmação de Senha:')
    submit = SubmitField('Cadastrar')