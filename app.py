import streamlit as st
import pandas as pd
import psycopg2
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# ---------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------
st.set_page_config(page_title="Monitoramento de Gases - ESP32", layout="wide")
st.title("Monitoramento Inteligente de Gases com ESP32 e Sensor MQ-2")


# ---------------------------
# FUNÇÃO PARA CARREGAR DADOS
# ---------------------------
@st.cache_data
def carregar_dados():
    conn = psycopg2.connect(
        host="dataiesb.iesbtech.com.br",
        dbname="2412120027_Gabriel",
        user="2412120027_Gabriel",
        password="2412120027_Gabriel"
    )
    query = "SELECT * FROM sensores_schema.mq2_data ORDER BY timestamp;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = carregar_dados()

# ---------------------------
# CRIAÇÃO DAS ABAS
# ---------------------------
abas = st.tabs(["📊 Visão Geral", "📈 Análise Temporal", "🔥 Alertas e Riscos", "ℹ️ Sobre o Projeto"])

# ---------------------------
# ABA 1 - VISÃO GERAL
# ---------------------------
with abas[0]:

    st.subheader("Distribuição dos valores do sensor MQ-2")

    fig, ax = plt.subplots(figsize=(6, 3))   # <-- tamanho reduzido

    sns.histplot(df['raw_value'], bins=30, kde=True, ax=ax)

    ax.set_title("Distribuição dos valores do sensor MQ-2")
    ax.set_xlabel("Valor bruto (raw_value)")
    ax.set_ylabel("Frequência")

    st.pyplot(fig)

    st.markdown("""
    🔍 **Interpretação:**  
    O histograma mostra a frequência dos valores captados pelo sensor MQ-2.  
    Concentrações mais altas podem indicar momentos de presença de fumaça ou gases inflamáveis.
    """)

# ---------------------------
# ABA 2 - ANÁLISE TEMPORAL
# ---------------------------
with abas[1]:
    st.header("📈 Correlação entre Variáveis")

    fig, ax = plt.subplots(figsize=(5, 3))

    sns.scatterplot(
        data=df,
        x='raw_value',
        y='v_adc',
        alpha=0.6,
        ax=ax
    )

    ax.set_title('Relação entre leitura bruta e tensão (v_adc)')
    ax.set_xlabel('Valor bruto (raw_value)')
    ax.set_ylabel('Tensão (V)')

    st.pyplot(fig)

    st.markdown("""
    📊 **Análise de Correlação:**  
    Este mapa mostra o grau de relação entre as variáveis numéricas.  
    Correlações positivas fortes podem indicar sensores redundantes ou padrões consistentes de leitura.
    """)

# ---------------------------
# ABA 3 - ALERTAS E RISCOS
# ---------------------------
with abas[2]:
    st.header("🚨 Monitoramento de Alertas")

    df_alarm = df[df["alarme"] == True]
    st.metric("Total de Leituras com Alarme", len(df_alarm))

    if len(df_alarm) > 0:
        fig3 = px.scatter(df_alarm, x="timestamp", y="v_adc",
                          color="alarme", title="Momentos de Alarme Ativo",
                          color_discrete_map={True: "red"})
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("✅ Nenhum alarme detectado nas leituras atuais.")

    alarme_counts = df["alarme"].value_counts()
    st.bar_chart(alarme_counts)

    st.markdown("""
    ⚠️ **Interpretação:**  
    Cada ponto vermelho indica um momento em que o sistema **acionou o alarme**.  
    É importante monitorar a frequência desses eventos para **avaliar a segurança do ambiente**.
    """)

# ---------------------------
# ABA 4 - SOBRE
# ---------------------------
with abas[3]:
    st.header("ℹ️ Sobre o Projeto")
    st.markdown('''
O projeto **Monitoramento de Gases com ESP32 e Sensor MQ-2** foi desenvolvido para acompanhar, em tempo real, a presença de gases inflamáveis e fumaça no ambiente.  

**Componentes Utilizados:**
- ESP32: Microcontrolador responsável pela leitura e transmissão dos dados.
- MQ-2: Sensor que detecta gases como GLP, CO e fumaça.
- Buzzer: Emite alerta sonoro quando o limite de segurança é ultrapassado.
- PostgreSQL: Banco de dados para armazenamento e análise histórica.

**Objetivo:**  
Fornecer uma ferramenta visual e analítica para monitoramento ambiental, contribuindo para **segurança e prevenção de riscos**.

**Desenvolvido por:** *Gabriel de Almeida Vieira*  
**Disciplina:** HMDC680 - Projeto Integrador Aplicado em CD & IA II  
''')









