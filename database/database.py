import pymysql
import os

def criar_conexao():
    """
    Cria uma conexão com o banco de dados.
    Tenta usar as credenciais da hospedagem primeiro. Se não achar, usa as locais.
    """
    # Na hospedagem (PythonAnywhere), estas variáveis de ambiente vão existir.
    db_host = os.environ.get('DB_HOST')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_database = os.environ.get('DB_DATABASE')

    # Se estiver no seu PC, ele não vai achar as variáveis e vai usar seus dados locais.
    if not all([db_host, db_user, db_password, db_database]):
        db_host = 'localhost'
        db_user = 'root'
        db_password = 'sousa123'
        db_database = 'monitoramentosustentabilidade'

    try:
        return pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_database
        )
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# O resto do seu código permanece o mesmo.
# ... (suas funções POST, GET, etc. continuam aqui)
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