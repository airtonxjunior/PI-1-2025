from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta
from database.database import ex_comando
user_route = Blueprint('user', __name__)

@user_route.route('/cadastro')
def mostrar_cadastro():
    return render_template("cadastro.html")


@user_route.route('/cadastro', methods=['POST'])
def criar_conta():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')


    comando = f'SELECT EXISTS(SELECT 1 FROM pessoas WHERE email = "{email}")'
    usuario_existe = ex_comando("GET_BY_ID", comando)

    if usuario_existe == 1:
        return jsonify({'erro': 'Usuário já cadastrado'}), 409

    comando_insert = f'INSERT INTO pessoas (nome, email, senha) VALUES ("{nome}", "{email}", "{senha}")'
    ex_comando("POST", comando_insert)

    comando= f'SELECT id FROM pessoas WHERE email = "{email}"'
    id_usuario = ex_comando("GET_BY_ID", comando)

    return jsonify({'id': id_usuario}) 


@user_route.route('/login')
def mostrar_login():
    return render_template("login.html")


@user_route.route('/login', methods=['POST'])
def fazer_login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    comando = f'SELECT * FROM pessoas WHERE email = "{email}" AND senha = "{senha}" LIMIT 1'
    retorno = ex_comando("GET", comando)

    if retorno:
        user = retorno[0]  
        return jsonify(id=user[0]), 201  
    else:
        return jsonify({"Status": "Erro ao executar login"}), 400


@user_route.route('/perfil/<int:id_usuario>')
def perfil(id_usuario):
    comando= f'SELECT nome FROM pessoas WHERE id = {id_usuario}'
    resultado= ex_comando("GET_BY_ID", comando)
    if resultado:
        nome_usuario = resultado[0] 
    return render_template("perfil.html", id_usuario=id_usuario, nome_usuario=nome_usuario)


@user_route.route('/perfil/<int:id_usuario>/sustentabilidade')
def mostrar_sustentabilidade(id_usuario):
    comando = f"SELECT media_final, classificacao_final FROM resultados_sustentabilidade WHERE id = {id_usuario} ORDER BY id DESC LIMIT 1"
    resultado = ex_comando("GET_BY_ID", comando)

    if resultado:
        media_final, classificacao_final = resultado  
    else:
        media_final = 0
        classificacao_final = "Não Sustentável"

    if classificacao_final == "Sustentável":
            if media_final == 3:
                selo = True
            else: 
                 selo = False
            imagem = "/static/img/sust.jpeg"
            dica = "Você está no nível máximo! Continue com seus hábitos sustentáveis para manter esse nível."
    elif classificacao_final == "Mediano":
            selo = False
            imagem = "/static/img/mediano.jpeg"
            dica = "Você está no caminho certo! Tente melhorar seu consumo de água, energia e produção de resíduos."
    else:
            selo = False
            imagem = "/static/img/nao-sust.jpeg"
            dica = "Tente rever seus hábitos diários para tornar seu estilo de vida mais sustentável."

    return render_template("sustentabilidade.html", id_usuario=id_usuario,  media_final=media_final, classificacao_final=classificacao_final, selo=selo, imagem=imagem, dica=dica)


@user_route.route('/perfil/<int:id_usuario>/graficos')
def mostrar_graficos(id_usuario):
    periodo = request.args.get('periodo', 7)  # Pega o período selecionado na URL, padrão é 7 dias

    comando = f'''
        SELECT data_calculo, pontuacao_agua, pontuacao_energia, pontuacao_residuo, pontuacao_transporte, media_final
        FROM resultados_sustentabilidade
        WHERE pessoa_id = {id_usuario}
        AND data_calculo >= CURDATE() - INTERVAL {periodo} DAY
        ORDER BY data_calculo DESC
    '''
    
    historico = ex_comando("GET", comando)

    # Verificar se há dados
    if historico:
        datas = [h[0] for h in historico]  # Extraindo as datas
        pontuacao_agua = [h[1] for h in historico]
        pontuacao_energia = [h[2] for h in historico]
        pontuacao_residuo = [h[3] for h in historico]
        pontuacao_transporte = [h[4] for h in historico]
        media_final = [h[5] for h in historico]
    else:
        datas = pontuacao_agua = pontuacao_energia = pontuacao_residuo = pontuacao_transporte = media_final = []

    return render_template(
        "graficos.html",
        id_usuario=id_usuario,
        pontuacao_agua=pontuacao_agua,
        pontuacao_energia=pontuacao_energia,
        pontuacao_residuo=pontuacao_residuo,
        pontuacao_transporte=pontuacao_transporte,
        media_final=media_final,
        datas=datas
    )


