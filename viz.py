import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import sweetviz as sv
from io import StringIO

def app(title=None):
    st.set_page_config(layout="wide")
    st.title(title)

    # Add a file uploader for CSV files
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    # Add a select box for choosing the separator
    sep = st.selectbox("Select the separator", ("Comma", "Tab", ";", ":"))
    sep = "," if sep == "Comma" else "\t" if sep == "Tab" else ";" if sep == ";" else ":"

    if uploaded_file is not None:
        # Read the CSV data from the uploaded file
        df = pd.read_csv(StringIO(uploaded_file.getvalue().decode('utf-8')), sep=sep)
        st.write(df)

        # Use the analysis function from sweetviz module to create a 'DataframeReport' object.
        analysis = sv.analyze(df)

        # Save the analysis as an HTML file.
        html_file = "output.html"
        # analysis.show_html(html_file)
        # Get the current directory
        current_dir = os.getcwd()
        # Create the full path to the HTML file
        full_path = os.path.join(current_dir, html_file)

        # Render the output on a web page.
        analysis.show_html(filepath=full_path, open_browser=False, layout='vertical', scale=1.0)
        HtmlFile = open("output.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code, height=1200, width=1600, scrolling=True)

app(title='Sweet Visualization')


