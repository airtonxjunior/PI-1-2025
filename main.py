from flask import Flask
from routes.user import user_route
from database.database import criar_conexao, criar_tabelas_se_nao_existirem # Importa a nova função

# Cria a aplicação Flask.
app = Flask(__name__)

# Chave secreta para sessões.
app.secret_key = '9f8K!2@#v9sa7%$8vjsn3p9!sZ'

# Registra a blueprint (rotas em user_route) na aplicação.
app.register_blueprint(user_route)

# IMPORTANTE: REMOVA OU COMENTE ESTE BLOCO EM AMBIENTES DE PRODUÇÃO.
# if __name__ == '__main__':
#    app.run(debug=True)

# Chama a função para criar tabelas se elas não existirem.
# Isso será executado uma vez quando o aplicativo iniciar no Render.
with app.app_context(): # Garante que o contexto da aplicação Flask esteja ativo
    criar_tabelas_se_nao_existirem()

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

