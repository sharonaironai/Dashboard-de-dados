import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Dados",
    layout="wide"
)

# Título, Autores e Introdução no topo
st.title("Dashboard de Dados - Segurança Pública no Brasil")
st.caption("Desenvolvido por: **Ada Mirella e Matheus Gabriel**")

st.markdown("""
**Introdução:**  
Este trabalho analisa os dados do IBGE sobre violência doméstica e estupro no Brasil (2021-2022). 
O objetivo é examinar a variação dos casos e as taxas por 100 mil habitantes em cada estado, identificando tendências e disparidades regionais.
""")

st.divider()

# Define o nome do arquivo padrão
NOME_ARQUIVO = "dados.csv"

# Função para carregar o arquivo com tratamento de codificação
@st.cache_data
def carregar_dados(caminho):
    # Se for Excel
    if caminho.endswith(('.xls', '.xlsx')):
        df_raw = pd.read_excel(caminho, skiprows=7, header=None)
        df = df_raw.iloc[:28, :6].copy()
        df.columns = ["UF", "Absoluto_2021", "Absoluto_2022", "Taxa_2021", "Taxa_2022", "Variacao_Pct"]
        df["UF"] = df["UF"].astype(str).str.replace(r"\s*\(\d+\)", "", regex=True).str.strip()
        for col in ["Absoluto_2021", "Absoluto_2022", "Taxa_2021", "Taxa_2022", "Variacao_Pct"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        return df
    
    # Se for CSV, tenta ler com latin1 primeiro para evitar UnicodeDecodeError
    try:
        return pd.read_csv(caminho, encoding="latin1")
    except Exception:
        return pd.read_csv(caminho, encoding="utf-8")

if os.path.exists(NOME_ARQUIVO):
    df = carregar_dados(NOME_ARQUIVO)

    # Indicadores principais de dimensão
    col1, col2 = st.columns(2)
    col1.metric("Quantidade de registros", df.shape[0])
    col2.metric("Quantidade de colunas", df.shape[1])

    st.subheader("Visualização dos dados")
    st.dataframe(df.head(), use_container_width=True)

    # Informações sobre a base
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

    # Tratamento de dados
    df = df.drop_duplicates()
    if "UF" in df.columns:
        df = df[df["UF"] != "Brasil"]

    st.divider()

    # Gráficos e Indicadores
    st.subheader("Gráficos e Indicadores")
    colunas_numericas = df.select_dtypes(include=['number']).columns
    
    if len(colunas_numericas) > 0:
        coluna_numerica = colunas_numericas[0]
        media = df[coluna_numerica].mean()
        st.metric("Valor Médio de Ocorrências", round(media, 2))

        colunas = df.columns

        # Gráfico 1: Barras
        fig1 = px.bar(
            df,
            x=colunas[0],
            y=coluna_numerica,
            title="Gráfico 1: Análise Por Categoria"
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("""
        **Análise do Gráfico 1:**  
        O gráfico de barras apresenta a distribuição dos registros absolutos por Unidade da Federação, evidenciando a diferença no volume de ocorrências pelo país. É possível comparar visualmente como estados mais populosos — como São Paulo, Rio de Janeiro e Minas Gerais — acumulam a maior parte dos casos brutos. Essa visualização ajuda a identificar as regiões que concentram a maior demanda por investimentos e recursos em segurança pública.
        """)

        # Gráfico 2: Linhas
        fig2 = px.line(
            df,
            x=colunas[0],
            y=coluna_numerica,
            title="Gráfico 2: Acompanhamento da Coluna"
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("""
        **Análise do Gráfico 2:**  
        O gráfico em linha permite observar a variação e o comportamento dos dados ao longo do território nacional. A conexão entre os pontos facilita a identificação de picos nos grandes centros e quedas nos estados de menor porte. Essa análise mostra que a distribuição dos casos não é homogênea, ajudando a diagnosticar diferenças regionais e a planejar ações preventivas direcionadas para cada localidade.
        """)

    st.divider()

    # Seção explicativa final
    st.subheader("Conclusões da Análise")

    st.markdown("""
    **O que esse dashboard representa?**  
    Este dashboard representa uma ferramenta interativa de análise sobre a segurança pública no Brasil, desenvolvida para transformar dados brutos e complexos do IBGE em informações visuais acessíveis. Ele centraliza métricas e gráficos que permitem monitorar o volume, a incidência proporcional e a evolução dos registros de violência entre as Unidades da Federação de forma simples e intuitiva.
    """)

    st.markdown("""
    **O que podemos observar?**  
    Ao analisar o painel, observamos uma clara divisão entre volume absoluto e taxa proporcional: enquanto estados do Sudeste como São Paulo e Rio de Janeiro lideram no número total de casos por terem populações maiores, estados do Norte como Roraima e Rondônia apresentam as maiores taxas por 100 mil habitantes. Além disso, nota-se uma tendência geral de crescimento nacional de 2,9% entre 2021 e 2022, impulsionada por altas expressivas em estados específicos, como o Amazonas, que teve um salto de 92% no período.
    """)

else:
    st.error(f"O arquivo '{NOME_ARQUIVO}' não foi encontrado no repositório do GitHub. Certifique-se de enviá-lo para a mesma pasta do app.py.")
