
# Exemplo de API com Flask

O projeto visa apresentar a aplicação da biblioteca Flask integrando com Front-End, 
aplicando métodos de segurança contra atques CSRF e proteção de senha com cripografia hash.

Desenvolvido como sugestão de prática durante treinamento.
## Stack utilizada

**Front-end:** HTML, CSS

**Back-end:** 
- [Python 3.11](https://docs.python.org/3.11/)
- [Flask 2.2.2](https://flask.palletsprojects.com/en/2.2.x/)
- [Flask-SQLAlchemy 3.0.2](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
- [Flask-Bcrypt 1.0.1](https://flask-bcrypt.readthedocs.io/en/1.0.1/)
- [Flask-WTF 1.0.1](https://flask-wtf.readthedocs.io/en/1.0.x/)
- [mysql-connector-python  8.0.31](https://dev.mysql.com/doc/connector-python/en/)
- [MySQL Community Server 8.0.31](https://dev.mysql.com/downloads/mysql/)









## Melhorias

- Adicionado validação de sessão se está logado caso tente realizar operações sem sessão 
aberta ou abertura de nova sessão.
- Adicionado operações com contas DELETAR/CRIAR usuário.

## Documentação da API

#### Redireciona para formulário de criação de usuário:

```
  GET /novo_usuario
```


#### Redireciona para formulário de login:

```
  GET /login
```
