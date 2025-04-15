import pymysql  

def criar_conexao():
    return pymysql.connect( 
        host='localhost',
        database='monitoramentosustentabilidade',
        user='root',
        password='sousa123'
    )

# Teste de conexão + leitura da tabela
con = criar_conexao()

if con.open:
    print('Conectado ao banco')
    cursor = con.cursor()

    cursor.execute('SELECT * FROM pessoas;')
    r = cursor.fetchone()
    while r:
        print(r)
        r = cursor.fetchone()

    cursor.close()
    con.close()

def POST(command):  # conseguiu criar => 'sucesso'
    con = criar_conexao()
    cursor = con.cursor()
    cursor.execute(command)
    con.commit()
    cursor.close()
    con.close()
    return "sucesso" 


def GET(command):  # conseguiu pegar => elemento do banco
    con = criar_conexao()
    cursor = con.cursor()
    cursor.execute(command)
    resultado = cursor.fetchall()
    cursor.close()
    con.close()
    return resultado


def GET_BY_ID(command):  # conseguiu pegar => elemento do banco
    con = criar_conexao()
    cursor = con.cursor()
    cursor.execute(command)
    resultado = cursor.fetchone()
    cursor.close()
    con.close()
    return resultado[0] if resultado else None


def PUT(command):  # conseguiu alterar => 'sucesso'
    con = criar_conexao()
    cursor = con.cursor()
    cursor.execute(command)
    con.commit()
    cursor.close()
    con.close()
    return "sucesso"


def DELETE(command):  # conseguiu deletar => 'sucesso'
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