@user_route.route('/perfil/<int:id_usuario>/inserir-dados', methods=['GET'])
def mostrar_inserir_dados(id_usuario):
    return render_template("inserir-dados.html", id_usuario=id_usuario)

@user_route.route('/perfil/<int:id_usuario>/inserir-dados', methods=['POST'])
def enviar_dados(id_usuario):
    data = request.json
    agua = data.get('agua')
    energia = data.get('energia')
    lixo = data.get('lixo')
    transporte = data.get('transporte')
    distancia = data.get('distancia')


    comando_inserir = f"""
        INSERT INTO monitoramento_parametros (
            pessoa_id, data_registro, leitura_atual_agua, leitura_anterior_agua,
            leitura_atual_energia, leitura_anterior_energia, peso_residuo,
            tipo_transporte, distancia_transporte
        ) VALUES (
            {id_usuario}, CURDATE(), {agua}, NULL, {energia}, NULL, {lixo}, '{transporte}', {distancia}
        )
    """
    ex_comando("POST", comando_inserir)


    comando_update_agua = f"""
        UPDATE monitoramento_parametros
        SET pontuacao_agua = CASE
            WHEN (leitura_atual_agua - COALESCE(leitura_anterior_agua, 0)) > 150 THEN 1
            WHEN (leitura_atual_agua - COALESCE(leitura_anterior_agua, 0)) BETWEEN 110 AND 150 THEN 2
            ELSE 3
        END
        WHERE pessoa_id = {id_usuario} AND pontuacao_agua IS NULL;
    """
    ex_comando("PUT", comando_update_agua)


    comando_update_energia = f"""
        UPDATE monitoramento_parametros
        SET pontuacao_energia = CASE
            WHEN (leitura_atual_energia - COALESCE(leitura_anterior_energia, 0)) > 180 THEN 1
            WHEN (leitura_atual_energia - COALESCE(leitura_anterior_energia, 0)) BETWEEN 120 AND 180 THEN 2
            ELSE 3
        END
        WHERE pessoa_id = {id_usuario} AND pontuacao_energia IS NULL;
    """
    ex_comando("PUT", comando_update_energia)


    comando_update_residuo = f"""
        UPDATE monitoramento_parametros
        SET pontuacao_residuo = CASE
            WHEN peso_residuo > 1.2 THEN 1
            WHEN peso_residuo BETWEEN 0.8 AND 1.2 THEN 2
            ELSE 3
        END
        WHERE pessoa_id = {id_usuario} AND pontuacao_residuo IS NULL;
    """
    ex_comando("PUT", comando_update_residuo)


    comando_update_emissao = f"""
        UPDATE monitoramento_parametros
        SET emissao_co2 = CASE tipo_transporte
            WHEN 'carro' THEN distancia_transporte * 0.12
            WHEN 'moto' THEN distancia_transporte * 0.08
            WHEN 'onibus' THEN distancia_transporte * 0.03
            WHEN 'metro' THEN distancia_transporte * 0.01
            WHEN 'bicicleta' THEN 0
            WHEN 'caminhada' THEN 0
            ELSE 0
        END
        WHERE pessoa_id = {id_usuario} AND emissao_co2 IS NULL;
    """
    ex_comando("PUT", comando_update_emissao)


    comando_update_transporte = f"""
        UPDATE monitoramento_parametros
        SET pontuacao_transporte = CASE
            WHEN emissao_co2 > 5 THEN 1
            WHEN emissao_co2 BETWEEN 2 AND 5 THEN 2
            ELSE 3
        END
        WHERE pessoa_id = {id_usuario} AND pontuacao_transporte IS NULL;
    """
    ex_comando("PUT", comando_update_transporte)
    comando_resultados = f"""
        INSERT INTO resultados_sustentabilidade (
            pessoa_id,
            monitoramento_id,
            data_calculo,
            pontuacao_agua,
            pontuacao_energia,
            pontuacao_residuo,
            pontuacao_transporte,
            media_final,
            classificacao_final
        )
        SELECT
            pessoa_id,
            id AS monitoramento_id,
            data_registro,
            pontuacao_agua,
            pontuacao_energia,
            pontuacao_residuo,
            pontuacao_transporte,
            (pontuacao_agua + pontuacao_energia + pontuacao_residuo + pontuacao_transporte) / 4.0 AS media,
            CASE
                WHEN (pontuacao_agua + pontuacao_energia + pontuacao_residuo + pontuacao_transporte) / 4.0 >= 2.5 THEN 'Sustentável'
                WHEN (pontuacao_agua + pontuacao_energia + pontuacao_residuo + pontuacao_transporte) / 4.0 >= 1.5 THEN 'Mediano'
                ELSE 'Não Sustentável'
            END AS classificacao
        FROM monitoramento_parametros
        WHERE id NOT IN (
            SELECT monitoramento_id FROM resultados_sustentabilidade
        );
    """
    ex_comando("POST", comando_resultados)

    return jsonify({'message': 'Dados inseridos e resultados calculados com sucesso', 'id_usuario': id_usuario}), 201


