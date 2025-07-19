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

def criar_tabelas_se_nao_existirem():
    """
    Tenta criar as tabelas no banco de dados se elas não existirem.
    Esta função é chamada na inicialização do aplicativo.
    """
    print("Tentando criar tabelas se não existirem...")
    conn = None
    try:
        conn = criar_conexao()
        if conn is None:
            print("Não foi possível estabelecer conexão para criar tabelas.")
            return

        cursor = conn.cursor()

        # Comandos SQL para criar tabelas (ADAPTADOS PARA POSTGRESQL)
        # Use IF NOT EXISTS para evitar erros se a tabela já existir
        commands = [
            """
            CREATE TYPE IF NOT EXISTS tipo_transporte_enum AS ENUM ('carro', 'moto', 'onibus', 'metro', 'bicicleta', 'caminhada');
            """,
            """
            CREATE TYPE IF NOT EXISTS classificacao_final_enum AS ENUM ('Não Sustentável', 'Mediano', 'Sustentável');
            """,
            """
            CREATE TABLE IF NOT EXISTS pessoas (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                senha VARCHAR(255) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS monitoramento_parametros (
                id SERIAL PRIMARY KEY,
                pessoa_id INTEGER NOT NULL,
                data_registro DATE NOT NULL DEFAULT CURRENT_DATE,
                leitura_atual_agua DECIMAL(10,2),
                leitura_anterior_agua DECIMAL(10,2),
                pontuacao_agua SMALLINT,
                leitura_atual_energia DECIMAL(10,2),
                leitura_anterior_energia DECIMAL(10,2),
                pontuacao_energia SMALLINT,
                peso_residuo DECIMAL(5,2),
                pontuacao_residuo SMALLINT,
                tipo_transporte tipo_transporte_enum,
                distancia_transporte DECIMAL(6,2),
                emissao_co2 DECIMAL(6,2),
                pontuacao_transporte SMALLINT,
                FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS resultados_sustentabilidade (
                id SERIAL PRIMARY KEY,
                pessoa_id INTEGER NOT NULL,
                monitoramento_id INTEGER NOT NULL,
                data_calculo DATE NOT NULL DEFAULT CURRENT_DATE,
                pontuacao_agua SMALLINT NOT NULL,
                pontuacao_energia SMALLINT NOT NULL,
                pontuacao_residuo SMALLINT NOT NULL,
                pontuacao_transporte SMALLINT NOT NULL,
                media_final DECIMAL(3,2) NOT NULL,
                classificacao_final classificacao_final_enum NOT NULL,
                FOREIGN KEY (pessoa_id) REFERENCES pessoas(id),
                FOREIGN KEY (monitoramento_id) REFERENCES monitoramento_parametros(id)
            );
            """
        ]

        for command in commands:
            try:
                cursor.execute(command)
                conn.commit()
                print(f"Comando SQL executado com sucesso: {command.splitlines()[0]}...")
            except psycopg2.errors.DuplicateObject as e:
                # Ignora erro se o tipo/tabela já existe (por causa do IF NOT EXISTS)
                print(f"Objeto já existe, ignorando: {e}")
                conn.rollback() # Faz rollback para limpar o estado da transação
            except Exception as e:
                print(f"Erro ao executar comando SQL: {command.splitlines()[0]}... Erro: {e}")
                conn.rollback() # Faz rollback em caso de erro

        print("Verificação e criação de tabelas concluída.")

    except Exception as e:
        print(f"Erro geral na função criar_tabelas_se_nao_existirem: {e}")
    finally:
        if conn:
            conn.close()

# As funções GET, POST, PUT, DELETE e ex_comando precisam ser ajustadas
# para usar o cursor do psycopg2 e para trabalhar com parâmetros de forma segura.

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
            with con.cursor() as cursor:
                cursor.execute(comando_sql, params or ())
                
                if method.upper() in ["GET", "GET_ALL"]:
                    resultado = cursor.fetchall()
                elif method.upper() == "GET_BY_ID":
                    resultado = cursor.fetchone()
                else: # Para INSERT, UPDATE, DELETE
                    con.commit()
                    resultado = "Sucesso"
        return resultado
    except Exception as e:
        print(f"Erro ao executar comando: {e}")
        return None

def POST(command, params=None):
    return ex_comando("POST", command, params)

def GET(command, params=None):
    return ex_comando("GET", command, params)

def GET_BY_ID(command, params=None):
    return ex_comando("GET_BY_ID", command, params)

def PUT(command, params=None):
    return ex_comando("PUT", command, params)

def DELETE(command, params=None):
    return ex_comando("DELETE", command, params)

# Bloco de teste de conexão na inicialização do módulo (para Render e local)
# Este bloco agora é mais para verificar a conexão inicial do que criar tabelas.
con_test = criar_conexao()
if con_test:
    print('Conectado ao banco de dados na inicialização do módulo.')
    con_test.close()
else:
    print('Falha ao conectar ao banco de dados na inicialização do módulo.')
