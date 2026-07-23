# ------------- IMPORTANDO BIBLIOTECAS ---------------- 
import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------ TÍTULO -----------------------------
# Definindo configurações de layout, titulo e fivicon da página
st.set_page_config(
    page_title="Dashboard Pegasus",
    page_icon="📊",
    layout="wide"
)

# Titulo principal e subtítulo do Dashboard 
st.title("Dashboard de Prospecção - Pegasus")
st.caption("Dashboard desenvolvido em Python utilizando Streamlit, Pandas e Plotly.")
st.markdown("**Análise dos Leads do Processo Seletivo**")


# ------------------ LEITURA ------------------
# Etapa que os Dados da planilha são carregados
planilha = "Dados.xlsx"

df = pd.read_excel( # df = DataFrame 
    planilha,
    sheet_name="Pipeline Prospecção 100 Leads",
    header=3
)

# --------------------------- FILTROS -----------------------------
# Criei uma sidebar com um filtro de LEADs de 1 segmento especifico
st.sidebar.header("🔎 Filtros")

lista_segmentos = sorted(df["Segmento"].dropna().unique())

segmento_selecionado = st.sidebar.selectbox(
    "Escolha um segmento",
    ["Todos"] + list(lista_segmentos)
)

if segmento_selecionado == "Todos":
    df_filtrado = df
else:
    df_filtrado = df[df["Segmento"] == segmento_selecionado]

# ------------------------------------------- KPIs --------------------------------------------
# Armazenei os valores dos KPIs em variaveis pois facilita a manutenção e deixa mais organizado
total_leads = len(df_filtrado)
total_segmentos = df_filtrado["Segmento"].nunique()
total_cidades = df_filtrado["Cidade/UF"].nunique()
total_executivos = df_filtrado["Principal Executivo / Cargo"].nunique()

# Criação dos 'cartões' KPIs (Indicador Chave de Desempenho) 
st.markdown("## 📈 Indicadores")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Leads", total_leads)

with col2:
    st.metric("Segmentos", total_segmentos)

with col3:
    st.metric("Cidades", total_cidades)

with col4:
    st.metric("Executivos", total_executivos)

# ------------------ GRAFICOS ----------------------
#           Todos graficos do Dashboard
st.markdown("## 📊 Análises")

#Grafico de Segmentos
contagem_segmentos = df_filtrado["Segmento"].value_counts()

grafico_segmentos = px.bar(
    contagem_segmentos,
    x=contagem_segmentos.values, # x = Horizontal do grafico
    y=contagem_segmentos.index, # y = Vertical do grafico
    labels={ # subtítulos de cada eixo
        "x": "Quantidade de Leads",
        "y": "Segmento"
    },
    title="Leads por Segmento" # Titulo principal do grafico
)

# Grafico de Cidades
contagem_cidades = df_filtrado["Cidade/UF"].value_counts().head(10)

grafico_cidades = px.bar(
    x = contagem_cidades.values, # x = Horizontal do grafico
    y = contagem_cidades.index, # y = Vertical do grafico 
    orientation="h", #
    labels={ # subtítulos de cada eixo
        "x": "Quantidade de LEADs",
        "y": "Cidades"
    },
    title= "Top 10 Cidades com mais LEADs"
)

# ---------------------------- ESTILIZAÇÃO DOS GRAFICOS ---------------------------
grafico_segmentos.update_layout(
    title_x=0.5
)
grafico_segmentos.update_traces(
    text=contagem_segmentos.values,
    textposition="outside"
)

grafico_cidades.update_layout(
    title_x=0.5
)

grafico_cidades.update_traces(
    text=contagem_cidades.values,
    textposition="outside"
)

# --------------------------- GRAFICOS LADO A LADO ------------------------------
col_grafico1, col_grafico2 = st.columns(2) 
with col_grafico1:
    st.plotly_chart(grafico_segmentos, use_container_width=True)

with col_grafico2:
    st.plotly_chart(grafico_cidades, use_container_width=True)

# ------------------ TABELA --------------------
# Todos dados da planilha excel usada no projeto
st.subheader("Prévia dos dados") # Verifica se os dados da planilha foram carregados corretamente 
st.dataframe(df_filtrado.head()) # df.head() exibe somente uma amostra de Dados 

# ---------------------------------- FOOTER ----------------------------------
st.markdown("---")

st.caption(
    "Projeto desenvolvido para o Processo Seletivo Pegasus Desenvolve."
)