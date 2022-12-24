from jogoteca import app
from flask import render_template, request, redirect, session, flash, url_for
from helpers import FormularioUsuario
from models import Usuarios
from flask_bcrypt import check_password_hash

#login servidor
@app.route('/login')
def login():
    if session['usuario_logado'] != None:
    # if 'usuario_logado' in session:
        flash(f'Usuario {session["""usuario_logado"""]} já logado')
        return redirect(url_for('index'))

    # criacao de variavel para recuperar query string(parametro da rota)
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    # parametro proxima = pagina a ser direcionada informado na query string
    return render_template('login.html', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST',]) #carregando formulario
def autenticar():
    form = FormularioUsuario(request.form)

    usuario = Usuarios.query.filter_by(nickname = form.nickname.data).first()

    if usuario:
        senha = check_password_hash(usuario.senha, form.senha.data)

        if usuario and senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname +' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuario ou senha incorreto!')#mensagens no html
            return redirect(url_for('login'))
    else:
        flash('Usuario ou senha incorreto!')#mensagens no html
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Sem usuario logado.')
        return redirect(url_for('index'))

    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))