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
model_KNN = load_model('output/Tipo_KNN.pkl')
model_GB = load_model('output/Tipo_GradientBoost.pkl')
model_SVC = load_model('output/Tipo_SVC.pkl')
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
            'Utiliza el slider para modificar los valores de `Vmag`, `B-V` y `d` el resto se ajustarán automáticamente con base en estos tres parámetros:')

        # Inicializamos un dataframe con valores por defecto
        X_new = pd.DataFrame([[8.312439, 9.11, 8.32, 0.69, 0.749, 5.0, 8.41, 0.740, 248, 0.0, 0.0]],
                             columns=['Vmag', 'BTmag', 'VTmag', 'B-V', 'V-I', 'Hpmag', '(V-I)red', 'd', 'T', 'M_v', 'M_Hip'])

        # Crear sliders para cada columna del DataFrame
        Vmag = st.slider('Vmag', min_value=-1.5,
                         max_value=14.0, value=float(X_new['Vmag'][0]))
        B_V = st.slider('B-V', min_value=-0.4,
                        max_value=5.46, value=float(X_new['B-V'][0]))

        d = st.slider('d [parsec]', min_value=1.2, max_value=990.0,
                      value=float(X_new['d'][0]))

        # Calcular valores predeterminados para T, M_v y M_Hip
        BTmag_default = 0.88114 * Vmag + 1.78857
        VTmag_default = 0.8588 * Vmag + 1.18088
        V_I_default = 1.0595 * B_V + 0.01201
        V_I_red_default = 1.0024 * V_I_default + 0.01201

        T_default = 8540 / (B_V + 0.865)
        M_v_default = (Vmag - 5 *
                       np.log10(d)+5).astype(np.float32)
        Hpmag_default = 1.00564 * Vmag + 0.05840

        M_Hip_default = (Hpmag_default - 5 *
                         np.log10(d)+5).astype(np.float32)

        # # Establecer valores predeterminados para T, M_v y M_Hip y deshabilitar los sliders correspondientes
        # BTmag = st.slider('BTmag', min_value=-0.5,
        #                   max_value=15.0, value=float(BTmag_default))
        # VTmag = st.slider('VTmag', min_value=-0.6,
        #                   max_value=12.0, value=float(VTmag_default))
        # V_I = st.slider('V-I', min_value=-0.49,
        #                 max_value=9.03, value=float(V_I_default))
        # Hpmag = st.slider('Hpmag', min_value=-1.1,
        #                   max_value=14.6, value=float(Hpmag_default))
        # V_I_red = st.slider('(V-I)red', min_value=-0.52,
        #                     max_value=9.29, value=float(V_I_red_default))
        # T = st.slider('T [K]', min_value=1300.0, max_value=18366.0,
        #               value=float(T_default), key="T")
        # M_v = st.slider('M_v', min_value=-9.0,
        #                 max_value=16.0, value=float(M_v_default))
        # M_Hip = st.slider('M_Hip', min_value=-10.0,
        #                   max_value=10.0, value=float(M_Hip_default))

        BTmag = BTmag_default
        VTmag = VTmag_default
        V_I = V_I_default
        Hpmag = Hpmag_default
        V_I_red = V_I_red_default
        T = T_default
        M_v = M_v_default
        M_Hip = M_Hip_default

        # Actualizar DataFrame con los nuevos valores
        X_new = pd.DataFrame([[Vmag, BTmag, VTmag, B_V, V_I, Hpmag, V_I_red, d, T, M_v, M_Hip]],
                             columns=['Vmag', 'BTmag', 'VTmag', 'B-V', 'V-I', 'Hpmag', '(V-I)red', 'd', 'T', 'M_v', 'M_Hip'])

        # Actualizar DataFrame con los nuevos valores
        X_new = pd.DataFrame([[Vmag, BTmag, VTmag, B_V, V_I, Hpmag, V_I_red, d, T, M_v, M_Hip]],
                             columns=['Vmag', 'BTmag', 'VTmag', 'B-V', 'V-I', 'Hpmag', '(V-I)red', 'd', 'T', 'M_v', 'M_Hip'])

        # Mostrar DataFrame actualizado
        st.write('DataFrame actualizado:')
        st.write(X_new)

        # Widget para seleccionar el modelo
        model_selector = st.selectbox('Selecciona un modelo', (
            'Logistic Regression', 'SVC', 'KNN', 'Gradient Boost', 'XGBoost'))
        st.write('Modelo seleccionado:', model_selector)

        # Seleccionar el modelo adecuado
        if model_selector == 'Logistic Regression':
            model = model_LR
        elif model_selector == 'KNN':
            model = model_KNN
        elif model_selector == 'Gradient Boost':
            model = model_GB
        elif model_selector == 'SVC':
            model = model_SVC
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
