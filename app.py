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

# Nome do ficheiro CSV no repositório
NOME_ARQUIVO = "dados.csv"

# Função para carregar o CSV tentando diferentes codificações e delimitadores
@st.cache_data
def carregar_csv(caminho):
    encodings = ["utf-8", "latin1", "iso-8859-1", "cp1252"]
    separadores = [",", ";", "\t"]
    
    for enc in encodings:
        for sep in separadores:
            try:
                df = pd.read_csv(caminho, encoding=enc, sep=sep)
                # Se leu mais de 1 coluna, encontrou o separador correto
                if df.shape[1] > 1:
                    return df
            except Exception:
                continue
                
    # Tentativa final padrão caso as anteriores falhem
    return pd.read_csv(caminho, encoding="latin1")

if os.path.exists(NOME_ARQUIVO):
    try:
        df = carregar_csv(NOME_ARQUIVO)

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

        # Limpeza de duplicados
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
            O gráfico de barras apresenta a distribuição dos registros absolutos por Unidade da Federação, evidenciando a diferença no volume de ocorrências pelo país. É possível comparar visualmente como estados mais populosos acumulam a maior parte dos casos brutos.
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
            O gráfico em linha permite observar a variação e o comportamento dos dados ao longo do território nacional. A conexão entre os pontos facilita a identificação de picos nos grandes centros e quedas nos estados de menor porte.
            """)

        st.divider()

        # Conclusões
        st.subheader("Conclusões da Análise")
        st.markdown("""
        **O que esse dashboard representa?**  
        Este dashboard representa uma ferramenta interativa de análise sobre a segurança pública no Brasil, desenvolvida para transformar dados brutos e complexos em informações visuais acessíveis.
        """)

    except Exception as e:
        st.error(f"Erro ao carregar o ficheiro 'dados.csv': {e}")

else:
    st.error(f"O ficheiro '{NOME_ARQUIVO}' não foi encontrado na raiz do repositório no GitHub.")