@user_route.route('/perfil/<int:id_usuario>/editar-dados', methods=['GET'])
def mostrar_editar_dados(id_usuario):
    return render_template("editar-dados.html", id_usuario=id_usuario)

@user_route.route('/perfil/<int:id_usuario>/editar-dados', methods=['PUT'])
def editar_dados(id_usuario):
    data = request.json
    data_registro = data.get('data_registro') 
    parametro = data.get('parametro') 
    novo_valor = data.get('valor')
    tipo_transporte = data.get('tipo_transporte')
    distancia = data.get('distancia')

    if parametro == 'agua':
        comando_editar = f"""
            UPDATE monitoramento_parametros
            SET leitura_atual_agua = {novo_valor}
            WHERE pessoa_id = {id_usuario} AND data_registro = '{data_registro}';
        """
    elif parametro == 'energia':
        comando_editar = f"""
            UPDATE monitoramento_parametros
            SET leitura_atual_energia = {novo_valor}
            WHERE pessoa_id = {id_usuario} AND data_registro = '{data_registro}';
        """
    elif parametro == 'residuos':
        comando_editar = f"""
            UPDATE monitoramento_parametros
            SET peso_residuo = {novo_valor}
            WHERE pessoa_id = {id_usuario} AND data_registro = '{data_registro}';
        """
    elif parametro == 'transporte' and tipo_transporte:
        comando_editar = f"""
            UPDATE monitoramento_parametros
            SET tipo_transporte = '{tipo_transporte}',
                distancia_transporte = {distancia}
            WHERE pessoa_id = {id_usuario} AND data_registro = '{data_registro}';
        """
    elif parametro == 'distancia' and distancia:
        comando_editar = f"""
            UPDATE monitoramento_parametros
            SET distancia_transporte = {distancia}
            WHERE pessoa_id = {id_usuario} AND data_registro = '{data_registro}';
        """
    else:
        return jsonify({'message': 'Parâmetro inválido ou falta de dados'}), 400


    ex_comando("PUT", comando_editar)

    #cálculo das pontuações
    if parametro == 'agua':
        comando_update_agua = f"""
            UPDATE monitoramento_parametros
            SET pontuacao_agua = CASE
                WHEN (leitura_atual_agua - COALESCE(leitura_anterior_agua, 0)) > 150 THEN 1
                WHEN (leitura_atual_agua - COALESCE(leitura_anterior_agua, 0)) BETWEEN 110 AND 150 THEN 2
                ELSE 3
            END
            WHERE pessoa_id = {id_usuario} AND data_registro = '{data_registro}';
        """
        ex_comando("PUT", comando_update_agua)

    if parametro == 'energia':
        comando_update_energia = f"""
            UPDATE monitoramento_parametros
            SET pontuacao_energia = CASE
                WHEN (leitura_atual_energia - COALESCE(leitura_anterior_energia, 0)) > 180 THEN 1
                WHEN (leitura_atual_energia - COALESCE(leitura_anterior_energia, 0)) BETWEEN 120 AND 180 THEN 2
                ELSE 3
            END
            WHERE pessoa_id = {id_usuario} AND data_registro = '{data_registro}';
        """
        ex_comando("PUT", comando_update_energia)

    if parametro == 'residuos':
        comando_update_residuo = f"""
            UPDATE monitoramento_parametros
            SET pontuacao_residuo = CASE
                WHEN peso_residuo > 1.2 THEN 1
                WHEN peso_residuo BETWEEN 0.8 AND 1.2 THEN 2
                ELSE 3
            END
            WHERE pessoa_id = {id_usuario} AND data_registro = '{data_registro}';
        """
        ex_comando("PUT", comando_update_residuo)

    if parametro == 'transporte' or parametro == 'distancia':
        comando_update_emissao = f"""
            UPDATE monitoramento_parametros
            SET emissao_co2 = CASE tipo_transporte
                WHEN 'carro' THEN distancia_transporte * 0.12
                WHEN 'moto' THEN distancia_transporte * 0.08
                WHEN 'onibus' THEN distancia_transporte * 0.03
                WHEN 'metro' THEN distancia_transporte * 0.01
                WHEN 'bicicleta' THEN 0
                WHEN 'caminhada' THEN 0
                ELSE 0
            END
            WHERE pessoa_id = {id_usuario} AND data_registro = '{data_registro}';
        """
        ex_comando("PUT", comando_update_emissao)

        comando_update_transporte = f"""
            UPDATE monitoramento_parametros
            SET pontuacao_transporte = CASE
                WHEN emissao_co2 > 5 THEN 1
                WHEN emissao_co2 BETWEEN 2 AND 5 THEN 2
                ELSE 3
            END
            WHERE pessoa_id = {id_usuario} AND data_registro = '{data_registro}';
        """
        ex_comando("PUT", comando_update_transporte)

    #atualizar a tabela de resultados
    comando_update_resultado = f"""
        UPDATE resultados_sustentabilidade
        SET 
            pontuacao_agua = (
                SELECT pontuacao_agua FROM monitoramento_parametros
                WHERE pessoa_id = {id_usuario} AND data_registro = '{data_registro}'
                LIMIT 1
            ),
            pontuacao_energia = (
                SELECT pontuacao_energia FROM monitoramento_parametros
                WHERE pessoa_id = {id_usuario} AND data_registro = '{data_registro}'
                LIMIT 1
            ),
            pontuacao_residuo = (
                SELECT pontuacao_residuo FROM monitoramento_parametros
                WHERE pessoa_id = {id_usuario} AND data_registro = '{data_registro}'
                LIMIT 1
            ),
            pontuacao_transporte = (
                SELECT pontuacao_transporte FROM monitoramento_parametros
                WHERE pessoa_id = {id_usuario} AND data_registro = '{data_registro}'
                LIMIT 1
            ),
            media_final = (
                SELECT ROUND((
                    COALESCE(pontuacao_agua, 0) + 
                    COALESCE(pontuacao_energia, 0) + 
                    COALESCE(pontuacao_residuo, 0) + 
                    COALESCE(pontuacao_transporte, 0)
                ) / 4.0, 2)
                FROM monitoramento_parametros
                WHERE pessoa_id = {id_usuario} AND data_registro = '{data_registro}'
                LIMIT 1
            )
        WHERE id = {id_usuario};
    """
    ex_comando("PUT", comando_update_resultado)

    return jsonify({'message': 'Dado atualizado com sucesso e pontuação recalculada.', 'id_usuario': id_usuario, 'data_registro': data_registro, 'parametro': parametro}), 200

