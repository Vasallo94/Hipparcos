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


pio.templates.default = "plotly_dark"
tipo_espectral_order = ['O', 'B', 'A', 'F', 'G', 'K', 'M']

colores = {
    'O': 'violet',
    'B': 'blue',
    'A': 'lightblue',
    'F': 'white',
    'G': 'yellow',
    'K': 'orange',
    'M': 'red'
}
clase_espectral_order = ['O0', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8', 'O9',
                         'B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
                         'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                         'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                         'G0', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9',
                         'K0', 'K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7', 'K8', 'K9',
                         'M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9']


@st.cache_data()
def load_data():
    df_parallax = pd.read_parquet('data/hipparcos_final.parquet')
    variables = pd.read_parquet('data/variables.parquet')
    return df_parallax, variables


@st.cache_data()
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


@st.cache_data()
def create_mov_propio_fig(df):
    mov_propio = px.scatter(df, x="pmRA", y="pmDE", color="d", range_color=[df["d"].min(), df["d"].max()],
                            color_continuous_scale='viridis', opacity=0.7)

    mov_propio.update_layout(
        xaxis_title="Movimiento propio en ascensión recta",
        yaxis_title="Movimiento propio en declinación",
        title="",
        xaxis_range=[-180, 180],
        yaxis_range=[-180, 180],
        coloraxis_colorbar=dict(
            title="Distancia [pc]"
        ),    template="plotly_dark",
        height=400,
        width=800
    )
    mov_propio.update_traces(
        mode='markers',
        marker=dict(size=2)
    )
    return mov_propio


@st.cache_data()
def create_tipo_espec_fig(df):
    fig = px.histogram(df, x="Tipo_espectral",
                       labels={"Tipo_espectral": "Tipo espectral",
                               "count": "Recuento"},
                       category_orders={"Tipo_espectral": [
                           'O', 'B', 'A', 'F', 'G', 'K', 'M']},
                       title="Número de estrellas por tipo espectral del catálogo Hipparcos", color='Tipo_espectral', color_discrete_map=colores)
    fig.update_yaxes(title="Recuento")
    fig.update_layout(height=400, width=800)
    return fig


@st.cache_data()
def create_clase_fig(df):
    fig = px.histogram(df, x='Clase_espectral',
                       nbins=70, color='Tipo_espectral',
                       category_orders={'Clase_espectral': ['O0', 'O1', 'O2', 'O3', 'O4', 'O5', 'O6', 'O7', 'O8', 'O9',
                                                            'B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9',
                                                            'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                                                            'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                                                            'G0', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9',
                                                            'K0', 'K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7', 'K8', 'K9',
                                                            'M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9']},  color_discrete_map=colores)
    fig.update_layout(title="Recuento de estrellas por clase espectral", xaxis_title="Clase espectral",
                      yaxis_title="Cantidad de estrellas", bargap=0.1, height=600, width=1100)
    return fig


@st.cache_data()
def filter_visible(data, cutoff_magnitude):
    visible = data[data['Vmag'] < cutoff_magnitude]
    return visible


@st.cache_data()
def custom_scatter(data, x, y, color, range_x, range_y, color_continuous_scale, opacity, labels, title, custom_data, hovertemplate):
    scatter = px.scatter(data, x=x, y=y, color=color, range_x=range_x, range_y=range_y,
                         color_continuous_scale=color_continuous_scale, opacity=opacity, labels=labels,
                         title=title, custom_data=custom_data)
    scatter.update_layout(height=600, width=800)
    scatter.update_traces(hovertemplate=hovertemplate)
    return scatter


@st.cache_data()
def create_visualizations(df_parallax):

    # Crear histograma de la magnitud visual aparente
    mag = px.histogram(df_parallax, x="Vmag", nbins=100)
    mag.update_layout(
        xaxis_title="Magnitud visual aparente",
        yaxis_title="Recuento",
        title="Distribución de estrellas según su magnitud aparente",
        height=600,
        width=1000,
    )

    # Ordenar el DataFrame por el tipo espectral
    df_parallax_sorted = df_parallax.sort_values(
        'Tipo_espectral', key=lambda x: pd.Categorical(
            x, categories=tipo_espectral_order, ordered=True
        )
    )

    # Crear histograma de la magnitud visual aparente con el tipo espectral
    dist_type = px.histogram(
        df_parallax_sorted, x="Vmag", color="Tipo_espectral", nbins=100,
        title='Distribución de las magnitudes visuales con base en el tipo espectral de las estrellas'
    )

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

    return mag, dist_type


@st.cache_data()
def create_magnitudes_plot(df_parallax):
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

    return magnitudes


@st.cache_data()
def create_cumulative_plot(df_parallax):
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

    return cumulative


@st.cache_data()
def generar_HR(df_parallax):
    df_parallax['Tipo_espectral'] = pd.Categorical(
        df_parallax['Tipo_espectral'], categories=tipo_espectral_order)

    # Crear el gráfico HR
    HR = px.scatter(x=df_parallax['B-V'],
                    y=df_parallax['M_v'],
                    color=df_parallax["Tipo_espectral"], color_discrete_map=colores)

    # Configurar los ejes y la leyenda
    HR.update_layout(
        xaxis_title="B-V [mag]",
        yaxis_title="Magnitud absoluta [mag]",
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

    return HR


@st.cache_data()
def generar_HR2(df_parallax):
    # Configurar el gráfico HR2
    HR2 = px.scatter(x=df_parallax['V-I'],
                     y=df_parallax['M_Hip'],
                     color=df_parallax["T"],
                     color_continuous_scale=px.colors.sequential.RdBu,
                     labels={'color': 'Temperatura [K]'},
                     title='HR Temperatura')

    # Configurar los ejes y la leyenda
    HR2.update_layout(
        xaxis_title="V-I [mag]",
        yaxis_title="Magnitud Absoluta Hipparcos [mag]",
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

    return HR2


def generar_HR3D(df_parallax):
    # Crear el gráfico HR3D
    HR3D = px.scatter_3d(x=df_parallax['V-I'],
                         y=df_parallax['M_Hip'],
                         z=df_parallax['T'],
                         color=df_parallax["Tipo_espectral"], color_discrete_map=colores)

    # Configurar los ejes y la leyenda
    HR3D.update_layout(
        scene=dict(
            xaxis_title="Índice V-I [mag]",
            yaxis_title="Magnitud absoluta [mag]",
            zaxis_title="Temperatura [K]",
        ),
        xaxis=dict(autorange='reversed'),
        yaxis=dict(autorange='reversed'),
        height=900,
        width=900,
        legend=dict(
            traceorder="normal",
            title="Tipo espectral",
            itemsizing='constant'
        ),
        title="Diagrama HR 3D"
    )

    # Add hover template
    HR3D.update_traces(hovertemplate='<br>'.join([
        'V-I: %{x:.2f}',
        'Magnitud absoluta: %{y:.2f}',
        'Temperatura: %{z:.2f} K'
    ]))

    # Configurar los marcadores
    HR3D.update_traces(
        mode='markers',
        marker=dict(size=1.5)
    )

    return HR3D
