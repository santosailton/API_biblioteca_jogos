import os
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField


# validação de formulario pela API usando flask WTF
class FormularioJogo(FlaskForm):
    # parametros de min maximo dos campos do banco
    nome = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')


class FormularioUsuario(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Salvar')


capa_padrao = 'capa_padrao.jpg'


def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return capa_padrao


def deleta_arquivo(id):
    arquivo = recupera_imagem(id)

    if arquivo != capa_padrao:
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
