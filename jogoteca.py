from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

app = Flask(__name__)
#carregamento de config do projeto
app.config.from_pyfile('config.py')
#drive de conexao com banco
db = SQLAlchemy(app)
#protecao de falha csrf
csrf = CSRFProtect(app)

bcrypt = Bcrypt(app)

from views_user import *
from views_game import *

# execucao do servidor com parametro para reexecutar a cada alteracao
if __name__ == '__main__':
    app.run(debug=True)