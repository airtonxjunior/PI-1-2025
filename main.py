from flask import Flask
from routes.user import user_route
from database.database import criar_conexao # Importação da função de conexão mantida

# Cria a aplicação Flask.
# __name__ SEM ASPAS é crucial!
app = Flask(__name__)

# Chave secreta para sessões. Mantenha esta chave segura e complexa!
app.secret_key = '9f8K!2@#v9sa7%$8vjsn3p9!sZ'

# Registra a blueprint (rotas em user_route) na aplicação.
app.register_blueprint(user_route)

# IMPORTANTE: ESTE BLOCO DEVE SER REMOVIDO OU COMENTADO EM AMBIENTES DE PRODUÇÃO.
# O servidor do Render (Gunicorn) é quem inicia seu aplicativo, não o app.run().
# if __name__ == '__main__':
#    app.run(debug=True)

# Bloco de teste de conexão com o banco de dados.
# Mantido para diagnóstico na inicialização do aplicativo no Render.
try:
    conn = criar_conexao()
    if conn:
        print("Conexão com o banco de dados estabelecida com sucesso na inicialização do app.")
        conn.close()
    else:
        print("Falha ao estabelecer conexão com o banco de dados na inicialização do app.")
except Exception as e:
    print(f"Erro ao tentar conectar ao banco de dados na inicialização do app: {e}")

