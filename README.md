🔥 Monitoramento Inteligente de Gases com ESP32 e Sensor MQ-2
🌐 Dashboard Online

🚀 Acessar Dashboard Online

🎯 Sobre o Projeto

Este projeto foi desenvolvido para monitorar a presença de gases inflamáveis e fumaça utilizando ESP32 e o sensor MQ-2.

Os dados coletados são armazenados em PostgreSQL e analisados através de um dashboard interativo desenvolvido com Streamlit.

O sistema permite acompanhamento em tempo real e análise estatística das leituras do sensor.

🛠 Tecnologias Utilizadas

Python

Streamlit

PostgreSQL

Pandas

Seaborn

Matplotlib

Plotly

ESP32

Sensor MQ-2

📊 Funcionalidades do Dashboard
📌 1. Visão Geral

Histograma da distribuição das leituras do sensor

Boxplot para análise de dispersão

📌 2. Correlação entre Variáveis

Gráfico de dispersão entre leitura bruta (raw_value) e tensão (v_adc)

📌 3. Estatísticas Gerais

Total de leituras registradas

Quantidade de alarmes acionados

Média e máximo de tensão

Indicador visual de risco (Gauge Chart interativo)

📌 4. Informações do Projeto

Componentes utilizados

Descrição técnica do sistema

🧠 Estrutura do Projeto

api.py → Aplicação principal (Streamlit)

requirements.txt → Dependências do projeto

▶️ Como Executar Localmente

Instale as dependências:

pip install -r requirements.txt

Execute o projeto:

streamlit run api.py
🗄 Banco de Dados

Os dados são armazenados em PostgreSQL e consultados via psycopg2.
As credenciais foram configuradas para ambiente acadêmico.

👨‍💻 Autor

Gabriel de Almeida Vieira

Projeto desenvolvido para a disciplina Projeto Integrador Aplicado em Ciência de Dados e IA II.
