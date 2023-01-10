from jogoteca import app, db
from flask import render_template, request, redirect, session, flash, url_for
from helpers import FormularioUsuario
from models import Usuarios
from flask_bcrypt import check_password_hash, generate_password_hash


@app.route('/login')
def login():
    if 'usuario_logado' in session and session['usuario_logado'] != None:
        flash(f'Usuario {session["""usuario_logado"""]} já logado')
        return redirect(url_for('index'))

    # criacao de variavel para recuperar query string(parametro da rota)
    proxima = request.args.get('proxima')
    form = FormularioUsuario()

    # parametro proxima = pagina a ser direcionada informado na query string
    return render_template('login.html', proxima=proxima, form=form)


@app.route('/autenticar', methods=['POST', ])  # carregando formulario
def autenticar():
    form = FormularioUsuario(request.form)

    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()

    if usuario:
        senha = check_password_hash(usuario.senha, form.senha.data)

        if usuario and senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuario ou senha incorreto!')  # mensagens no html
            return redirect(url_for('login'))
    else:
        flash('Usuario ou senha incorreto!')  # mensagens no html
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sem usuario logado.')
        return redirect(url_for('index'))

    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))


@app.route('/novo_usuario')
def novo_usuario():
    """
    rota para criação de usuario
    :return: caso logado, desloga usuario atual e rendeniza template de criação registrar.html
    """

    if 'usuario_logado' in session and session['usuario_logado'] != None:
        session['usuario_logado'] = None
        flash('Usuário deslogado para criação de um novo.')

    form = FormularioUsuario()
    return render_template('registrar.html', titulo='Criar Usuário', form=form)


@app.route('/registrar', methods=['POST', ])
def registrar():
    form = FormularioUsuario(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('novo_usuario'))

    nome = form.nome.data
    nickname = form.nickname.data
    senha = form.senha.data

    usuario = Usuarios.query.filter_by(nickname=nickname).first()
    if usuario:
        flash('Nickname já cadastrado.')
        return redirect(url_for('index'))

    novo_usuario = Usuarios(nome=nome, nickname=nickname, senha=generate_password_hash(senha))
    db.session.add(novo_usuario)
    db.session.commit()
    return redirect(url_for('index'))
