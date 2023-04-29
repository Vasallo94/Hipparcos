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
from PIL import Image
import os
path.append(os.path.abspath(os.path.join('../')))
pio.templates.default = "plotly_dark"


# Configuración de la página
st.set_page_config(page_title="Hipparcos",
                   layout="wide", page_icon="✨", initial_sidebar_state="expanded")
st.set_option("deprecation.showPyplotGlobalUse", False)
warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("# Hipparcos")
        st.markdown("La misión [Hipparcos](https://www.cosmos.esa.int/web/hipparcos) fue una misión espacial de la Agencia Espacial Europea (ESA) lanzada en 1989 con el objetivo de medir con precisión las posiciones, distancias y movimientos de más de un millón de estrellas en nuestra galaxia, la Vía Láctea.")
        st.markdown("Durante su misión, el satélite Hipparcos utilizó un telescopio especializado para medir la posición de las estrellas con una precisión nunca antes alcanzad (ahora ampliamente superada por la misión Gaia). Además, utilizó técnicas de paralaje para medir la distancia de las estrellas a la Tierra, lo que permitió construir un mapa tridimensional de la galaxia.")
        st.markdown("El resultado de la misión fue la creación del Catálogo Hipparcos, que contiene información detallada sobre la posición, el movimiento y la distancia de más de 100,000 estrellas con una precisión sin precedentes. El catálogo también incluye información sobre la luminosidad y la temperatura de las estrellas, lo que permite a los astrónomos estudiar la evolución y la estructura de nuestra galaxia.")
        st.markdown("El Catálogo Hipparcos ha sido ampliamente utilizado por la comunidad científica en una variedad de campos, desde la astrofísica hasta la cosmología, y ha sido fundamental para nuestra comprensión del universo y nuestro lugar en él.")
        st.markdown("---")
        st.markdown("## Datos")
        df = pd.read_parquet('data/hipparcos_final.parquet')
        st.dataframe(df)
    with col2:
        # Mostrar la imagen
        img_url = "https://upload.wikimedia.org/wikipedia/commons/7/78/Hipparcos-testing-estec.jpg"
        link_url = "https://upload.wikimedia.org/wikipedia/commons/7/78/Hipparcos-testing-estec.jpg"
        st.image(img_url, use_column_width=True)

        # Crear el enlace en formato markdown
        link_markdown = f'<a href="{link_url}">Ver imagen original</a>'

        # Mostrar el enlace
        st.markdown(link_markdown, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
