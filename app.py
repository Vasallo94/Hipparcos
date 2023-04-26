
import warnings
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly_express as px
from utils.funciones import *
import streamlit as st


sns.set()
warnings.simplefilter(action='ignore', category=FutureWarning)

# mapas interactivos
# to make the plotly graphs
cufflinks.go_offline(connected=True)
init_notebook_mode(connected=True)
# text mining
# This i will use to print Lottie file ( Lottie is a JSON-based animation file format that can be used in webapp applications)


# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()


def main():

    # --------------------------------------------------------CONFIGURACIÓN DE LA PÁGINA---------------------------------------------------#
    # layout="centered" or "wide"
    st.set_page_config(page_title="Hipparcos",
                       layout="wide", page_icon="✨", initial_sidebar_state="expanded")
    st.set_option("deprecation.showPyplotGlobalUse", False)

# -----------------------------------------------------------------HEADER----------------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    # first column, this is the lottie file
    with col1:
        # lottie_url_hello = "https://assets5.lottiefiles.com/packages/lf20_7D0uqz.json"
        # lottie_hello = load_lottieurl(lottie_url_hello)
        # st_lottie(lottie_hello, key="hello", height=150, width=150, loop=True)
        # second column, this is the title
    with col2:
        st.title(
            "Análisis del catálogo Hipparcos: Una aproximación a la astrofísica estelar")
    with col3:
        # image = Image.open('')

        # st.image(image, caption='',
        #          use_column_width='auto')

        # -----------------------------------------------LECTURA DE DATOS Y PREPROCESAMIENTO------------------------------------#

    df = pd.read_pickle('data/hipparcos.pkl')
    df_55 = pd.read_pickle('data/variables.pkl')
    st.subheader(
        "")
# -----------------------------------------------------------SLIDER--------------------------------------------#
    # Filtrar el dataframe según la distancia seleccionada
    # Crear el slider para seleccionar la distancia máxima
    # distancia = st.slider(
    #     "Seleccione la distancia máxima a la que mostrar resultados (km):", 1, 60, 25)

    # # Crear un nuevo dataframe filtrando los valores de la columna de distancias
    # df_slider = df_55[df_55['distancia'] < distancia]


# -----------------------------------------------------------MAIN PAGE----------------------------------------#
    # Show the selected dataframe on the main page
    st.write(df_slider)
    st.markdown("""---""")
    st.markdown(
        "<center><h2><l style='color:white; font-size: 30px;'>Visualización y estudio de los datos</h2></l></center>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------TABS---------------------------------------------------#
    st.title("")
    tabs = st.tabs(["", ''])

    # -------------------------------------------------------TAB 1-----------------------------------------------------#
    tab_plots = tabs[0]  # this is the first tab
    with tab_plots:

        st.title('')

        cols = st.columns(2)
        with cols[0]:
            st.write("")

        with cols[1]:
            st.write("")

        cols = st.columns(2)
        with cols[0]:

            st.write('...')

        with cols[1]:
            st.write("...")

            # -------------------------------------------------------TAB 2-----------------------------------------------------#

    tab_plots = tabs[1]  # this is the second tab
    with tab_plots:
        st.title('...')

        cols = st.columns(2)
        with cols[0]:
            st.write("")

        with cols[1]:
            st.write("")

        cols = st.columns(2)
        with cols[0]:
            st.write("")
        with cols[1]:
            st.write("")

        # -------------------------------------------------------TAB 4-----------------------------------------------------#
    tab_plots = tabs[2]  # this is the third tab
    with tab_plots:
        st.title('...')
        cols = st.columns(2)
        with cols[0]:
            st.write("")
        with cols[1]:
            st.write("")

        st.markdown('---')
        st.write('...')

        # -------------------------------------------------------TAB 6-----------------------------------------------------#
    tab_plots = tabs[3]  # this is the third tab
    with tab_plots:

        st.title('...')

        # -------------------------------------------------------TAB 5-----------------------------------------------------#
    tab_plots = tabs[4]  # this is the third tab
    with tab_plots:
        st.title('...')


if __name__ == '__main__':
    main()
