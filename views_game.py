from flask import render_template, request, redirect, session, flash, url_for, send_from_directory, jsonify
from models import Jogos
from jogoteca import app, db
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo
import time

@app.route('/')
def index():
    """
    rota raiz
    :return: lista jogos cadastrados
    """
    lista = Jogos.query.order_by(Jogos.id) #consulta em banco jogos cadastrados
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/editar/<int:id>') #testar com metodo post
def editar(id):
    """
    rota para atualizar formulario caso logado

    :param id: id do jogo que será editado
    :return: caso nao logado, redireciona para pagina de login. Caso logado, rendeniza o template de edição
    """

    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id))) # redireciona para proxima rota informada na url_for se logado

    jogo = Jogos.query.filter_by(id=id).first()
    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    capa_jogo = recupera_imagem(id)

    return render_template('editar.html', titulo='Editando Jogo', id=id, capa_jogo=capa_jogo, form=form)

#deletando informações do banco
@app.route('/deletar/<int:id>')
def deletar(id):
    """
    rota para deletar jogo
    :param id: id do jogo que será deletado
    :return: caso nao logado, redireciona para pagina de login. Caso logado, deletará o jogo informando por mensagem flash
    """
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Jogo deletado com sucesso")

    return redirect(url_for('index'))

#rota para redirecionar para criar formulario caso logado
@app.route('/novo')
def novo():
    """
    rota para criação de jogo

    :return: caso nao logado, redireciona para pagina de login. Caso logado, rendeniza template de criação novo.html
    """
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # se logado redireciona para a query string (proxima rota informada na url_for)
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioJogo()
    return render_template('novo.html', titulo='Novo Jogo', form=form)


#salvando informações do formulario
@app.route('/criar', methods=['POST',])
def criar():
    """
    rota para validar e inserir dados no banco de dados efetivando na base caso estiverem corretos

    :return: retorna Jogo já existente retornando para pagina principal ou adicionando jogo
    """
    #validacao se campos estao preenchidos
    form = FormularioJogo(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já existente')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    # gravação do arquivo no diretorio do projeto
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')

    # url_for para redirecionar para a pagina atraves do rota(endpoint) da pagina
    return redirect(url_for('index'))

@app.route('/atualizar', methods=['POST',]) #atualizando informações do banco
def atualizar():
    """
    rota para validar e editar dados no banco de dados efetivando na base caso estiverem corretos

    :return: redireciona para pagina principal com jogo editado
    """
    # recuperando dados da interface com FlaskForm
    form = FormularioJogo(request.form)

    if form.validate_on_submit():

        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(jogo.id)
        # gravação do arquivo no diretorio do projeto
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    """
    rota para carregar imagem para template

    :param nome_arquivo: capa do arquivo que enviada para template
    :return: carrega imagem do diretorio informado para o template
    """
    return send_from_directory('uploads', nome_arquivo)#carregamento de foto no diretorio informado