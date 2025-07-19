# database/database.py

import os
from urllib.parse import urlparse
import psycopg2 # Importa o driver psycopg2

def criar_conexao():
    """Cria uma conexão com o banco de dados PostgreSQL."""
    try:
        database_url = os.environ.get('DATABASE_URL')
        
        if not database_url:
            # Fallback para credenciais locais (MySQL) se DATABASE_URL não estiver definida.
            # Isso permite que você continue desenvolvendo localmente com MySQL.
            print("DATABASE_URL não definida. Usando credenciais locais (MySQL)...")
            import pymysql # Importa PyMySQL apenas para uso local
            return pymysql.connect(
                host='localhost',
                user='root',
                password='sousa123',
                database='monitoramentosustentabilidade',
                cursorclass=pymysql.cursors.DictCursor
            )
        
        # Se DATABASE_URL estiver definida (ambiente Render)
        url = urlparse(database_url)
        
        # Conecta usando as informações da URL do PostgreSQL
        conn = psycopg2.connect(
            host=url.hostname,
            user=url.username,
            password=url.password,
            database=url.path[1:], # Remove a barra inicial
            port=url.port if url.port else 5432 # Porta padrão do PostgreSQL é 5432
        )
        print(f"Conexão com o DB Render (PostgreSQL) estabelecida com sucesso.")
        return conn
        
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def ex_comando(method, comando_sql, params=None):
    """
    Executa um comando SQL de forma segura.
    ATENÇÃO: Com psycopg2, 'params' deve ser uma TUPLA ou LISTA de valores,
    e o 'comando_sql' deve usar '%s' como placeholder.
    """
    con = criar_conexao()
    if con is None:
        return None

    try:
        with con:
            # O cursor padrão do psycopg2 retorna tuplas. Se precisar de dicionários,
            # você pode usar 'psycopg2.extras.DictCursor' mas precisaria importar.
            with con.cursor() as cursor:
                # O psycopg2 espera parâmetros como uma tupla/lista e usa %s para placeholders.
                # Se params for None, ele passa uma tupla vazia.
                cursor.execute(comando_sql, params or ())
                
                if method.upper() in ["GET", "GET_ALL"]:
                    resultado = cursor.fetchall() # Retorna lista de tuplas
                elif method.upper() == "GET_BY_ID":
                    resultado = cursor.fetchone() # Retorna uma tupla
                else: # Para INSERT, UPDATE, DELETE
                    con.commit()
                    resultado = "Sucesso"
        return resultado
    except Exception as e:
        print(f"Erro ao executar comando: {e}")
        return None

# Funções auxiliares para manter a interface externa.
# Elas chamam ex_comando.
# Se suas rotas passavam parâmetros, a chamada a ex_comando dentro delas
# precisa ser ajustada para passar uma TUPLA/LISTA de parâmetros.
# Por exemplo: ex_comando("GET_BY_ID", "SELECT * FROM users WHERE id = %s", (user_id,))

def POST(command, params=None): # Adicionado params para consistência
    return ex_comando("POST", command, params)

def GET(command, params=None): # Adicionado params para consistência
    return ex_comando("GET", command, params)

def GET_BY_ID(command, params=None): # Adicionado params para consistência
    return ex_comando("GET_BY_ID", command, params)

def PUT(command, params=None): # Adicionado params para consistência
    return ex_comando("PUT", command, params)

def DELETE(command, params=None): # Adicionado params para consistência
    return ex_comando("DELETE", command, params)

# Bloco de teste de conexão na inicialização do módulo (para Render e local)
con_test = criar_conexao()
if con_test:
    print('Conectado ao banco de dados na inicialização do módulo.')
    con_test.close()
else:
    print('Falha ao conectar ao banco de dados na inicialização do módulo.')
