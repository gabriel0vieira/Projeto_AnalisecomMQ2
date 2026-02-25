import streamlit as st
import pandas as pd
import psycopg2
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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
abas = st.tabs(["📊 Visão Geral", "📈 Correlação entre Variáveis", "📊 Estatísticas Gerais", "ℹ️ Sobre o Projeto"])


# ============================================================
# 📊 ABA 1 - VISÃO GERAL
# ============================================================
with abas[0]:
    st.subheader("📦 Distribuição dos valores do sensor MQ-2")

    # Histograma
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(df['raw_value'], bins=30, kde=True, ax=ax)
    ax.set_title("Distribuição dos valores do sensor MQ-2")
    ax.set_xlabel("Valor bruto (raw_value)")
    ax.set_ylabel("Frequência")
    st.pyplot(fig)

    # Boxplot (adicionado)
    st.subheader("📌 Boxplot da leitura bruta")
    fig2, ax2 = plt.subplots(figsize=(6, 3.5))
    sns.boxplot(x=df["raw_value"], ax=ax2)
    ax2.set_title("Distribuição da leitura bruta (raw_value)")
    ax2.set_xlabel("Valor bruto (raw_value)")
    st.pyplot(fig2)

    st.markdown("""
    🔍 **Interpretação:**  
    O histograma e o boxplot mostram a dispersão das leituras.  
    Valores muito altos podem indicar momentos de risco, fumaça ou gases inflamáveis.
    """)


# ============================================================
# 📈 ABA 2 - ANÁLISE TEMPORAL
# ============================================================
with abas[1]:
    st.header("📈 Correlação entre Variáveis")

    fig, ax = plt.subplots(figsize=(6, 4))
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
    Uma relação clara entre raw_value e tensão indica que o sensor está funcionando de forma consistente.
    """)


# ============================================================
# 📊 ABA 3 - ESTATÍSTICAS GERAIS
# ============================================================
with abas[2]:
    st.header("📊 Estatísticas Gerais")

    total = len(df)
    alarme_count = df['alarme'].sum()
    media_tensao = df['v_adc'].mean()
    max_tensao = df['v_adc'].max()
    max_raw = df['raw_value'].max()
    valor_atual = df["raw_value"].iloc[-1]

    col1, col2 = st.columns(2)

    # ----------- Coluna 1: Estatísticas -----------
    with col1:
        st.subheader("📘 Resumo dos Dados")
        st.write(f"**Total de leituras:** {total}")
        st.write(f"**Leituras com alarme:** {alarme_count} ({alarme_count/total*100:.2f}%)")
        st.write(f"**Média de tensão:** {media_tensao:.2f} V")
        st.write(f"**Máximo de tensão:** {max_tensao:.2f} V")
        st.write(f"**Máximo RAW detectado:** {max_raw}")

    # ----------- Coluna 2: Indicador de risco -----------
    with col2:
        st.subheader("🚨 Indicador de Risco (RAW)")

        # thresholds
        t1 = 500
        t2 = 1000

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge",
            value=valor_atual,
            gauge={
                'shape': "bullet",
                'axis': {'range': [0, max_raw]},
                'bar': {'color': "black"},
                'steps': [
                    {'range': [0, t1], 'color': "lightgreen"},
                    {'range': [t1, t2], 'color': "yellow"},
                    {'range': [t2, max_raw], 'color': "red"},
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.7,
                    'value': valor_atual
                }
            }
        ))

        fig_gauge.update_layout(height=180, margin=dict(l=10, r=10, t=20, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)


# ============================================================
# ℹ️ ABA 4 - SOBRE
# ============================================================
with abas[3]:
    st.header("ℹ️ Sobre o Projeto")
    st.markdown('''
O projeto **Monitoramento de Gases com ESP32 e Sensor MQ-2** foi desenvolvido para acompanhar, em tempo real,
a presença de gases inflamáveis e fumaça no ambiente.  

**Componentes Utilizados:**
- ESP32  
- MQ-2  
- Buzzer  
- PostgreSQL  

**Objetivo:** Monitorar o ambiente e ajudar na prevenção de riscos.  
**Desenvolvido por:** *Gabriel de Almeida Vieira*  
**Disciplina:** HMDC680 - Projeto Integrador Aplicado em CD & IA II  
''')









