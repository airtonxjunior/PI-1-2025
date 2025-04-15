from flask import Blueprint, render_template, request, jsonify, url_for, redirect
from database.database import ex_comando
user_route = Blueprint('user', __name__)

@user_route.route('/cadastro')
def mostrar_cadastro():
    return render_template("cadastro.html")


@user_route.route('/cadastro', methods=['POST'])
def criar_conta():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')


    comando = f'SELECT EXISTS(SELECT 1 FROM pessoas WHERE email = "{email}")'
    usuario_existe = ex_comando("GET_BY_ID", comando)

    if usuario_existe == 1:
        return jsonify({'erro': 'Usuário já cadastrado'}), 409

    comando_insert = f'INSERT INTO pessoas (nome, email, senha) VALUES ("{nome}", "{email}", "{senha}")'
    ex_comando("POST", comando_insert)

    comando= f'SELECT id FROM pessoas WHERE email = "{email}"'
    id_usuario = ex_comando("GET_BY_ID", comando)

    return jsonify({'id': id_usuario}) 


@user_route.route('/login')
def mostrar_login():
    return render_template("login.html")


@user_route.route('/login', methods=['POST'])
def fazer_login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    comando = f'SELECT * FROM pessoas WHERE email = "{email}" AND senha = "{senha}" LIMIT 1'
    retorno = ex_comando("GET", comando)

    if retorno:
        user = retorno[0]  
        return jsonify(id=user[0]), 201  
    else:
        return jsonify({"Status": "Erro ao executar login"}), 400



@user_route.route('/perfil/<int:id_usuario>')
def perfil(id_usuario):
    return render_template("perfil.html", id_usuario=id_usuario)


