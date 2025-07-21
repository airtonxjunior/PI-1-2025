from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from database.database import ex_comando
from criptografia.criptografia import criptografar_hill, descriptografar_hill


user_route = Blueprint('user', __name__)

@user_route.route('/')
def home():
    return render_template('index.html')

@user_route.route('/cadastro')
def mostrar_cadastro():
    return render_template("cadastro.html")

@user_route.route('/cadastro', methods=['POST'])
def criar_conta():
    #pega os dados inseridos no formulario via requisição json
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha_original = data.get('senha')

    #usa a função para criptografar a senha
    senha_criptografada = criptografar_hill(senha_original)

    #verifica se existe algum usuário com o mesmo email
    comando = "SELECT EXISTS(SELECT 1 FROM pessoas WHERE email = %s)"
    resultado = ex_comando("GET_BY_ID", comando, (email,)) #passa o email como uma tupla

    if resultado and resultado[0]: #verifica se a tupla não está vazia e o primeiro elemento é True/1
        return jsonify({'erro': 'Usuário já cadastrado com este e-mail.'}), 409

    #inserir novo usuário com senha criptografada no banco
    comando = "INSERT INTO pessoas (nome, email, senha) VALUES (%s, %s, %s)"
    try:
        ex_comando("POST", comando, (nome, email, senha_criptografada)) #passa os valores como tupla
    except Exception as e_db:
        print(f"Erro ao inserir usuário no banco: {e_db}")
        return jsonify({'erro': 'Erro ao criar conta no banco de dados.'}), 500

    #pega o id do usuário gerado no banco
    comando = "SELECT id FROM pessoas WHERE email = %s"
    resultado = ex_comando("GET_BY_ID", comando, (email,)) #passa o email como uma tupla

    if resultado:
        id_usuario = resultado[0] #resultado é uma tupla, ex: (123,)
        return jsonify({'id': id_usuario, 'message': 'Conta criada com sucesso!'}), 201
    else:
        print(f"Erro CRÍTICO: Usuário inserido mas ID não encontrado para email {email}")
        return jsonify({'erro': 'Conta criada, mas houve um problema ao finalizar o registro.'}), 500

@user_route.route('/login')
def mostrar_login():
    return render_template("login.html")

@user_route.route('/login', methods=['POST'])
def fazer_login():
    #pega os dados inserido no form via requisição json
    data = request.json
    email = data.get('email')
    senha_original = data.get('senha')

    #pega o id e senha do usuário que está no banco de dados
    comando = "SELECT id, senha FROM pessoas WHERE email = %s LIMIT 1"
    retorno = ex_comando("GET_BY_ID", comando, (email,)) #passa o email como uma tupla

    #se tiver retorno, essas duas variáveis recebem o retorno
    if retorno:
        id_usuario_db, senha_criptografada_db = retorno #retorno é uma tupla, ex: (1, 'SENHA_CRIP')
        
        try:
            #faz a descriptografia
            senha_descriptografada = descriptografar_hill(senha_criptografada_db)
            
            #se as senhas forem iguais após a descriptografia, a sessão é iniciada
            if senha_original.upper() == senha_descriptografada:
                session['user_id'] = id_usuario_db
                return jsonify({'id': id_usuario_db, 'message': 'Login realizado com sucesso'}), 200
            else:
                return jsonify({"erro": "E-mail ou senha inválidos."}), 401
        except ValueError as e:
            return jsonify({"erro": "Erro ao processar credenciais."}), 500
    else:
        #retorna erro caso a email e senha não sejam encontrados no banco
        return jsonify({"erro": "E-mail ou senha inválidos."}), 401

@user_route.route('/logout')
def logout():
    #se o botão sair for apertado, o id é retirado e o usuário é redirecionado para o inicio
    session.pop('user_id', None) 
    return redirect(url_for('user.home'))

@user_route.route('/perfil/<int:id_usuario>')
def perfil(id_usuario):
    #se o id não estiver em session ou for diferente, o usuário é redirecionado para a tela de login
    if 'user_id' not in session or session['user_id'] != id_usuario:
        return redirect(url_for('user.mostrar_login'))
    
    #pega o nome do usuário para retornar pro frontend
    comando = "SELECT nome FROM pessoas WHERE id = %s"
    resultado = ex_comando("GET_BY_ID", comando, (id_usuario,)) #passa o id como uma tupla
    
    if resultado:
        nome_usuario = resultado[0] #resultado é uma tupla, ex: ('Nome',)
    else:
        nome_usuario = "Usuário Desconhecido" #fallback caso não encontre o nome
    return render_template("perfil.html", id_usuario=id_usuario, nome_usuario=nome_usuario)

