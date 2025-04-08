use monitoramentosustentabilidade;

CREATE TABLE pessoas(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
    );
    

CREATE TABLE consumo_agua (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pessoa_id INT NOT NULL, 
    leitura_atual DECIMAL(10,2) NOT NULL,
    leitura_anterior DECIMAL(10,2),
    data_leitura DATE NOT NULL,
    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
);

CREATE TABLE consumo_energia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pessoa_id INT NOT NULL,
    leitura_atual DECIMAL(10,2) NOT NULL,
    leitura_anterior DECIMAL(10,2),
    data_leitura DATE NOT NULL,
    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
);

CREATE TABLE residuos_nao_reciclaveis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pessoa_id INT NOT NULL,
    peso DECIMAL(5,2) NOT NULL,
    data_registro DATE NOT NULL,
    classificacao ENUM('Não Sustentável', 'Mediano', 'Sustentável') NOT NULL,
    pontuacao TINYINT NOT NULL,
    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
);

CREATE TABLE transportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pessoa_id INT NOT NULL,
    tipo ENUM('carro', 'moto', 'onibus', 'metro', 'bicicleta', 'caminhada') NOT NULL,
    distancia DECIMAL(6,2) NOT NULL,
    data_registro DATE NOT NULL,
    emissao_co2 DECIMAL(6,2),
    classificacao ENUM('Não Sustentável', 'Mediano', 'Sustentável'),
    pontuacao TINYINT,
    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
);

CREATE TABLE resultados_sustentabilidade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pessoa_id INT NOT NULL,
    data_calculo DATE NOT NULL,
    pontuacao_agua TINYINT NOT NULL,
    pontuacao_energia TINYINT NOT NULL COMMENT,
    pontuacao_residuos TINYINT,
    pontuacao_transporte TINYINT NOT NULL COMMENT,
    media_final DECIMAL(3,2) NOT NULL,
    classificacao_final ENUM('Não Sustentável', 'Mediano', 'Sustentável') NOT NULL,
    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
);

CREATE TABLE resultados_sustentabilidade (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pessoa_id INT NOT NULL,
    data_calculo DATE NOT NULL,
    consumo_agua_id INT NOT NULL,
    consumo_energia_id INT NOT NULL,
    residuos_id INT NOT NULL,
    transporte_id INT NOT NULL,
    pontuacao_agua TINYINT NOT NULL,
    pontuacao_energia TINYINT NOT NULL,
    pontuacao_residuos TINYINT NOT NULL,
    pontuacao_transporte TINYINT NOT NULL,
    media_final DECIMAL(3,2) NOT NULL,
    classificacao_final ENUM('Não Sustentável', 'Mediano', 'Sustentável') NOT NULL,
    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id),
    FOREIGN KEY (consumo_agua_id) REFERENCES consumo_agua(id),
    FOREIGN KEY (consumo_energia_id) REFERENCES consumo_energia(id),
    FOREIGN KEY (residuos_id) REFERENCES residuos_nao_reciclaveis(id),
    FOREIGN KEY (transporte_id) REFERENCES transportes(id)
);
