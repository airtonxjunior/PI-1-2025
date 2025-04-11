use monitoramentosustentabilidade;

CREATE TABLE pessoas(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
    );
    
    CREATE TABLE monitoramento_parametros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pessoa_id INT NOT NULL,
    data_registro DATE NOT NULL,

    leitura_atual_agua DECIMAL(10,2),
    leitura_anterior_agua DECIMAL(10,2),
    pontuacao_agua TINYINT,

    leitura_atual_energia DECIMAL(10,2),
    leitura_anterior_energia DECIMAL(10,2),
    pontuacao_energia TINYINT,

    peso_residuo DECIMAL(5,2),
    pontuacao_residuo TINYINT,

    tipo_transporte ENUM('carro', 'moto', 'onibus', 'metro', 'bicicleta', 'caminhada'),
    distancia_transporte DECIMAL(6,2),
    emissao_co2 DECIMAL(6,2),
    pontuacao_transporte TINYINT,

    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
);

CREATE TABLE resultados_sustentabilidade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pessoa_id INT NOT NULL,
    monitoramento_id INT NOT NULL,
    data_calculo DATE NOT NULL,

    pontuacao_agua TINYINT NOT NULL,
    pontuacao_energia TINYINT NOT NULL,
    pontuacao_residuo TINYINT NOT NULL,
    pontuacao_transporte TINYINT NOT NULL,

    media_final DECIMAL(3,2) NOT NULL,
    classificacao_final ENUM('Não Sustentável', 'Mediano', 'Sustentável') NOT NULL,

    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id),
    FOREIGN KEY (monitoramento_id) REFERENCES monitoramento_parametros(id)
);

INSERT INTO pessoas (nome, email, senha) VALUES
('Junior', 'junior@email.com', 'senha123'),
('Ane', 'ane@email.com', 'senha456');

INSERT INTO monitoramento_parametros (pessoa_id,data_registro,leitura_atual_agua,leitura_anterior_agua,leitura_atual_energia,leitura_anterior_energia,peso_residuo,tipo_transporte,distancia_transporte)
VALUES
(1,'2025-04-09', 380, 200, 17, 12, 0.9, 'carro', 60),
(2, '2025-04-09', 90, NULL, 3.5, NULL, 0.6, 'onibus', 80);


UPDATE monitoramento_parametros
SET pontuacao_agua = CASE
    WHEN (leitura_atual_agua - COALESCE(leitura_anterior_agua, 0)) > 150 THEN 1
    WHEN (leitura_atual_agua - COALESCE(leitura_anterior_agua, 0)) BETWEEN 110 AND 150 THEN 2
    ELSE 3
END
WHERE pontuacao_agua IS NULL;


UPDATE monitoramento_parametros
SET pontuacao_energia = CASE
    WHEN (leitura_atual_energia - COALESCE(leitura_anterior_energia, 0)) > 180 THEN 1
    WHEN (leitura_atual_energia - COALESCE(leitura_anterior_energia, 0)) BETWEEN 120 AND 180 THEN 2
    ELSE 3
END
WHERE pontuacao_energia IS NULL;

UPDATE monitoramento_parametros
SET pontuacao_residuo = CASE
    WHEN peso_residuo > 1.2 THEN 1
    WHEN peso_residuo BETWEEN 0.8 AND 1.2 THEN 2
    ELSE 3
END
WHERE pontuacao_residuo IS NULL;

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
WHERE emissao_co2 IS NULL;

UPDATE monitoramento_parametros
SET pontuacao_transporte = CASE
    WHEN emissao_co2 > 5 THEN 1
    WHEN emissao_co2 BETWEEN 2 AND 5 THEN 2
    ELSE 3
END
WHERE pontuacao_transporte IS NULL;


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


SELECT * FROM resultados_sustentabilidade;