@user_route.route('/perfil/<int:id_usuario>/sustentabilidade')
def mostrar_sustentabilidade(id_usuario):
    #se o id não estiver em session ou for diferente, o usuário é redirecionado para a tela de login
    if 'user_id' not in session or session['user_id'] != id_usuario:
        return redirect(url_for('user.mostrar_login')) 
    
    #cria a variável comando com o comando para o banco, selecionando a media e classificação
    comando = "SELECT media_final, classificacao_final FROM resultados_sustentabilidade WHERE pessoa_id = %s ORDER BY id DESC LIMIT 1"
    resultado = ex_comando("GET_BY_ID", comando, (id_usuario,)) #passa o id como uma tupla

    #se tiver resultado, as duas variáveis recebem resultado em ordem
    if resultado:
        media_final, classificacao_final = resultado #resultado é uma tupla, ex: (2.5, 'Sustentavel')
    else:
        #se não obter resultado (primeiro acesso), as variáveis recebem 0 e não sustentável
        media_final = 0
        classificacao_final = "Não Sustentável"

    #se for sustentável, exibe a imagem sustentável e a dica, se a média for 3 o usuário recebe o selo
    if classificacao_final == "Sustentável":
        if media_final == 3:
            selo = True
        else: 
            selo = False
        imagem = "/static/img/sust.jpeg"
        dica = "Você está no nível máximo! Continue com seus hábitos sustentáveis para manter esse nível."
    #se for mediano, coloca o selo em false, recebe a imagem de mediano e a dica
    elif classificacao_final == "Mediano":
        selo = False
        imagem = "/static/img/mediano.jpeg"
        dica = "Você está no caminho certo! Tente melhorar seu consumo de água, energia e produção de resíduos."
    #nenhum (não sustentável), coloca o selo em false, recebe a imagem de não sust e a dica
    else:
        selo = False
        imagem = "/static/img/nao-sust.jpeg"
        dica = "Tente rever seus hábitos diários para tornar seu estilo de vida mais sustentável."

    #retorna as variáveis pro front
    return render_template("sustentabilidade.html", id_usuario=id_usuario, media_final=media_final, classificacao_final=classificacao_final, selo=selo, imagem=imagem, dica=dica)

@user_route.route('/perfil/<int:id_usuario>/graficos')
def mostrar_graficos(id_usuario):
    #se o id não estiver em session ou for diferente, o usuário é redirecionado para a tela de login
    if 'user_id' not in session or session['user_id'] != id_usuario:
        return redirect(url_for('user.mostrar_login'))
    
    periodo = request.args.get('periodo', 7) #pega o período selecionado na URL, padrão é 7 dias

    #pesquisa no banco as pontuações e média, filtrando pelo período fornecido
    comando = """
        SELECT data_calculo, pontuacao_agua, pontuacao_energia, pontuacao_residuo, pontuacao_transporte, media_final
        FROM resultados_sustentabilidade
        WHERE pessoa_id = %s
        AND data_calculo >= CURRENT_DATE - INTERVAL %s DAY
        ORDER BY data_calculo DESC
    """
    # Passa id_usuario e periodo como tupla
    resultado = ex_comando("GET", comando, (id_usuario, str(periodo))) #period é passado como string para o INTERVAL

    #inicializa as listas vazias
    datas_formatadas = [] 
    pontuacao_agua = []
    pontuacao_energia = []
    pontuacao_residuo = []
    pontuacao_transporte_lista = []
    media_final = []

    if resultado:
        for item in resultado: # item vem como uma tupla, ex: (datetime.date(2025, 5, 24), 3, 2, 3, 1, 2.25)

            data_calculo = item[0] #data_calculo recebe o primeiro item da tupla(a data) para ser formatada
            datas_formatadas.append(data_calculo.strftime('%d/%m/%y')) #ex 24/05/25
            pontuacao_agua.append(item[1])
            pontuacao_energia.append(item[2])
            pontuacao_residuo.append(item[3])
            pontuacao_transporte_lista.append(item[4])
            media_final.append(item[5])
            #cada variável recebe seu dado de acordo com a ordem de busca

    #retorna as variaveis com os valores pro front
    return render_template(
        "graficos.html", id_usuario=id_usuario, pontuacao_agua=pontuacao_agua, pontuacao_energia=pontuacao_energia, pontuacao_residuo=pontuacao_residuo, pontuacao_transporte=pontuacao_transporte_lista, media_final=media_final,datas=datas_formatadas)

