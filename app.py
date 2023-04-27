import plotly.io as pio
import requests
from io import BytesIO
import warnings
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly_express as px
import streamlit as st
from streamlit_lottie import st_lottie
import requests
from sys import path
import os
path.append(os.path.abspath(os.path.join('..')))
pio.templates.default = "plotly_dark"


# Configuración de la página
st.set_page_config(page_title="Hipparcos",
                   layout="wide", page_icon="✨", initial_sidebar_state="expanded")
st.set_option("deprecation.showPyplotGlobalUse", False)
warnings.simplefilter(action='ignore', category=FutureWarning)

# Lectura de datos
df_parallax = pd.read_parquet('data/hipparcos_final.parquet')
variables = pd.read_parquet('data/variables.parquet')


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def main():
    # Cambiar la fuente de texto
    st.write(
        """ <style>h1, h2, h3, h4, h5, h6 { font-family: 'roman'; } </style>""", unsafe_allow_html=True)
    # Header
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("# Análisis del catálogo Hipparcos:")
        st.markdown('## Una aproximación a la astrofísica estelar')

    with col2:
        lottie_url_hello = "https://assets8.lottiefiles.com/packages/lf20_afg1tquy.json"
        lottie_hello = load_lottieurl(lottie_url_hello)
        st_lottie(lottie_hello, key="hello", loop=True)

    st.markdown("""---""")
    st.markdown("<center><h2><l style='color:white; font-size: 30px;'>Estudio astronómico de los datos</h2></l></center>", unsafe_allow_html=True)
    st.markdown("""---""")
    # Tabs
    tabs = st.tabs(["Paralaje y movimientos propios",
                    "Clasificación espectral", "La magnitud de las estrellas", "Tab 4", "Tab 5"])

    # Tab 1
    with tabs[0]:
        st.markdown('### Distancias en astronomía: Paralaje')

        cols = st.columns(2)

        with cols[0]:
            st.write("¿Qué es la paralaje?")
            # Agregar el caption

            st.image('img/parallax.jpeg',
                     caption='https://josevicentediaz.com/astronomia-practica/paralajes-estelares-distancias-astronomicas/', use_column_width=True)
            st.latex(r'''d(\text{pasecs})=\frac{1}{p(\text{arcsec})}''')
            st.latex(r'''1 \,\text{pc} = 3,26 \,\text{años-luz}''')
        with cols[1]:
            dist_hist = go.Figure()
            dist_hist.add_trace(go.Histogram(x=df_parallax['d'], nbinsx=100))
            dist_hist.update_layout(title="Distribución de la distancia",
                                    xaxis_title="Distancia [pc]", yaxis_title="Recuento", template='plotly_dark', height=400, width=800)
            st.plotly_chart(dist_hist,  use_container_width=True)
            st.markdown(
                "Cuanto más lejanas son las estrellas más pequeño es el ángulo de la paralaje y por tanto menos medidas.")

        cols = st.columns(1)
        st.markdown("### Movimientos propios de las estrellas")
        mov_propio = px.scatter(df_parallax, x="pmRA", y="pmDE", color="d", range_color=[df_parallax["d"].min(), df_parallax["d"].max()],
                                color_continuous_scale='viridis', opacity=0.7)

        mov_propio.update_layout(
            xaxis_title="Movimiento propio en ascensión recta",
            yaxis_title="Movimiento propio en declinación",
            title="",
            xaxis_range=[-180, 180],
            yaxis_range=[-180, 180],
            coloraxis_colorbar=dict(
                title="distance [pc]"
            ),    template="plotly_dark",
            height=400,
            width=800
        )
        mov_propio.update_traces(
            mode='markers',
            marker=dict(size=2)
        )
        st.plotly_chart(mov_propio, use_container_width=True)
    # Tab 2
    with tabs[1]:
        st.markdown('### Clasificación espectral')
        # Crea una columna categórica con las categorías en el orden deseado
        cat_order = pd.Categorical(df_parallax['Tipo_espectral'],
                                   categories=['O', 'B', 'A',
                                               'F', 'G', 'K', 'M'],
                                   ordered=True)
        df_parallax['Tipo_espectral_orden'] = cat_order

        # Grafica el histograma
        tipo_espec = px.histogram(df_parallax, x="Tipo_espectral_orden",
                                  labels={
                                      "Tipo_espectral_orden": "Tipo espectral", "count": "Recuento"},
                                  category_orders={"Tipo_espectral_orden": [
                                      'O', 'B', 'A', 'F', 'G', 'K', 'M']},
                                  title="Número de estrellas por tipo espectral del catálogo Hipparcos", color='Tipo_espectral')
        tipo_espec.update_yaxes(title="Recuento")
        tipo_espec.update_layout(height=400, width=800)

        # Elimina el dataframe intermedio creado por pd.Categorical
        del cat_order
        st.plotly_chart(tipo_espec, use_container_width=True)

        # Crear la categoría ordenada
        cat_order = pd.Categorical(df_parallax['Clase_espectral'],
                                   categories=['O0', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8', 'O9',
                                               'B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
                                               'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                                               'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                                               'G0', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9',
                                               'K0', 'K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7', 'K8', 'K9',
                                               'M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9'],
                                   ordered=True)

        # Crear una nueva columna con la categoría ordenada
        df_parallax['Clase_espectral_orden'] = cat_order

        # Ordenar el dataframe por la columna Clase_espectral_orden y parallax
        # df_parallax = df_parallax.sort_values(by=['Clase_espectral_orden'])

        # Crear la figura de histograma con la categoría ordenada
        clase = px.histogram(
            df_parallax, x='Clase_espectral_orden', nbins=70, color='Tipo_espectral')

        # Actualizar el diseño de la figura
        clase.update_layout(
            title="Recuento de estrellas por clase espectral",
            xaxis_title="Clase",
            yaxis_title="Cantidad de estrellas",
            bargap=0.1,
            height=600,
            width=1100
        )
        # Eliminar el dataframe intermedio creado por pd.Categorical
        del cat_order
        # Mostrar la figura
        st.plotly_chart(clase, use_container_width=True)

   # Tab 3
    with tabs[2]:
        st.markdown('### La magnitud en astronomía y astrofísica')
        st.markdown(
            '#### Magnitud visual aparente: Estrellas visibles y algunas constelaciones conocidas')

        def filter_visible(data, cutoff_magnitude):
            visible = data[data['Vmag'] < cutoff_magnitude]
            return visible

        visible = filter_visible(df_parallax, cutoff_magnitude=6.5)

        cols = st.columns(2)

        with cols[0]:
            # # Select only necessary columns from the dataframe
            # data = visible[['RAdeg', 'DEdeg', 'Vmag', 'd']]

            # # Reduce the precision of the coordinates to save memory
            # data[['RAdeg', 'DEdeg']] = data[['RAdeg', 'DEdeg']].round(2)

            # Create scatter plot with custom data and defined template
            osa = px.scatter(visible, x='RAdeg', y='DEdeg', color='Vmag', range_x=[220, 140], range_y=[40, 70],
                             color_continuous_scale='Greys', opacity=1, custom_data=['d', 'Vmag'],
                             labels={
                                 'x': 'Ascensión recta [°]', 'y': 'Declinación [°]'},
                             title='Constelación de la Osa Mayor')

            # Add hover template
            osa.update_traces(hovertemplate='<br>'.join([
                'RA: %{x:.2f}',
                'Dec: %{y:.2f}',
                'Distancia: %{customdata[0]:.2f} pc',
                'Magnitud visual: %{customdata[1]:.2f}',
            ]))

            # Update layout
            osa.update_layout(title_x=0.5, height=600, width=800)

            # Show plot
            st.plotly_chart(osa, use_container_width=True)

        with cols[1]:

            # Create scatter plot with custom data
            orion = px.scatter(visible, x='RAdeg', y='DEdeg', color='Vmag',
                               range_x=[120, 40], range_y=[-20, 22], color_continuous_scale='Greys',
                               opacity=1, labels={'RAdeg': 'Ascensión recta [°]', 'DEdeg': 'Declinación [°]'},
                               title='Constelación de Orión',
                               custom_data=['d', 'Vmag'])

            # Update layout
            orion.update_layout(template='plotly_dark',
                                title_x=0.5, height=600, width=800)

            # Add hover template
            orion.update_traces(hovertemplate='<br>'.join([
                'RA: %{x:.2f}',
                'Dec: %{y:.2f}',
                'Distancia: %{customdata[0]:.2f} pc',
                'Magnitud visual: %{customdata[1]:.2f}',
            ]))

            # Show plot
            st.plotly_chart(orion, use_container_width=True)
            del visible

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


if __name__ == '__main__':
    main()
