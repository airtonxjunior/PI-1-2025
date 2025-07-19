# database/database.py

import pymysql
import os

def criar_conexao():
    """
    Cria uma conexão com o banco de dados MySQL.
    Hardcoded credentials for PythonAnywhere free tier, and fallback for local.
    """
    try:
        # Credenciais para o PythonAnywhere (Free Tier)
        # Atenção: Estas credenciais ficarão no código!
        # Hostname: airtonjunior.mysql.pythonanywhere-services.com
        # Username: airtonjunior
        # Password: Antonio123@
        # Database name: airtonjunior$default
        
        # Você pode comentar ou remover esta parte para rodar localmente,
        # ou ajustar o 'if' para um modo de desenvolvimento/produção mais robusto.
        
        # Verifica se estamos no ambiente PythonAnywhere ( heuristicamente )
        if 'PYTHONANYWHERE_SITE_NAME' in os.environ:
            host = 'airtonjunior.mysql.pythonanywhere-services.com'
            user = 'airtonjunior'
            password = 'Antonio123@'
            database = 'airtonjunior$default'
        else:
            # Credenciais para rodar no seu PC local
            host = 'localhost'
            user = 'root'
            password = 'sousa123'
            database = 'monitoramentosustentabilidade'

        return pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# O RESTO DO SEU CÓDIGO PERMANECE IGUAL, SEM MUDANÇAS
con = criar_conexao()
if con and con.open:
    print('Conectado ao banco')
else:
    print('Falha ao conectar ao banco')


def POST(command):
    con = criar_conexao()
    cursor = con.cursor()
    cursor.execute(command)
    con.commit()
    cursor.close()
    con.close()
    return "sucesso"


def GET(command):
    con = criar_conexao()
    cursor = con.cursor()
    cursor.execute(command)
    resultado = cursor.fetchall()
    cursor.close()
    con.close()
    return resultado


def GET_BY_ID(command):
    con = criar_conexao()
    cursor = con.cursor()
    cursor.execute(command)
    resultado = cursor.fetchone()
    cursor.close()
    con.close()
    return resultado if resultado else None


def PUT(command):
    con = criar_conexao()
    cursor = con.cursor()
    cursor.execute(command)
    con.commit()
    cursor.close()
    con.close()
    return "sucesso"


def DELETE(command):
    con = criar_conexao()
    cursor = con.cursor()
    cursor.execute(command)
    con.commit()
    cursor.close()
    con.close()
    return "sucesso"


def ex_comando(method, command):
    match method:
        case "POST":
            return POST(command)
        case "GET":
            return GET(command)
        case "GET_BY_ID":
            return GET_BY_ID(command)
        case "PUT":
            return PUT(command)
        case "DELETE":
            return DELETE(command)
        case _:
            return "MÉTODO INVÁLIDO"
    return " "