@user_route.route('/perfil/<int:id_usuario>/inserir-dados', methods=['GET'])
def mostrar_inserir_dados(id_usuario):
    #se o id não estiver em session ou for diferente, o usuário é redirecionado para a tela de login
    if 'user_id' not in session or session['user_id'] != id_usuario:
        return redirect(url_for('user.mostrar_login'))
    return render_template("inserir-dados.html", id_usuario=id_usuario)

@user_route.route('/perfil/<int:id_usuario>/inserir-dados', methods=['POST'])
def enviar_dados(id_usuario):
    #se o id não estiver em session ou for diferente, o usuário é redirecionado para a tela de login
    if 'user_id' not in session or session['user_id'] != id_usuario:
        return redirect(url_for('user.mostrar_login')) 
    
    #pega os valores inseridos no form via requisição json
    data = request.json
    agua = data.get('agua')
    energia = data.get('energia')
    residuo = data.get('residuo')
    transporte = data.get('transporte')
    distancia = data.get('distancia')

    #faz o comando para inserir os dados e executa a função para inserir no banco
    comando_inserir = """
        INSERT INTO monitoramento_parametros (
            pessoa_id, data_registro, leitura_atual_agua, leitura_anterior_agua,
            leitura_atual_energia, leitura_anterior_energia, peso_residuo,
            tipo_transporte, distancia_transporte
        ) VALUES (
            %s, CURRENT_DATE, %s, NULL, %s, NULL, %s, %s::tipo_transporte_enum, %s
        )
    """
    #função para inserir no banco
    ex_comando("POST", comando_inserir, (id_usuario, agua, energia, residuo, transporte, distancia))

    #faz o uptade na pontuação de água, maior que 150 recebe 1, entre 110 e 150 recebe 2, se não recebe 3
    comando_update_agua = """
        UPDATE monitoramento_parametros
        SET pontuacao_agua = CASE
            WHEN (leitura_atual_agua - COALESCE(leitura_anterior_agua, 0)) > 150 THEN 1
            WHEN (leitura_atual_agua - COALESCE(leitura_anterior_agua, 0)) BETWEEN 110 AND 150 THEN 2
            ELSE 3
        END
        WHERE pessoa_id = %s AND pontuacao_agua IS NULL;
    """
    #função para inserir no banco
    ex_comando("PUT", comando_update_agua, (id_usuario,))

    #faz o uptade na pontuação de energia, maior que 180 recebe 1, entre 120 e 180 recebe 2, se não recebe 3
    comando_update_energia = """
        UPDATE monitoramento_parametros
        SET pontuacao_energia = CASE
            WHEN (leitura_atual_energia - COALESCE(leitura_anterior_energia, 0)) > 180 THEN 1
            WHEN (leitura_atual_energia - COALESCE(leitura_anterior_energia, 0)) BETWEEN 120 AND 180 THEN 2
            ELSE 3
        END
        WHERE pessoa_id = %s AND pontuacao_energia IS NULL;
    """
    #função para inserir no banco
    ex_comando("PUT", comando_update_energia, (id_usuario,))

    #faz o uptade na pontuação de residuos, maior que 1.2 recebe 1, entre 0.8 e 1.2 recebe 2, se não recebe 3
    comando_update_residuo = """
        UPDATE monitoramento_parametros
        SET pontuacao_residuo = CASE
            WHEN peso_residuo > 1.2 THEN 1
            WHEN peso_residuo BETWEEN 0.8 AND 1.2 THEN 2
            ELSE 3
        END
        WHERE pessoa_id = %s AND pontuacao_residuo IS NULL;
    """
    #função para inserir no banco
    ex_comando("PUT", comando_update_residuo, (id_usuario,))
    
    #faz o uptade na emissão de co2, é multiplicado a distancia com a quantidade de co2 que cada veículo produz
    comando_update_emissao = """
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
        WHERE pessoa_id = %s AND emissao_co2 IS NULL;
    """
    #função para inserir no banco
    ex_comando("PUT", comando_update_emissao, (id_usuario,)) 

    #faz o uptade na pontuação de transporte, maior que 5 recebe 1, entre 2 e 5 recebe 2, se não recebe 3
    comando_update_transporte = """
        UPDATE monitoramento_parametros
        SET pontuacao_transporte = CASE
            WHEN emissao_co2 > 5 THEN 1
            WHEN emissao_co2 BETWEEN 2 AND 5 THEN 2
            ELSE 3
        END
        WHERE pessoa_id = %s AND pontuacao_transporte IS NULL;
    """
    #função para inserir no banco
    ex_comando("PUT", comando_update_transporte, (id_usuario,))

    #faz o comando para inserir as pontuações na tabela resultados, no prório uptade, a média é calculada
    #soma todas as pontuações e divide por 4, >= 2.5 é sustentável, >= 1.5 mediano, abaixo de 1.5 é n sust 
    comando_resultados = """
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
            mp.pessoa_id,
            mp.id AS monitoramento_id,
            mp.data_registro,
            mp.pontuacao_agua,
            mp.pontuacao_energia,
            mp.pontuacao_residuo,
            mp.pontuacao_transporte,
            (mp.pontuacao_agua + mp.pontuacao_energia + mp.pontuacao_residuo + mp.pontuacao_transporte) / 4.0 AS media,
            (CASE
                WHEN (mp.pontuacao_agua + mp.pontuacao_energia + mp.pontuacao_residuo + mp.pontuacao_transporte) / 4.0 >= 2.5 THEN 'Sustentável'
                WHEN (mp.pontuacao_agua + mp.pontuacao_energia + mp.pontuacao_residuo + mp.pontuacao_transporte) / 4.0 >= 1.5 THEN 'Mediano'
                ELSE 'Não Sustentável'
            END)::classificacao_final_enum AS classificacao -- CAST explícito
        FROM monitoramento_parametros mp
        WHERE mp.pessoa_id = %s AND mp.data_registro = CURRENT_DATE AND mp.id NOT IN (
            SELECT rs.monitoramento_id FROM resultados_sustentabilidade rs
            WHERE rs.pessoa_id = %s AND rs.data_calculo = CURRENT_DATE
        );
    """
    #função para inserir no banco
    ex_comando("POST", comando_resultados, (id_usuario, id_usuario)) #passa id_usuario duas vezes

    return jsonify({'message': 'Dados inseridos e resultados calculados com sucesso', 'id_usuario': id_usuario}), 201

