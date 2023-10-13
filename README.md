![image](https://github.com/Zenox-AI/Teste-Backend-Golang/assets/144921896/480d7d7d-aa5b-4f00-b5a0-b9d4e740fc99)


# Desafio Backend Python

**Objetivo:** O sistema consiste em um crawler que coleta dados de países de um site e os envia para uma fila no Kafka, no qual pode ser visualizado através de uma aplicação feita com streamlit.

## Detalhes tecnicos

**Funcionamento do Crawler**

 - O crawler é executado manualmente, coletando os dados de países do site https://www.scrapethissite.com/pages/simple/ e os envia para uma fila no Kafka.
 - O crawler conta com um sistema de proxies rotativos, que são utilizados para evitar o bloqueio do site. (OBS: O crawler pode apresentar lentidão devido a utilização de proxies gratuitos)
 - O crawler conta com um sistema de User-Agent rotativos, que também são utilizados para evitar o bloqueio do site.

**Integração com Kafka**:

 - O crawler envia os dados para uma fila no Kafka, que é consumida pela aplicação feita com streamlit.
 - O Kafka foi configurado utilizando o docker-compose, para facilitar a execução do projeto.

**Aplicação com streamlit**:

 - A aplicação feita com streamlit consome os dados da fila no Kafka e os exibe em uma tabela além de apresentar um gráfico demonstrando o países com maiores densidades demográficas.

## Instalação

**Pré-requisitos:**

 - Docker Compose
 - Python 3
 - Pip
 - Git

**Instalação:**

 - Clone o repositório
    - `git clone git@github.com:MauroTony/Teste-Backend-Python.git`
    - `cd Teste-Backend-Python`
    - `git checkout main`
 - Execute o docker-compose
    - `docker-compose up -d`
 - Instale as dependências do projeto
    - `pip install -r requirements.txt`
 - Configue as variáveis de ambiente
    - Valide que a .env existe na raiz do projeto
    - Valide a existencia da variável de ambiente KAFKA_HOST e KAFKA_PORT e configure-as caso necessário
   
**Execução:**

 - Inicialize o kafka
    - `docker-compose up -d`
 - Inicialize o streamlit
    - `streamlit run streamlit-frontend.py`
 - Execute o crawler
    - `cd scraping`
    - `python runCrawler.py`
 
