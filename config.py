import os
SECRET_KEY = 'alura' #criar palavra chave para criptografia

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '123456',
        servidor = 'localhost',
        database = 'jogoteca'
        )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'