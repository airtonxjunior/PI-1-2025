import pymysql
import os

def criar_conexao():
    try:
        host = os.environ.get('DB_HOST')
        user = os.environ.get('DB_USER')
        password = os.environ.get('DB_PASSWORD')
        database = os.environ.get('DB_DATABASE')

        if not all([host, user, password, database]):
            print("Usando credenciais locais...")
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