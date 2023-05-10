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
import joblib
import os
path.append(os.path.abspath(os.path.join('..')))
pio.templates.default = "plotly_dark"


# Configuración de la página
st.set_page_config(page_title="Hipparcos",
                   layout="wide", page_icon="✨", initial_sidebar_state="auto")
st.set_option("deprecation.showPyplotGlobalUse", False)
warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    # Cambiar la fuente de texto
    st.write(
        """ <style>h1, h2, h3, h4, h5, h6 { font-family: 'roman'; } </style>""", unsafe_allow_html=True)

    st.markdown("# Bibliografía y enlaces")
    st.markdown(
        "Los datos son de Kaggle y se pueden consultar [aquí](https://www.kaggle.com/datasets/konivat/hipparcos-star-catalog)")
    st.markdown(
        'El archivo lottie se puede ver [aquí](https://lottiefiles.com/89151-stars)')
    st.markdown(
        'Apuntes de las asignaturas de __Astrofísica__ y __Astrofísica estelar__ de la Universidad Complutense de Madrid')
    st.markdown('Kippenhahn, R., Weigert, A., & Weiss, A. (1990). Stellar structure and evolution (Vol. 192). Berlin: Springer-verlag.')


if __name__ == '__main__':
    main()
