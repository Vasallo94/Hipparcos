import plotly.io as pio
import requests
from io import BytesIO
import warnings
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly_express as px
import plotly.figure_factory as ff
import streamlit as st
from streamlit_lottie import st_lottie
from sys import path
import os
path.append(os.path.abspath(os.path.join('..')))
pio.templates.default = "plotly_dark"


# Configuración de la página
st.set_page_config(page_title="Hipparcos",
                   layout="wide", page_icon="✨", initial_sidebar_state="expanded")
st.set_option("deprecation.showPyplotGlobalUse", False)
warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    # Cambiar la fuente de texto
    st.write(
        """ <style>h1, h2, h3, h4, h5, h6 { font-family: 'roman'; } </style>""", unsafe_allow_html=True)

    st.markdown("# Machine Learning aplicado al catálogo estelar Hipparcos")

  # Tabs
    tabs = st.tabs(["Modelos y curvas de aprendizaje",
                   "Clasificación estelar mediante ML"])

    # Tab 1
    with tabs[0]:
        st.markdown('### Modelos y curvas de aprendizaje')

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('### Modelo Regresión Logística')
            st.image('img/ML_images/LogisticRegression.png')

            st.markdown('### Modelo KNN')
            st.image('img/ML_images/KNN.png')

        with col2:
            st.markdown('### Modelo Random Forest')
            st.image('img/ML_images/RandomForest.png')

            st.markdown('### Modelo Gradient Boosting')
            st.image('img/ML_images/GradientBoost.png')

        st.markdown('### Modelo XGBoosting')
        st.image('img/ML_images/XGBoost.png', width=700, use_column_width=True)

    with tabs[1]:
        st.markdown('### Clasificación estelar mediante ML')


if __name__ == '__main__':
    main()
