#variável com o alfabeto e numeros
alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

#tamanho do alfabeto para usar no módulo
MOD = len(alfabeto)

#matriz usada para criptografar
matriz = [[5, 17], [4, 15]]

#inversa da matriz no módulo MOD (para descriptografar)
inversa = [[33, 13], [20, 11]]

#função para converter letra para número (retorna o numero da posição que está na variável alfabeto)
def letra_para_numero(letra):
    return alfabeto.index(letra.upper())

#função que converte número para letra (retorna a letra na variável alfabeto)
def numero_para_letra(numero):
    return alfabeto[numero % MOD] #divide por mod pra garantir que so vá até 35



def criptografar_hill(texto_original):
    texto = texto_original.upper() #garante que o texto esteja em maiúsculas

    #se o texto for impar, o ultimo caractere é repetido
    if len(texto) % 2 != 0:
        texto += texto[-1]

    resultado = ""

    for i in range(0, len(texto), 2): #pega 2 caracteares por vez
        #converte o par de letras atual em números
        par_numeros = [letra_para_numero(texto[i]), letra_para_numero(texto[i+1])]

        #calcula o primeiro número cifrado (linha1_matriz * par_numeros) % MOD
        c1 = (matriz[0][0]*par_numeros[0] + matriz[0][1]*par_numeros[1]) % MOD

        #faz o mesmo com o segundo número, mas com a linha2
        c2 = (matriz[1][0]*par_numeros[0] + matriz[1][1]*par_numeros[1]) % MOD

        #converte os números cifrados de volta para letras e coloca em resultado
        resultado += numero_para_letra(c1) + numero_para_letra(c2)

    return resultado


def descriptografar_hill(texto_criptografado):
        
    resultado = ""
    for i in range(0, len(texto_criptografado), 2):
        #converte o par de letras criptografadas em seus equivalentes numeros.
        par_numeros = [letra_para_numero(texto_criptografado[i]), letra_para_numero(texto_criptografado[i+1])]

        # Calcula o primeiro número (linha1_matriz_inversa * par_numeros_cifrados) % MOD
        p1 = (inversa[0][0]*par_numeros[0] + inversa[0][1]*par_numeros[1]) % MOD

        #faz a mesma coisa, mas com a linha2
        p2 = (inversa[1][0]*par_numeros[0] + inversa[1][1]*par_numeros[1]) % MOD

        #converte os números decifrados de volta para letras e coloca em resultado.
        resultado += numero_para_letra(p1) + numero_para_letra(p2)

    return resultado
