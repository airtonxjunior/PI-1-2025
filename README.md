🌿 GreenTech: Sistema de Monitoramento de Sustentabilidade
Um sistema web desenvolvido para ajudar usuários a monitorar e visualizar seus hábitos de consumo de água, energia, resíduos e transporte, calculando uma pontuação de sustentabilidade e oferecendo insights para um estilo de vida mais ecológico.

✨ Funcionalidades
Cadastro e Login de Usuários: Sistema de autenticação seguro.

Inserção de Dados de Consumo: Registro de consumo de água, energia, peso de resíduos, tipo de transporte e distância percorrida.

Cálculo de Pontuação de Sustentabilidade: Baseado nos dados inseridos, o sistema calcula uma pontuação individual para cada categoria (água, energia, resíduo, transporte) e uma média final.

Classificação de Sustentabilidade: Classifica o usuário como "Não Sustentável", "Mediano" ou "Sustentável" com base na média final.

Visualização de Resultados:

Tela de Sustentabilidade: Exibe a média final e a classificação, com imagens e dicas personalizadas.

Gráficos: Apresenta a evolução das pontuações e da média final ao longo do tempo (7, 30 ou 365 dias).

Edição de Dados: Permite que o usuário edite registros de consumo existentes.

🚀 Tecnologias Utilizadas
Backend: Python 3.x com Flask

Banco de Dados: PostgreSQL (Hospedado no Render)

psycopg2-binary: Driver Python para PostgreSQL

PyMySQL: Driver Python para MySQL (usado apenas para desenvolvimento local como fallback)

Servidor de Aplicação: Gunicorn

Gerenciamento de Dependências: pip e requirements.txt

Controle de Versão: Git e GitHub

Hospedagem: Render (Serviço Web e PostgreSQL)

Criptografia: Hill Cipher (para senhas)

Frontend: HTML, CSS, JavaScript

🚧 Desafios Superados
Este projeto foi uma jornada de aprendizado intenso, especialmente nos desafios de deploy e compatibilidade de ambiente:

Migração de Banco de Dados: Transição de MySQL para PostgreSQL, exigindo a substituição do driver (PyMySQL para psycopg2-binary) e adaptação de sintaxes SQL específicas (como CURDATE() para CURRENT_DATE, INTERVAL e a sintaxe de UPDATE com JOIN).

Tratamento de Tipos ENUM: O PostgreSQL é rigoroso com tipos ENUM. Foi necessário adicionar CASTs explícitos (::tipo_enum) nas consultas SQL para garantir a correta inserção e atualização de dados.

Criação de Tabelas em Ambiente Restrito: Devido à limitação de acesso ao shell em planos gratuitos do Render, foi implementada uma lógica no database.py para criar as tabelas automaticamente (CREATE TABLE IF NOT EXISTS) na inicialização do aplicativo.

Depuração de Logs: Análise contínua de logs de deploy e runtime para identificar e resolver erros de conexão, importação de módulos e sintaxe SQL.

--Configuração e Execução Local--
Para rodar o projeto em sua máquina local, siga os passos abaixo:

Pré-requisitos
Python 3.x instalado

Git instalado

MySQL Server (ou outro banco de dados compatível com PyMySQL para desenvolvimento local)

Banco de dados monitoramentosustentabilidade criado no seu MySQL local.

Passos
Clone o Repositório:

git clone https://github.com/airtonxjunior/PI-1-2025.git
cd PI-1-2025

Crie e Ative o Ambiente Virtual:

python -m venv venv
# No Windows (PowerShell):
.\venv\Scripts\activate
# No Linux/macOS (ou WSL):
source venv/bin/activate

Se encontrar um erro de "política de execução" no PowerShell, execute Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass e tente ativar novamente.

Instale as Dependências:

pip install -r requirements.txt

O database.py está configurado para usar PyMySQL automaticamente em ambiente local.

Execute o Aplicativo Flask:

flask run

O aplicativo estará disponível em http://127.0.0.1:5000/. As tabelas serão criadas automaticamente no seu MySQL local na primeira execução.

--Deploy no Render--
Este projeto está configurado para deploy contínuo no Render. As principais configurações são:

Serviço Web:

Build Command: pip install -r requirements.txt

Start Command: gunicorn main:app

Variáveis de Ambiente: DATABASE_URL (fornecida pelo Render PostgreSQL), PYTHON_VERSION (ex: 3.11.11).

Banco de Dados: PostgreSQL (criado como um serviço separado no Render).

Criação de Tabelas: A função criar_tabelas_se_nao_existirem() no database.py garante que as tabelas e tipos ENUM sejam criados automaticamente no banco de dados do Render na primeira inicialização do serviço web.

Link do Projeto Hospedado: https://greentech-v12l.onrender.com