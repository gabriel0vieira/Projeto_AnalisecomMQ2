import streamlit as st
import pandas as pd
import psycopg2
import seaborn as sns
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Monitoramento de Gases - ESP32", layout="wide")

st.title("💨 Monitoramento de Gases com ESP32 e Sensor MQ-2")

# Função para carregar dados do PostgreSQL
@st.cache_data
def carregar_dados():
    conn = psycopg2.connect(
        host="dataiesb.iesbtech.com.br",
        dbname="2412120027_Gabriel",
        user="2412120027_Gabriel",
        password="2412120027_Gabriel"
    )
    query = "SELECT * FROM sensores_schema.mq2_data;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = carregar_dados()

# Criar abas
abas = st.tabs(["📋 Dados", "📈 Gráficos", "🚨 Alarmes", "ℹ️ Sobre o Projeto"])

# Aba 1 - Dados
with abas[0]:
    st.subheader("📋 Últimas Leituras do Sensor")
    st.dataframe(df.tail(20))
    st.write(f"Total de leituras: {len(df)}")

# Aba 2 - Gráficos
with abas[1]:
    st.subheader("📊 Distribuição dos Valores (raw_value)")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    sns.histplot(df["raw_value"], bins=30, kde=True, ax=ax1)
    st.pyplot(fig1)

    st.subheader("📈 Tendência Temporal (v_adc)")
    df["media_movel"] = df["v_adc"].rolling(window=10).mean()
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(df["timestamp"], df["v_adc"], label="Leitura Original", alpha=0.5)
    ax2.plot(df["timestamp"], df["media_movel"], color="red", label="Média Móvel (10 amostras)")
    ax2.legend()
    st.pyplot(fig2)

# Aba 3 - Alarmes
with abas[2]:
    st.subheader("🚨 Leituras com Alarme Ativo")
    df_alarm = df[df["alarme"] == True]
    st.dataframe(df_alarm.tail(10))

    st.subheader("Proporção de Leituras com Alarme")
    alarme_counts = df["alarme"].value_counts()
    st.bar_chart(alarme_counts)

    st.subheader("Correlação entre Variáveis")
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax3)
    st.pyplot(fig3)

# Aba 4 - Sobre
with abas[3]:
    st.markdown('''
    ### ℹ️ Sobre o Projeto
    Este dashboard apresenta os dados coletados pelo sistema de **Monitoramento de Gases com ESP32 e Sensor MQ-2**.

    **Componentes principais:**
    - ESP32: microcontrolador responsável pela coleta e envio dos dados.
    - Sensor MQ-2: detecta gases inflamáveis e fumaça.
    - Buzzer: dispara um alarme sonoro quando o limite é ultrapassado.
    - Banco de Dados PostgreSQL: armazena todas as leituras para análise posterior.

    **Desenvolvido por:** Gabriel de Almeida Vieira  
    **Disciplina:** HMDC680 - Projeto Integrador Aplicado em CD & IA II  
    ''')
