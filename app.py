import warnings
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly_express as px
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Hipparcos",
                   layout="wide", page_icon="✨", initial_sidebar_state="expanded")
st.set_option("deprecation.showPyplotGlobalUse", False)
warnings.simplefilter(action='ignore', category=FutureWarning)

# Lectura de datos
df = pd.read_pickle('data/hipparcos.pkl')
df_55 = pd.read_pickle('data/variables.pkl')


# Header
col1, col2, col3 = st.columns(3)

with col1:
    st.write("")

with col2:
    st.title(
        "Análisis del catálogo Hipparcos: Una aproximación a la astrofísica estelar")

with col3:
    st.write("")

st.markdown("""---""")
st.markdown("<center><h2><l style='color:white; font-size: 30px;'>Visualización y estudio de los datos</h2></l></center>", unsafe_allow_html=True)

# Tabs
tabs = st.tabs(["Tab 1", "Tab 2", "Tab 3", "Tab 4", "Tab 5"])

# Tab 1
with tabs[0]:
    st.title('Visualización 1')

    cols = st.columns(2)

    with cols[0]:
        st.write("Aquí va una visualización")

    with cols[1]:
        st.write("Aquí va otra visualización")

# Tab 2
with tabs[1]:
    st.title('Visualización 2')

    cols = st.columns(2)

    with cols[0]:
        st.write("Aquí va una visualización")

    with cols[1]:
        st.write("Aquí va otra visualización")

# Tab 3
with tabs[2]:
    st.title('Visualización 3')

    cols = st.columns(2)

    with cols[0]:
        st.write("Aquí va una visualización")

    with cols[1]:
        st.write("Aquí va otra visualización")

# Tab 4
with tabs[3]:
    st.title('Visualización 4')

    cols = st.columns(2)

    with cols[0]:
        st.write("Aquí va una visualización")

    with cols[1]:
        st.write("Aquí va otra visualización")

# Tab 5
with tabs[4]:
    st.title('Visualización 5')

    cols = st.columns(2)

    with cols[0]:
        st.write("Aquí va una visualización")

    with cols[1]:
        st.write("Aquí va otra visualización")
