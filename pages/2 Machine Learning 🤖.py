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


@st.cache_resource()
def load_model(model_name):
    model = joblib.load(f'{model_name}')
    return model


# Carga los cinco modelos
model_LR = load_model('output/Tipo_GradientBoost.pkl')
model_RF = load_model('output/Tipo_RandomForest.pkl')
model_KNN = load_model('output/Tipo_KNN.pkl')
model_GB = load_model('output/Tipo_GradientBoost.pkl')
model_XGB = load_model('output/Tipo_XGBoost.pkl')


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
            st.image('img/ML_images/Logistic_Regression.png')

            st.markdown('### Modelo KNN')
            st.image('img/ML_images/KNN.png')

        with col2:
            st.markdown('### Modelo Random Forest')
            st.image('img/ML_images/RandomForest.png')

            st.markdown('### Modelo Gradient Boosting')
            st.image('img/ML_images/GradientBoosting.png')

        st.markdown('### Modelo XGBoosting')
        st.image('img/ML_images/XGBoost.png', width=700, use_column_width=True)

    with tabs[1]:
        st.markdown('### Clasificación estelar mediante ML')

        # Crear menú de Streamlit
        st.title('Modifica los valores de tu estrella para clasificarla')
        st.markdown(
            'Utiliza el slider para modificar los valores del DataFrame:')

        # Inicializamos un dataframe con valores por defecto
        X_new = pd.DataFrame([[8.312439, 9.11, 8.32, 0.69, 0.749, 5.0, 8.41, 0.740, 248, 0.0, 0.0]],
                             columns=['Vmag', 'BTmag', 'VTmag', 'B-V', 'V-I', 'Hpmag', '(V-I)red', 'd', 'T', 'M_v', 'M_Hip'])

        # Crear sliders para cada columna del DataFrame
        Vmag = st.slider('Vmag', min_value=-1.5,
                         max_value=14.0, value=float(X_new['Vmag'][0]))
        BTmag = st.slider('BTmag', min_value=-0.5,
                          max_value=15.0, value=float(X_new['BTmag'][0]))
        VTmag = st.slider('VTmag', min_value=-0.6,
                          max_value=12.0, value=float(X_new['VTmag'][0]))
        B_V = st.slider('B-V', min_value=-0.4,
                        max_value=5.46, value=float(X_new['B-V'][0]))
        V_I = st.slider('V-I', min_value=-0.49,
                        max_value=9.03, value=float(X_new['V-I'][0]))
        Hpmag = st.slider('Hpmag', min_value=-1.1,
                          max_value=14.6, value=float(X_new['Hpmag'][0]))
        V_I_red = st.slider('(V-I)red', min_value=-0.52,
                            max_value=9.29, value=float(X_new['(V-I)red'][0]))
        d = st.slider('d [parsec]', min_value=1.2, max_value=990.0,
                      value=float(X_new['d'][0]))

        # Calcular valores predeterminados para T, M_v y M_Hip
        T_default = 8540 / (B_V + 0.865)
        M_v_default = (Vmag - 5 *
                       np.log10(d)+5).astype(np.float32)
        M_Hip_default = (Hpmag - 5 *
                         np.log10(d)+5).astype(np.float32)

        # Establecer valores predeterminados para T, M_v y M_Hip y deshabilitar los sliders correspondientes
        T = st.slider('T [K]', min_value=1300.0, max_value=1900.0,
                      value=float(T_default), key="T")
        M_v = st.slider('M_v', min_value=-9.0,
                        max_value=16.0, value=float(M_v_default), key="M_v")
        M_Hip = st.slider('M_Hip', min_value=-10.0,
                          max_value=10.0, value=float(M_Hip_default), key="M_Hip")

        # Actualizar DataFrame con los nuevos valores
        X_new = pd.DataFrame([[Vmag, BTmag, VTmag, B_V, V_I, Hpmag, V_I_red, d, T, M_v, M_Hip]],
                             columns=['Vmag', 'BTmag', 'VTmag', 'B-V', 'V-I', 'Hpmag', '(V-I)red', 'd', 'T', 'M_v', 'M_Hip'])

        # Mostrar DataFrame actualizado
        st.write('DataFrame actualizado:')
        st.write(X_new)

        # Widget para seleccionar el modelo
        model_selector = st.selectbox('Selecciona un modelo', (
            'Logistic Regression', 'Random Forest', 'KNN', 'Gradient Boost', 'XGBoost'))
        st.write('Modelo seleccionado:', model_selector)

        # Seleccionar el modelo adecuado
        if model_selector == 'Logistic Regression':
            model = model_LR
        elif model_selector == 'Random Forest':
            model = model_RF
        elif model_selector == 'KNN':
            model = model_KNN
        elif model_selector == 'Gradient Boost':
            model = model_GB
        else:
            model = model_XGB

        # Botón para hacer la predicción
        if st.button('RUN'):
            # Hacer predicciones en los nuevos datos utilizando el modelo seleccionado
            y_pred = model.predict(X_new)
            # Obtener la letra correspondiente
            letters = ['A', 'B', 'F', 'G', 'K', 'M', 'O']
            letter = letters[y_pred[0]]
            # Mostrar la predicción
            st.write('La estrella es de tipo:', letter)


if __name__ == '__main__':
    main()
