from flask import Flask
from routes.user import user_route
from database.database import criar_conexao # Importa a função de conexão para teste inicial

# Cria a aplicação Flask.
app = Flask(__name__)

#chave secreta para sessões
app.secret_key = '9f8K!2@#v9sa7%$8vjsn3p9!sZ'

app.register_blueprint(user_route)

if __name__ == '__main__':
    app.run(debug=True)

try:
    conn = criar_conexao()
    if conn:
        print("Conexão com o banco de dados estabelecida com sucesso na inicialização do app.")
        conn.close()
    else:
        print("Falha ao estabelecer conexão com o banco de dados na inicialização do app.")
except Exception as e:
    print(f"Erro ao tentar conectar ao banco de dados na inicialização do app: {e}")

