import pymysql  

#função que cria a conexão com o banco
def criar_conexao():
    return pymysql.connect( 
        host='localhost',
        database='monitoramentosustentabilidade',
        user='root',
        password='sousa123'
    )

#teste para verificar se a conexão deu certo
con = criar_conexao()
if con.open:
    print('Conectado ao banco')

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


#função que recebe o metodo e comando, verifica o metodo e o executa com o comando
#essa função é exportada para routes
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

