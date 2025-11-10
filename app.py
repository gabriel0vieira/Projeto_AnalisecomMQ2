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
st.title("💨 Monitoramento Inteligente de Gases com ESP32 e Sensor MQ-2")

st.markdown("""
Bem-vindo ao painel interativo de **análise e monitoramento ambiental**.  
Aqui você pode acompanhar a evolução das leituras do sensor MQ-2, entender padrões e identificar situações de risco.
""")

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
    st.header("📋 Resumo das Leituras")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Registros", len(df))
    col2.metric("Média leitura_volts", f"{df['v_adc'].mean():.3f}")
    col3.metric("Máx. intensidade_gas", int(df["raw_value"].max()))
    col4.metric("Alarmes Ativos", df["alarme"].sum())

    st.markdown("### Distribuição dos Valores Captados")
    fig = px.histogram(df, x="raw_value", nbins=30, title="Distribuição de Intensidade dos Gases", color_discrete_sequence=["#0083B8"])
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    🔍 **Interpretação:**  
    O histograma mostra a frequência dos valores captados pelo sensor MQ-2.  
    Concentrações mais altas podem indicar momentos de presença de fumaça ou gases inflamáveis.
    """)

# ---------------------------
# ABA 2 - ANÁLISE TEMPORAL
# ---------------------------
with abas[1]:
    st.header("📈 Análise de Tendência Temporal")

    df["media_movel"] = df["v_adc"].rolling(window=10).mean()

    fig2 = px.line(df, x="timestamp", y=["v_adc", "media_movel"],
                   labels={"timestamp": "Tempo", "value": "Leitura (v_adc)"},
                   title="Evolução das Leituras no Tempo",
                   color_discrete_map={"v_adc": "#1f77b4", "media_movel": "#d62728"})
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    🧠 **Insight Analítico:**  
    A linha vermelha representa a **média móvel de 10 amostras**, ajudando a suavizar ruídos e identificar **tendências**.  
    Oscilações bruscas podem indicar **variação rápida na concentração de gases**, exigindo atenção.
    """)

    st.subheader("Correlação entre Variáveis")
    fig_corr, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig_corr)

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