@user_route.route('/perfil/<int:id_usuario>/editar-dados', methods=['GET'])
def mostrar_editar_dados(id_usuario):
    #se o id não estiver em session ou for diferente, o usuário é redirecionado para a tela de login
    if 'user_id' not in session or session['user_id'] != id_usuario:
        return redirect(url_for('user.mostrar_login'))
    return render_template("editar-dados.html", id_usuario=id_usuario)

@user_route.route('/perfil/<int:id_usuario>/editar-dados', methods=['PUT'])
def editar_dados(id_usuario):
    #se o id não estiver em session ou for diferente, o usuário é redirecionado para a tela de login
    if 'user_id' not in session or session['user_id'] != id_usuario:
        return redirect(url_for('user.mostrar_login'))
    
    #pega os dados do form via requisição json
    data = request.json
    data_registro = data.get('data_registro') 
    parametro = data.get('parametro') 
    novo_valor = data.get('valor')
    tipo_transporte = data.get('tipo_transporte')
    distancia = data.get('distancia')

    #verifica qual dado foi alterado e insere o novo valor digitado filtrando pela data informada
    if parametro == 'agua':
        comando_editar = """
            UPDATE monitoramento_parametros
            SET leitura_atual_agua = %s
            WHERE pessoa_id = %s AND data_registro = %s;
        """
        ex_comando("PUT", comando_editar, (novo_valor, id_usuario, data_registro))
    elif parametro == 'energia':
        comando_editar = """
            UPDATE monitoramento_parametros
            SET leitura_atual_energia = %s
            WHERE pessoa_id = %s AND data_registro = %s;
        """
        ex_comando("PUT", comando_editar, (novo_valor, id_usuario, data_registro))
    elif parametro == 'residuo':
        comando_editar = """
            UPDATE monitoramento_parametros
            SET peso_residuo = %s
            WHERE pessoa_id = %s AND data_registro = %s;
        """
        ex_comando("PUT", comando_editar, (novo_valor, id_usuario, data_registro))
    elif parametro == 'transporte' and tipo_transporte:
        comando_editar = """
            UPDATE monitoramento_parametros
            SET tipo_transporte = %s::tipo_transporte_enum, -- CAST explícito
                distancia_transporte = %s
            WHERE pessoa_id = %s AND data_registro = %s;
        """
        ex_comando("PUT", comando_editar, (tipo_transporte, distancia, id_usuario, data_registro))
    elif parametro == 'distancia' and distancia:
        comando_editar = """
            UPDATE monitoramento_parametros
            SET distancia_transporte = %s
            WHERE pessoa_id = %s AND data_registro = %s;
        """
        ex_comando("PUT", comando_editar, (distancia, id_usuario, data_registro))
    else:
        return jsonify({'message': 'Parâmetro inválido ou falta de dados'}), 400

    #refaz o calculo da pontuação do parâmetro informado
    if parametro == 'agua':
        comando_update_agua = """
            UPDATE monitoramento_parametros
            SET pontuacao_agua = CASE
                WHEN (leitura_atual_agua - COALESCE(leitura_anterior_agua, 0)) > 150 THEN 1
                WHEN (leitura_atual_agua - COALESCE(leitura_anterior_agua, 0)) BETWEEN 110 AND 150 THEN 2
                ELSE 3
            END
            WHERE pessoa_id = %s AND data_registro = %s;
        """
        ex_comando("PUT", comando_update_agua, (id_usuario, data_registro))

    if parametro == 'energia':
        comando_update_energia = """
            UPDATE monitoramento_parametros
            SET pontuacao_energia = CASE
                WHEN (leitura_atual_energia - COALESCE(leitura_anterior_energia, 0)) > 180 THEN 1
                WHEN (leitura_atual_energia - COALESCE(leitura_anterior_energia, 0)) BETWEEN 120 AND 180 THEN 2
                ELSE 3
            END
            WHERE pessoa_id = %s AND data_registro = %s;
        """
        ex_comando("PUT", comando_update_energia, (id_usuario, data_registro))

    if parametro == 'residuo':
        comando_update_residuo = """
            UPDATE monitoramento_parametros
            SET pontuacao_residuo = CASE
                WHEN peso_residuo > 1.2 THEN 1
                WHEN peso_residuo BETWEEN 0.8 AND 1.2 THEN 2
                ELSE 3
            END
            WHERE pessoa_id = %s AND data_registro = %s;
        """
        ex_comando("PUT", comando_update_residuo, (id_usuario, data_registro))

    if parametro == 'transporte' or parametro == 'distancia':
        comando_update_emissao = """
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
            WHERE pessoa_id = %s AND data_registro = %s;
        """
        ex_comando("PUT", comando_update_emissao, (id_usuario, data_registro))

        comando_update_transporte = """
            UPDATE monitoramento_parametros
            SET pontuacao_transporte = CASE
                WHEN emissao_co2 > 5 THEN 1
                WHEN emissao_co2 BETWEEN 2 AND 5 THEN 2
                ELSE 3
            END
            WHERE pessoa_id = %s AND data_registro = %s;
        """
        ex_comando("PUT", comando_update_transporte, (id_usuario, data_registro))

    #atualiza a tabela de resultados
    comando_update_resultado = """
        UPDATE resultados_sustentabilidade rs
        SET 
            pontuacao_agua = mp.pontuacao_agua,
            pontuacao_energia = mp.pontuacao_energia,
            pontuacao_residuo = mp.pontuacao_residuo,
            pontuacao_transporte = mp.pontuacao_transporte,
            media_final = ROUND((mp.pontuacao_agua + mp.pontuacao_energia + mp.pontuacao_residuo + mp.pontuacao_transporte) / 4.0, 2),
            classificacao_final = (CASE
                WHEN ROUND((mp.pontuacao_agua + mp.pontuacao_energia + mp.pontuacao_residuo + mp.pontuacao_transporte) / 4.0, 2) >= 2.5 THEN 'Sustentável'
                WHEN ROUND((mp.pontuacao_agua + mp.pontuacao_energia + mp.pontuacao_residuo + mp.pontuacao_transporte) / 4.0, 2) >= 1.5 THEN 'Mediano'
                ELSE 'Não Sustentável'
            END)::classificacao_final_enum -- CAST explícito
        FROM monitoramento_parametros mp
        WHERE rs.pessoa_id = mp.pessoa_id
          AND rs.data_calculo = mp.data_registro
          AND rs.pessoa_id = %s
          AND rs.data_calculo = %s;
    """
    #passa os parâmetros para a cláusula WHERE principal
    ex_comando("PUT", comando_update_resultado, (
        id_usuario, data_registro, #WHERE principal
        id_usuario, data_registro  #WHERE principal
    ))

    return jsonify({'message': 'Dado atualizado com sucesso e pontuação recalculada.', 'id_usuario': id_usuario, 'data_registro': data_registro, 'parametro': parametro}), 200
