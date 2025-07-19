from flask import Flask
from routes.user import user_route

#cria a aplicação Flask.
app = Flask('__name__')

#chave secreta para sessões
app.secret_key = '9f8K!2@#v9sa7%$8vjsn3p9!sZ'

#registra a blueprint (rotas em user_route) na aplicação.
app.register_blueprint(user_route)

#inicia o servidor
app.run(debug=True)

