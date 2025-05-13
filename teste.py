# Converte letra para número (A=1, ..., Z=26)
def letra_para_numero(letra):
    return ord(letra.upper()) - 64

# Converte número para letra (1=A, ..., 26=Z)
def numero_para_letra(numero):
    return chr(numero + 64)

# Matriz codificadora
matriz = [[5, 4], [3, 3]]

# matriz inversa módulo 26
def inversa_matriz_2x2(matriz):
    # Determinante da matriz
    det = matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
    det = det % 26
    
    # Inverso do determinante módulo 26
    det_inverso = pow(det, -1, 26)

    # Matriz adjunta
    adj = [[matriz[1][1], -matriz[0][1]], [-matriz[1][0], matriz[0][0]]]

    # Matriz inversa
    inversa = [
        [det_inverso * adj[0][0] % 26, det_inverso * adj[0][1] % 26],
        [det_inverso * adj[1][0] % 26, det_inverso * adj[1][1] % 26]
    ]

    return inversa


def criptografar_hill(texto):
    texto = texto.upper().replace(" ", "")  # Remove espaços e deixa maiúsculo

    # Se o texto for ímpar, repete a última letra
    if len(texto) % 2 != 0:
        texto += texto[-1]

    resultado = ""

    for i in range(0, len(texto), 2):
        par = [letra_para_numero(texto[i]), letra_para_numero(texto[i+1])]

        # Multiplica a matriz pelo par
        c1 = (matriz[0][0]*par[0] + matriz[0][1]*par[1]) % 26
        c2 = (matriz[1][0]*par[0] + matriz[1][1]*par[1]) % 26

        # Corrige caso dê zero, que deve ser mapeado para 26
        if c1 == 0:
            c1 = 26
        if c2 == 0:
            c2 = 26

        resultado += numero_para_letra(c1) + numero_para_letra(c2)

    return resultado


def descriptografar_hill(texto_criptografado):
    inversa = inversa_matriz_2x2(matriz)
    texto_criptografado = texto_criptografado.upper().replace(" ", "")  # Remove espaços e deixa maiúsculo

    resultado = ""

    for i in range(0, len(texto_criptografado), 2):
        par = [letra_para_numero(texto_criptografado[i]), letra_para_numero(texto_criptografado[i+1])]

        # Multiplica a matriz inversa pelo par
        p1 = (inversa[0][0] * par[0] + inversa[0][1] * par[1]) % 26
        p2 = (inversa[1][0] * par[0] + inversa[1][1] * par[1]) % 26

        # Corrige caso dê zero, que deve ser mapeado para 26
        if p1 == 0:
            p1 = 26
        if p2 == 0:
            p2 = 26

        resultado += numero_para_letra(p1) + numero_para_letra(p2)

    # Se o texto foi criptografado com uma letra duplicada, remove a última letra
    if len(resultado) > 1 and resultado[-1] == resultado[-2]:
        resultado = resultado[:-1]  # Remove a última letra duplicada

    return resultado

# Exemplo de uso
texto = input("Digite o texto a ser criptografado: ")
texto_criptografado = criptografar_hill(texto)
print(f"Texto original: {texto}")
print(f"Texto criptografado: {texto_criptografado}")

texto_descriptografado = descriptografar_hill(texto_criptografado)
print(f"Texto descriptografado: {texto_descriptografado}")
