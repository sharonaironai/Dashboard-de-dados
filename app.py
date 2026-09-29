import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="Dashboard de Dados",
    layout="wide"
)

st.title("Dashboard de Dados")
arquivo = "s2t6101.xls"
if arquivo is not None:
    arquivo.endswith(('.xls', '.xlsx')):
    df_raw = pd.read_excel(arquivo, skiprows=7, header=None)
    df = df_raw.iloc[:28, :6].copy()
    df.columns = ["UF", "Absoluto_2021", "Absoluto_2022", "Taxa_2021", "Taxa_2022", "Variacao_Pct"]
    df["UF"] = df["UF"].astype(str).str.replace(r"\s*\(\d+\)", "", regex=True).str.strip()
    for col in ["Absoluto_2021", "Absoluto_2022", "Taxa_2021", "Taxa_2022", "Variacao_Pct"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    else:
        df = pd.read_csv(arquivo)
    col1, col2 = st.columns(2)
    col1.metric("Quantidade de registros", df.shape[0])
    col2.metric("Quantidade de colunas", df.shape[1])
    
    st.subheader("Visualização dos dados")
    st.dataframe(df.head())
    
    # --- ATUALIZADO: Formatação profissional das Informações da Base ---
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

    # --- ATUALIZADO: Remoção da linha 'Brasil' para não distorcer média e gráficos ---
    df = df[df["UF"] != "Brasil"]

    st.subheader("Gráficos e Indicadores")
    coluna_numerica = df.select_dtypes(include=['number']).columns[0]
    media = df[coluna_numerica].mean()
    st.metric("Valor Médio", round(media, 2))

    colunas = df.columns

    fig1 = px.bar(
        df,
        x=colunas[0],
        y=coluna_numerica,
        title="Gráfico 1: Análise Por Categoria"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    **Análise do Gráfico 1:** 
    O gráfico de barras apresenta a distribuição dos registros por localização. É possível comparar visualmente quais Unidades da Federação acumulam os maiores e menores valores absolutos.
    """)

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
 
    st.markdown("""
        **O que esse dashboard representa?**
        Este dashboard representa uma ferramenta interativa de análise sobre a segurança pública no Brasil, desenvolvida para transformar dados brutos e complexos do IBGE em informações visuais acessíveis. Ele centraliza métricas e gráficos que permitem monitorar o volume, a incidência proporcional e a evolução dos registros de violência entre as Unidades da Federação de forma simples e intuitiva.
        """)
 
    st.markdown("""
    **O que podemos observar?**
    Ao analisar o painel, observamos uma clara divisão entre volume absoluto e taxa proporcional: enquanto estados do Sudeste como São Paulo e Rio de Janeiro lideram no número total de casos por terem populações maiores, estados do Norte como Roraima e Rondônia apresentam as maiores taxas por 100 mil habitantes. Além disso, nota-se uma tendência geral de crescimento nacional de 2,9% entre 2021 e 2022, impulsionada por altas expressivas em estados específicos, como o Amazonas, que teve um salto de 92% no período
    """)

    st.markdown(""" **Ada Mirella e Matheus Gabriel** """)

    st.markdown(""" INTRODUÇÃO
Este trabalho analisa os dados do IBGE sobre violência doméstica e estupro no Brasil (2021-2022). O objetivo é examinar a variação dos casos e as taxas por 100 mil habitantes em cada estado, identificando tendências e disparidades regionais.""")
