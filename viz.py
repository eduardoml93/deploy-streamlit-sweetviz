import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import sweetviz as sv
from io import StringIO
import requests

def app(title=None):
    st.set_page_config(layout="wide")
    st.title(title)

    # Escolha da fonte de dados
    option = st.radio("Selecione a fonte do CSV:", ("Upload de Arquivo", "Link da Web"))

    df = None
    sep = st.selectbox("Selecione o separador", ("Comma", "Tab", ";", ":"))
    sep = "," if sep == "Comma" else "\t" if sep == "Tab" else ";" if sep == ";" else ":"

    if option == "Upload de Arquivo":
        uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")
        if uploaded_file is not None:
            df = pd.read_csv(StringIO(uploaded_file.getvalue().decode('utf-8')), sep=sep)

    elif option == "Link da Web":
        url = st.text_input("Cole aqui o link do CSV (ex: https://.../arquivo.csv)")
        if url:
            try:
                response = requests.get(url)
                response.raise_for_status()  # Verifica se houve erro
                df = pd.read_csv(StringIO(response.text), sep=sep)
            except Exception as e:
                st.error(f"Erro ao carregar o CSV da URL: {e}")

    # Se o DataFrame foi carregado, mostra os dados e gera relatório
    if df is not None:
        st.write("### Visualização inicial do CSV")
        st.write(df.head())

        # Gera análise com Sweetviz
        analysis = sv.analyze(df)

        # Salva o relatório em HTML
        html_file = "output.html"
        analysis.show_html(filepath=html_file, open_browser=False, layout='vertical', scale=1.0)

        # Mostra dentro do Streamlit
        with open(html_file, 'r', encoding='utf-8') as HtmlFile:
            source_code = HtmlFile.read()
            components.html(source_code, height=1200, width=1750, scrolling=True)

app(title='SweetViz Visualization App')
