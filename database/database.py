# database/database.py
import pymysql
import os
from urllib.parse import urlparse # Importa urlparse

def criar_conexao():
    """Cria uma conexão com o banco de dados MySQL."""
    try:
        database_url = os.environ.get('DATABASE_URL')
        
        if database_url:
            # Parseia a DATABASE_URL fornecida pelo Render (PostgreSQL)
            url = urlparse(database_url)
            
            host = url.hostname
            user = url.username
            password = url.password
            database = url.path[1:] # Remove a barra inicial
            port = url.port if url.port else 3306 # MySQL default port, Render pode ter outra

            # Print para depuração (remova em produção final)
            print(f"Conectando ao DB Render: Host={host}, User={user}, DB={database}, Port={port}")

            # Tenta conectar com PyMySQL usando as partes da URL do Render
            # Lembre-se: PyMySQL é para MySQL, Render usa PostgreSQL.
            # Esta é a "gambiarra" para evitar trocar o driver.
            # Se falhar aqui, a solução é trocar para psycopg2-binary.
            return pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port, 
                cursorclass=pymysql.cursors.DictCursor
            )
        else:
            # Se DATABASE_URL não estiver definida (provavelmente rodando localmente)
            print("DATABASE_URL não definida. Usando credenciais locais...")
            host = 'localhost'
            user = 'root'
            password = 'sousa123'
            database = 'monitoramentosustentabilidade'
            return pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                cursorclass=pymysql.cursors.DictCursor
            )
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# O resto do seu código de ex_comando, POST, GET, etc. permanece igual.
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
        case _:\
            return "MÉTODO INVÁLIDO"
    return " "
