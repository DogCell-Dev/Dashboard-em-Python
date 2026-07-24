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
planilha = "dados.xlsx"

df = pd.read_excel( # df = DataFrame 
    planilha,
    sheet_name="Pipeline Prospecção 100 Leads",
    header=3
)

# ------------------------ BLOCO DE SCORE DE PRIORIDADE ---------------------------
# Palavras que podem indicam oportunidade de melhores LEADs
# Palavras-chave que podem indicam possíveis necessidades de segurança
palavras_risco = [
    "lgpd",
    "vazamento",
    "ataque",
    "hacker",
    "cibernético",
    "cibernetico",
    "segurança",
    "risco",
    "vulnerabilidade",
    "firewall",
    "criptografia",
    "backup",
    "servidor",
    "rede",
    "dados",
    "ti"
]

def calculo_score(row):
    obs_empresa = str(row["Observações"]).lower().strip()

    score = 0

    for palavra in palavras_risco:
        if palavra in obs_empresa:
            score += 1
    return score

df["Score Risco"] = df.apply(
    calculo_score,
    axis=1
)

# --------------------------- FILTROS -----------------------------
# Criei uma sidebar com um filtro de LEADs de 1 segmento especifico
st.sidebar.header("🔎 Filtros")
df_filtrado = df

lista_segmentos = sorted(df["Segmento"].dropna().unique())

segmento_selecionado = st.sidebar.selectbox(
    "Escolha um segmento",
    ["Todos"] + list(lista_segmentos)
)

if segmento_selecionado == "Todos":
    lista_cidades = sorted(df["Cidade/UF"].dropna().unique())
else:
    lista_cidades = sorted(
        df[df["Segmento"] == segmento_selecionado]["Cidade/UF"].dropna().unique()
    )

cidade_selecionada = st.sidebar.selectbox(
    "Escolha uma cidade",
    ["Todas"] + list(lista_cidades)
)

if segmento_selecionado != "Todos":
    df_filtrado = df[
        df["Segmento"] == segmento_selecionado
    ]

if cidade_selecionada != "Todas":
    df_filtrado = df_filtrado[
        df_filtrado["Cidade/UF"] == cidade_selecionada
    ]

if df_filtrado.empty:
    st.warning("Nenhum lead encontrado para os filtros selecionados.")
    st.stop()


# ------------------------------------------- KPIs --------------------------------------------
# Armazenei os valores dos KPIs em variaveis pois facilita a manutenção e deixa mais organizado
total_leads = len(df_filtrado)
total_segmentos = df_filtrado["Segmento"].nunique()
total_cidades = df_filtrado["Cidade/UF"].nunique()
total_executivos = df_filtrado["Principal Executivo / Cargo"].nunique()
media_kpi = (df_filtrado["KPI Sucesso"].str.replace("%","").astype(float).mean()
)

# Criação dos 'cartões' KPIs (Indicador Chave de Desempenho) 
st.markdown("## 📈 Indicadores")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total de Leads", total_leads)

with col2:
    st.metric("Segmentos", total_segmentos)

with col3:
    st.metric("Cidades", total_cidades)

with col4:
    st.metric("Executivos", total_executivos)

with col5:
    st.metric("KPI Médio de Sucesso",f"{media_kpi:.1f}%")

st.divider()

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
    contagem_cidades,
    x = contagem_cidades.values, # x = Horizontal do grafico
    y = contagem_cidades.index, # y = Vertical do grafico 
    orientation="h", #
    labels={ # subtítulos de cada eixo
        "x": "Quantidade de LEADs",
        "y": "Cidades"
    },
    title= "Top 10 Cidades com mais LEADs"
)

# Grafico scatter de oportunidades 
df_filtrado["KPI Numerico"] = (
    df_filtrado["KPI Sucesso"]
    .str.replace("%", "")
    .astype(float)
)

grafico_oportunidade = px.scatter(
    df_filtrado,
    x="KPI Numerico",
    y="Score Risco",
    color="Segmento",
    hover_name="Nome da Empresa",
    labels={
        "KPI Numerico": "KPI de Sucesso (%)",
        "Oportunidade de abordagem": "Score de Prioridade"
    },
    title="Mapa de oportunidade de venda"
)

# ---------------------------- ESTILIZAÇÃO DOS GRAFICOS ---------------------------
grafico_segmentos.update_layout(
    title_x=0.4,
    template="plotly_white"
)
grafico_segmentos.update_traces(
    text=contagem_segmentos.values,
    textposition="outside"
)

grafico_cidades.update_layout(
    title_x=0.4,
    template="plotly_white"
)

grafico_cidades.update_traces(
    text=contagem_cidades.values,
    textposition="outside"
)

grafico_oportunidade.update_layout(
    title_x=0.4,
    template="plotly_white"
)

# --------------------------- GRAFICOS LADO A LADO ------------------------------
col_grafico1, col_grafico2 = st.columns(2) 
with col_grafico1:
    st.plotly_chart(grafico_segmentos, use_container_width=True)

with col_grafico2:
    st.plotly_chart(grafico_cidades, use_container_width=True)

st.plotly_chart(grafico_oportunidade, use_container_width=True)

st.divider()

# ------------------ TABELA --------------------
# Todos dados da planilha excel usada no projeto
st.write(f"Total de registros encontrados: {len(df_filtrado)}")
st.subheader("Prévia dos dados") # Verifica se os dados da planilha foram carregados corretamente 
st.dataframe(df_filtrado, use_container_width=True) # df.head() exibe somente uma amostra de Dados 

# ---------------------------------- FOOTER ----------------------------------
st.divider()

st.caption(
    "Projeto desenvolvido para o Processo Seletivo Pegasus Desenvolve."
)