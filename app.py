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

# Lectura de datos
df_parallax = pd.read_parquet('data/hipparcos_final.parquet')
variables = pd.read_parquet('data/variables.parquet')


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def main():
    @st.cache
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
        lottie_stars = load_lottieurl(lottie_url_hello)
        st_lottie(lottie_stars, key="hello", loop=True)

    st.markdown("""---""")
    st.markdown("<center><h2><l style='color:white; font-size: 30px;'>Estudio astronómico de los datos</h2></l></center>", unsafe_allow_html=True)
    st.markdown("""---""")

    # Tabs
    tabs = st.tabs(["Paralaje y movimientos propios",
                    "Clasificación espectral", "La magnitud de las estrellas", "Variabilidad estelar", "Diagrama Herztprung-Russell"])

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

            # Create scatter plot with custom data and defined template
            osa = px.scatter(visible, x='RAdeg', y='DEdeg', color='Vmag', range_x=[220, 140], range_y=[40, 70],
                             color_continuous_scale='Greys', opacity=1, custom_data=['d', 'Vmag'],
                             labels={
                                 'x': 'Ascensión recta [°]', 'y': 'Declinación [°]'},
                             title='Constelación de la Osa Mayor')
            osa.update_layout(height=600, width=800)
            # Add hover template
            osa.update_traces(hovertemplate='<br>'.join([
                'RA: %{x:.2f}',
                'Dec: %{y:.2f}',
                'Distancia: %{customdata[0]:.2f} pc',
                'Magnitud visual: %{customdata[1]:.2f}',
            ]))

            # Show plot
            st.plotly_chart(osa, use_container_width=True)

        with cols[1]:
            # Create scatter plot with custom data
            orion = px.scatter(visible, x='RAdeg', y='DEdeg', color='Vmag',
                               range_x=[120, 40], range_y=[-20, 22], color_continuous_scale='Greys',
                               opacity=1, labels={'RAdeg': 'Ascensión recta [°]', 'DEdeg': 'Declinación [°]'},
                               title='Constelación de Orión',
                               custom_data=['d', 'Vmag'])
            orion.update_layout(height=600, width=800)

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

        mag = px.histogram(df_parallax, x="Vmag", nbins=100)
        mag.update_layout(
            xaxis_title="Magnitud visual aparente",
            yaxis_title="Recuento",
            title="Distribución de estrellas según su magnitud aparente",
            height=600,
            width=1000,)
        st.plotly_chart(mag, use_container_width=True)

        tipo_espectral_order = ['O', 'B', 'A', 'F', 'G', 'K', 'M']

        # Ordenar el DataFrame por la variable categórica 'Tipo_espectral'
        df_parallax_sorted = df_parallax.sort_values('Tipo_espectral', key=lambda x: pd.Categorical(
            x, categories=tipo_espectral_order, ordered=True))
        # Crear la figura
        dist_type = px.histogram(df_parallax_sorted, x="Vmag", color="Tipo_espectral", nbins=100,
                                 title='Distribución de las magnitudes visuales con base en el tipo espectral de las estrellas')

        # Actualizar el orden de la leyenda y los títulos de los ejes
        dist_type.update_layout(
            legend=dict(
                traceorder="normal",
                title="Tipo espectral",
                itemsizing='constant'
            ),
            xaxis=dict(
                title="Magnitud visual aparente"
            ),
            yaxis=dict(
                title="Recuento"
            ),
            height=600,
            width=1000
        )

        # Mostrar la figura
        st.plotly_chart(dist_type, use_container_width=True)

        df_parallax.reset_index(drop=True, inplace=True)

        cols = st.columns(2)

        with cols[0]:
            hist_data = [df_parallax["BTmag"],
                         df_parallax["VTmag"], df_parallax["Hpmag"]]

            group_labels = ['Magnitud BT aparente',
                            'Magnitud VT aparente', 'Magnitud HP aparente']

            # Crear el distplot con el tamaño personalizado de los bins
            magnitudes = ff.create_distplot(
                hist_data, group_labels, bin_size=0.2)

            # Actualizar el diseño
            magnitudes.update_layout(
                title='Distribución de magnitudes en el catálogo Hipparcos',
                xaxis_title='Magnitud aparente',
                yaxis_title='Densidad',
                height=600,
                width=1000)

            # Mostrar el gráfico
            st.plotly_chart(magnitudes, use_container_width=True)

        with cols[1]:
            # Crear el histograma con distribución acumulada
            cumulative = px.histogram(df_parallax, x="Vmag", nbins=50, cumulative=True,
                                      title="Distribución de la magnitud visual aparente (Acumulativo)",
                                      labels={'Vmag': 'Magnitud aparente visual'})

            # Cambiar el título y los nombres de los ejes a español
            cumulative.update_layout(
                xaxis_title='Magnitud aparente V', yaxis_title='Recuento')
            cumulative.update_traces(
                hovertemplate="Magnitud aparente visual: %{x}")
            cumulative.update_layout(
                height=600,
                width=1000,
                template="plotly_dark")

            # Mostrar el gráfico
            st.plotly_chart(cumulative, use_container_width=True)
    # Tab 4
    with tabs[3]:
        variab = px.histogram(variables, x="Period", nbins=200, log_y=True, template='plotly_dark',
                              title="Histograma del período estelar en el catálogo Hipparcos")

        # Actualizar el diseño
        variab.update_layout(xaxis_title="Período [Días]", yaxis_title="log(N)",
                             height=600,
                             width=1000)
        st.plotly_chart(variab, use_container_width=True)

        var_type = px.histogram(variables, x='HvarType', color='HvarType',
                                title='Distribución del tipo de variabilidad estelar en el catálogo Hipparcos',
                                template='plotly_dark')
        var_type.update_layout(xaxis_title='Tipo de variabilidad',
                               yaxis_title='Recuento',
                               height=600,
                               width=1000)
        st.plotly_chart(var_type, use_container_width=True)

    # Tab 5
    with tabs[4]:
        st.latex(r'''M = m - 5 \times \log_{10}\left(d_{pc} \right) + 5''')
        st.latex(r'''T = \frac{8540\,\text{K}}{(B-V)+0.865}''')
        cols = st.columns(2)

        with cols[0]:
            df_parallax['Tipo_espectral'] = pd.Categorical(
                df_parallax['Tipo_espectral'], categories=tipo_espectral_order)

            # Crear el gráfico HR
            HR = px.scatter(x=df_parallax['B-V'],
                            y=df_parallax['M_v'],
                            color=df_parallax["Tipo_espectral"])

            # Configurar los ejes y la leyenda
            HR.update_layout(
                xaxis_title="B-V [mag]",
                yaxis_title="M_v [mag]",
                yaxis=dict(autorange='reversed'),
                height=900,
                width=900,
                legend=dict(
                    traceorder="normal",
                    title="Tipo espectral",
                    itemsizing='constant'
                ),
                title="Diagrama HR"
            )

            # Add hover template
            HR.update_traces(hovertemplate='<br>'.join([
                'B-V: %{x:.2f}',
                'Magnitud absoluta: %{y:.2f}'
            ]))

            # Configurar los marcadores
            HR.update_traces(
                mode='markers',
                marker=dict(size=1.5)
            )

            # Mostrar el gráfico
            st.plotly_chart(HR, use_container_width=True)

        with cols[1]:

            # Configurar el gráfico HR3
            HR2 = px.scatter(x=df_parallax['V-I'],
                             y=df_parallax['M_Hip'],
                             color=df_parallax["T"],
                             color_continuous_scale=px.colors.sequential.RdBu,
                             labels={'color': 'Temperatura [K]'},
                             title='HR Temperatura')

            # Configurar los ejes y la leyenda
            HR2.update_layout(
                xaxis_title="V-I [mag]",
                yaxis_title=r"M_{Hip}\,[mag]",
                yaxis=dict(autorange='reversed'),
                height=900,
                width=900,
                legend=dict(
                    traceorder="normal",
                    title="Clase espectral",
                    itemsizing='constant'
                )
            )

            # Configurar los marcadores
            HR2.update_traces(
                mode='markers',
                marker=dict(size=2)
            )

            HR2.update_traces(hovertemplate='<br>'.join([
                'V-I: %{x:.2f}',
                'M: %{y:.2f}']
            ))

            # Limitar el rango del eje x
            HR2.update_xaxes(range=[-1.5, 6])

            # Mostrar el gráfico
            st.plotly_chart(HR2, use_container_width=True)

        col1, col2 = st.columns(2)
        with cols[0]:
            # Crear el gráfico HR3D
            HR3D = px.scatter_3d(x=df_parallax['V-I'],
                                 y=df_parallax['M_Hip'],
                                 z=df_parallax['T'],
                                 color=df_parallax["Tipo_espectral"])

            # Configurar los ejes y la leyenda
            HR3D.update_layout(
                scene=dict(
                    xaxis_title="Índice V-I",
                    yaxis_title="Magnitud absoluta",
                    zaxis_title="Temperatura",
                ),
                xaxis=dict(autorange='reversed'),
                yaxis=dict(autorange='reversed'),
                height=900,
                width=900,
                legend=dict(
                    traceorder="normal",
                    title="Tipo espectral",
                    itemsizing='constant'
                )
            )

            HR3D.update_traces(hovertemplate='<br>'.join([
                'V-I: %{x:.2f}',
                'M: %{y:.2f}',
                'T: %{z:.2f} K',
            ]))
            # Configurar los marcadores
            HR3D.update_traces(
                mode='markers',
                marker=dict(size=1.5)
            )
            st.plotly_chart(HR3D, use_container_width=True)
        with cols[1]:
            st.image('img/HR.jpeg', width=900)


if __name__ == '__main__':
    main()
