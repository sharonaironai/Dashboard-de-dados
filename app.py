import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Dados",
    layout="wide"
)

st.title("Dashboard de Dados - Segurança Pública no Brasil")
st.caption("Desenvolvido por: **Ada Mirella e Matheus Gabriel**")

st.markdown("""
**Introdução:**  
Este trabalho analisa os dados do IBGE sobre violência doméstica e estupro no Brasil (2021-2022). 
O objetivo é examinar a variação dos casos e as taxas por 100 mil habitantes em cada estado, identificando tendências e disparidades regionais.
""")

st.divider()

NOME_ARQUIVO = "dados.csv"

@st.cache_data
def carregar_dados(caminho):
    try:
        df_raw = pd.read_excel(caminho, skiprows=7, header=None)
        df = df_raw.iloc[:28, :6].copy()
        df.columns = ["UF", "Absoluto_2021", "Absoluto_2022", "Taxa_2021", "Taxa_2022", "Variacao_Pct"]
        df["UF"] = df["UF"].astype(str).str.replace(r"\s*\(\d+\)", "", regex=True).str.strip()
        for col in ["Absoluto_2021", "Absoluto_2022", "Taxa_2021", "Taxa_2022", "Variacao_Pct"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        return df
    except Exception:
        # Plano B caso o arquivo seja convertido para CSV real futuramente
        return pd.read_csv(caminho, encoding="latin1")

if os.path.exists(NOME_ARQUIVO):
    df = carregar_dados(NOME_ARQUIVO)

    col1, col2 = st.columns(2)
    col1.metric("Quantidade de registros", df.shape[0])
    col2.metric("Quantidade de colunas", df.shape[1])

    st.subheader("Visualização dos dados")
    st.dataframe(df.head(), use_container_width=True)

    st.subheader("Informações sobre a base")
    col_info1, col_info2, col_info3 = st.columns(3)

    with col_info1:
        st.markdown("**Tipos de dados por coluna:**")
        df_tipos = pd.DataFrame(df.dtypes.astype(str), columns=["Tipo"]).reset_index()
        df_tipos.columns = ["Coluna", "Tipo de Dado"]
        st.dataframe(df_tipos, hide_index=True, use_container_width=True)

    with col_info2:
        st.markdown("**Valores ausentes por coluna:**")
        df_nulos = pd.DataFrame(df.isnull().sum(), columns=["Nulos"]).reset_index()
        df_nulos.columns = ["Coluna", "Qtd. Nulos"]
        st.dataframe(df_nulos, hide_index=True, use_container_width=True)

    with col_info3:
        st.markdown("**Registros Duplicados:**")
        qtd_duplicados = df.duplicated().sum()
        st.metric("Total de Linhas Duplicadas", qtd_duplicados)
        st.caption("Linhas 100% idênticas encontradas na base.")

    df = df.drop_duplicates()
    df_estados = df[df["UF"] != "Brasil"].copy()

    st.divider()

    st.subheader("Gráficos e Indicadores")
    media_casos = df_estados["Absoluto_2022"].mean()
    st.metric("Média de Ocorrências em 2022 (por Estado)", f"{media_casos:,.2f}")

    fig1 = px.bar(
        df_estados,
        x="UF",
        y="Absoluto_2022",
        title="Gráfico 1: Registros Absolutos de Violência Doméstica por Estado (2022)",
        labels={"UF": "Estado (UF)", "Absoluto_2022": "Casos Absolutos em 2022"}
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    **Análise do Gráfico 1:**  
    O gráfico de barras apresenta a distribuição dos registros absolutos por Unidade da Federação em 2022. Observa-se que estados com maiores contingentes populacionais acumulam o maior volume bruto de registros.
    """)
    fig2 = px.line(
        df_estados,
        x="UF",
        y="Taxa_2022",
        title="Gráfico 2: Taxa por 100 mil Habitantes por Estado (2022)",
        labels={"UF": "Estado (UF)", "Taxa_2022": "Taxa por 100 mil Hab."}
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    **Análise do Gráfico 2:**  
    O gráfico em linha demonstra a incidência proporcional dos casos por 100 mil habitantes. A análise em taxa revela a gravidade relativa do problema em estados de menor população total.
    """)

    st.divider()

    st.subheader("Conclusões da Análise")
    st.markdown("""
    **O que esse dashboard representa?**  
    Este dashboard representa uma ferramenta interativa de análise sobre a segurança pública no Brasil, desenvolvida para transformar dados brutos do IBGE em informações visuais acessíveis.
    """)

else:
    st.error(f"O arquivo '{NOME_ARQUIVO}' não foi encontrado no repositório.")
