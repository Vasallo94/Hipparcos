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
    st.markdown("# Machine Learning aplicado al catálogo estelar Hipparcos")


if __name__ == '__main__':
    main()
