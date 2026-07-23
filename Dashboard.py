# Importando bibliotecas #
import streamlit as st
import pandas as pd
import plotly.express as px

# Definindo configurações de layout, titulo e fivicon da página #
st.set_page_config(
    page_title="Dashboard Pegasus",
    page_icon="📊",
    layout="wide"
)

# Titulo principal e subtítulo do Dashboard #
st.title("Dashboard de Prospecção - Pegasus")
st.markdown("**Análise dos Leads do Processo Seletivo**")

# Etapa que os Dados da planilha são carregados #
planilha = "Dados.xlsx"
# DataFrame #
df = pd.read_excel(
    planilha,
    sheet_name="Pipeline Prospecção 100 Leads",
    header=3
)

# Verifica se os dados da planilha foram carregados corretamente #
st.subheader("Prévia dos dados")
# df.head() exibe somente uma amostra de Dados #
st.dataframe(df)

# Criação dos 'cartões' KPIs (Indicador Chave de Desempenho) #
st.subheader("Indicadores")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Leads", len(df))

with col2:
    st.metric("Segmentos", df["Segmento"].nunique())

with col3:
    st.metric("Cidades", df["Cidade/UF"].nunique())

with col4:
    st.metric("Executivos", df["Principal Executivo / Cargo"].nunique())

    