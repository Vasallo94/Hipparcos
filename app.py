'''
Programa de aplicación de Streamlit para visualizar datos astronómicos del catálogo Hipparcos.

Nota: este código aún no ha sido optimizado para su máxima eficiencia y rapidez. Se aceptan sugerencias y mejoras para hacerlo más elegante y rápido. El código que aparece comentado era la primera versión de este código, parece que ahora con los decoradores de la caché funciona algo mejor, pero se agradecen todas las ideas que puedan ayudar a mejorar el rendimiento y la legibilidad del código. 
'''


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
from utils.func_streamlit import *


path.append(os.path.abspath(os.path.join('..')))


# Configuración de la página
st.set_page_config(page_title="Hipparcos",
                   layout="wide", page_icon="✨", initial_sidebar_state="collapsed")
st.set_option("deprecation.showPyplotGlobalUse", False)
warnings.simplefilter(action='ignore', category=FutureWarning)

# Lectura de datos
df_parallax, variables = load_data()

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
        lottie_stars = load_lottieurl(lottie_url_hello)
        st_lottie(lottie_stars, key="hello", loop=True)

    st.markdown("""---""")
    st.markdown(
        "<center><h2><l style='color:white; font-size: 30px;'>Estudio astronómico de los datos</h2></l></center>", unsafe_allow_html=True)
    st.markdown("""---""")

    # Tabs
    tabs = st.tabs(["Paralaje y movimientos propios",
                    "Clasificación espectral", "La magnitud de las estrellas", "Variabilidad estelar", "Diagrama Herztprung-Russell"])

    # Tab 1
    with tabs[0]:
        st.markdown('### Distancias en astronomía: Paralaje \n')

        cols = st.columns(2)

        with cols[0]:
            # Agregar el caption

            st.image('img/parallax.jpeg',
                     caption='https://josevicentediaz.com/astronomia-practica/paralajes-estelares-distancias-astronomicas/', use_column_width=True)
            st.latex(r'''d(\text{pasecs})=\frac{1}{p(\text{arcsec})}''')
            st.latex(r'''1 \,\text{pc} = 3,26 \,\text{años-luz}''')

        with cols[1]:
            dist_hist = px.histogram(
                df_parallax, x=df_parallax['d'], nbins=100)
            dist_hist.update_layout(title="Distribución de la distancia",
                                    xaxis_title="Distancia [pc]", yaxis_title="Recuento", template='plotly_dark', height=400, width=800)
            st.plotly_chart(dist_hist,  use_container_width=True)
            st.markdown(
                "Cuanto más lejanas son las estrellas más pequeño es el ángulo de la paralaje y por tanto menos medidas.")
        expander = st.expander("Ver explicación")
        expander.write("""\
            Una de las medidas que realizó Hipparcos fue la paralaje estelar, que es la técnica utilizada para determinar la distancia de las estrellas más cercanas a nosotros.
    """)
        expander.write("""\
            La paralaje estelar se basa en el efecto de la perspectiva: cuando observamos un objeto desde dos puntos diferentes, el objeto parece desplazarse ligeramente. En el caso de las estrellas, la Tierra actúa como uno de los puntos de observación, y el otro punto es el centro del sistema solar. Debido al movimiento orbital de la Tierra alrededor del Sol, las estrellas cercanas parecen moverse en el cielo en un patrón anual llamado "paralaje anual".
    """)
        expander.write("""\
            La distancia se calcula utilizando la trigonometría y se expresa en parsecs.
    """)


        st.markdown("### Movimientos propios de las estrellas")

        mov_propio = create_mov_propio_fig(df_parallax)

        st.plotly_chart(mov_propio, use_container_width=True)

        expander = st.expander("Ver explicación")
        expander.write("""\
            El movimiento propio de las estrellas se refiere al desplazamiento aparente que tienen las estrellas en el cielo a lo largo del tiempo, como resultado de su movimiento en relación con el sistema solar. Este movimiento puede ser medido a lo largo de dos direcciones: la ascensión recta y la declinación. Es importante tener en cuenta que este movimiento aparente no es causado por un cambio en la posición real de las estrellas en el espacio, sino más bien por el movimiento del observador en la Tierra y el movimiento de las estrellas en su órbita alrededor de la galaxia. La medición del movimiento propio de las estrellas es una herramienta importante para estudiar la estructura y la dinámica de la Vía Láctea.
            """)


    # Tab 2
    with tabs[1]:
        st.markdown('### Clasificación espectral')
        expander = st.expander("Ver explicación")
        expander.write("""\
            Los tipos espectrales de las estrellas son una clasificación de las estrellas según la apariencia de sus espectros de luz. Esta clasificación se basa en la temperatura efectiva de la estrella y en las líneas espectrales que son características de diferentes elementos químicos presentes en la atmósfera estelar.

            La clasificación más comúnmente utilizada es la clasificación de Harvard, que se basa en una serie de letras que van de la O a la M. Cada letra representa un rango de temperaturas efectivas y una serie de características espectrales. La clasificación se muestra a continuación:

            - O: Estrellas más calientes con temperaturas efectivas superiores a 30.000 K.
            - B: Estrellas con temperaturas efectivas de entre 10.000 y 30.000 K.
            - A: Estrellas con temperaturas efectivas de entre 7.500 y 10.000 K.
            - F: Estrellas con temperaturas efectivas de entre 6.000 y 7.500 K.
            - G: Estrellas como nuestro Sol, con temperaturas efectivas de entre 5.200 y 6.000 K.
            - K: Estrellas con temperaturas efectivas de entre 3.700 y 5.200 K.
            - M: Estrellas más frías con temperaturas efectivas inferiores a 3.700 K.
            """)

        # Mostrar los gráficos
        st.plotly_chart(create_tipo_espec_fig(
            df_parallax), use_container_width=True)
        st.plotly_chart(create_clase_fig(df_parallax),
                        use_container_width=True)

        expander = st.expander("Ver explicación")
        expander.markdown("""\
            Después de las letras O, B, A, F, G, K y M, las estrellas se subclasifican usando números y letras adicionales para indicar características específicas, como la temperatura superficial, la luminosidad y la presencia de líneas espectrales particulares.

            Para las estrellas de clase O, B, A y F, se utilizan los números del 0 al 9 para indicar la subclase. Por ejemplo, una estrella de clase A5 es más caliente que una estrella de clase A7.

            Para las estrellas de clase G, K y M, se utilizan las letras "d" (para enanas) y "g" (para gigantes) para indicar la luminosidad. Por ejemplo, una estrella de clase K3III es una estrella gigante de clase K3.

            Además, las estrellas de clase M también se subdividen en subclases más detalladas utilizando letras adicionales, como "sd" (para subenanas) y "c" (para estrellas carbonadas). Por ejemplo, una estrella de clase M5IIIa es una gigante roja con características espectrales inusuales.

            También se utilizan otras letras adicionales para indicar características especiales, como "e" (para líneas espectrales de emisión) y "p" (para pulsar).
                        """)

# Tab 3
    with tabs[2]:
        st.markdown('### La magnitud en astronomía y astrofísica')
        expander = st.expander('¿Qué es la magnitud?')
        expander.markdown("""
                    La magnitud en astronomía es una medida que se utiliza para describir la luminosidad de los objetos celestes. Se trata de una escala logarítmica en la que se asigna un número a cada objeto en función de su brillo aparente en el cielo nocturno. Esta escala se basa en el trabajo del astrónomo griego Hiparco de Nicea, quien clasificó a las estrellas visibles a simple vista en seis categorías en función de su brillo, denominándolas de la primera a la sexta magnitud.

                    A medida que se ha ido avanzando en el estudio de la astronomía, se ha ampliado la escala de magnitud para incluir objetos más brillantes y más débiles que los contemplados por Hiparco. Así, se ha creado la escala de magnitud absoluta, que se utiliza para medir la luminosidad real de los objetos celestes, y la escala de magnitud aparente, que mide la luminosidad de los objetos tal y como los vemos desde la Tierra.

                    A partir de la magnitud, se pueden obtener diversos datos sobre los objetos celestes, como su distancia, tamaño, temperatura y composición. Por ejemplo, al conocer la magnitud aparente y la magnitud absoluta de un objeto, es posible calcular su distancia a partir de la ley de inversa del cuadrado, que relaciona la luminosidad y la distancia de los objetos celestes. Además, la magnitud también puede utilizarse para identificar objetos celestes y clasificarlos según su brillo y características espectrales.
        """)
        st.markdown(
            '#### Magnitud visual aparente: Estrellas visibles y algunas constelaciones conocidas')
        expander = st.expander('¿Qué es la magnitud visual aparente?')
        expander.markdown("""
                        La magnitud visual de una estrella es una medida de su brillo aparente tal como se ve desde la Tierra. Fue desarrollada por el astrónomo griego Hiparco de Nicea en el siglo II a.C., y se utiliza hasta el día de hoy para clasificar y comparar el brillo de las estrellas.

                        Hiparco desarrolló una escala de magnitud aparente que clasificaba las estrellas en seis categorías según su brillo, siendo la categoría 1 la más brillante y la 6 la menos brillante. Sin embargo, con la mejora de los instrumentos de observación, se descubrió que la escala original de Hiparco no era lo suficientemente precisa y se hicieron ajustes en ella.

                        Hoy en día, la escala de magnitud aparente se ha refinado y extendido a una escala logarítmica en la que un cambio de una unidad en magnitud representa un cambio de aproximadamente 2,5 veces en brillo. Por lo tanto, una estrella de magnitud 1 es aproximadamente 2,5 veces más brillante que una estrella de magnitud 2, y así sucesivamente.

                        La magnitud visual de las estrellas se utiliza para clasificarlas en diferentes categorías según su brillo aparente. Las estrellas más brillantes tienen una magnitud visual negativa, mientras que las estrellas menos brillantes tienen una magnitud visual positiva.

                        Por tanto, la magnitud visual de las estrellas es una medida importante para clasificar y comparar el brillo aparente de las estrellas.
                """)
        
        visible = filter_visible(df_parallax, cutoff_magnitude=6.5)

        cols = st.columns(2)

        with cols[0]:
            osa = custom_scatter(visible, 'RAdeg', 'DEdeg', 'Vmag', [220, 140], [40, 70], 'Greys', 1,
                                 {'RAdeg': 'Ascensión recta [°]',
                                     'DEdeg': 'Declinación [°]'},
                                 'Constelación de la Osa Mayor', ['d', 'Vmag'],
                                 '<br>'.join([
                                     'RA: %{x:.2f}',
                                     'Dec: %{y:.2f}',
                                     'Distancia: %{customdata[0]:.2f} pc',
                                     'Magnitud visual: %{customdata[1]:.2f}',
                                 ]))
            st.plotly_chart(osa, use_container_width=True)

        with cols[1]:
            orion = custom_scatter(visible, 'RAdeg', 'DEdeg', 'Vmag', [120, 40], [-20, 22], 'Greys', 1,
                                   {'RAdeg': 'Ascensión recta [°]',
                                       'DEdeg': 'Declinación [°]'},
                                   'Constelación de Orión', ['d', 'Vmag'],
                                   '<br>'.join([
                                       'RA: %{x:.2f}',
                                       'Dec: %{y:.2f}',
                                       'Distancia: %{customdata[0]:.2f} pc',
                                       'Magnitud visual: %{customdata[1]:.2f}',
                                   ]))
            st.plotly_chart(orion, use_container_width=True)
            del visible


        # Llamar a la función para crear las visualizaciones
        mag, dist_type = create_visualizations(df_parallax)

        # Mostrar las visualizaciones
        st.plotly_chart(mag, use_container_width=True)
        st.plotly_chart(dist_type, use_container_width=True)

        # Resetear el índice del DataFrame
        df_parallax.reset_index(drop=True, inplace=True)


        cols = st.columns(2)

        # Llamar a las funciones para crear las gráficas
        with cols[0]:
            magnitudes = create_magnitudes_plot(df_parallax)
            st.plotly_chart(magnitudes, use_container_width=True)

        with cols[1]:
            cumulative = create_cumulative_plot(df_parallax)
            st.plotly_chart(cumulative, use_container_width=True)
            expander = st.expander("Más información")
            expander.write("""
                La distribución acumulada de estrellas es una forma de visualizar la distribución de estrellas en una muestra particular. En la práctica, los astrónomos estudian una gran cantidad de estrellas y trazan su distribución acumulada, que es una forma de mostrar cuántas estrellas tienen cierto valor de un parámetro particular, como su magnitud visual aparente.

                La pendiente de la curva está directamente relacionada con la densidad numérica de estrellas, que es la cantidad de estrellas por unidad de volumen. Este es un parámetro importante para la cosmología, ya que está relacionado con la distribución de materia en el universo. Al medir la densidad numérica de estrellas en diferentes regiones del cielo, los astrónomos pueden estudiar la estructura a gran escala del universo y verificar el principio cosmológico, que establece que el universo es homogéneo e isotrópico a gran escala.

                Al comparar la densidad numérica de estrellas en diferentes regiones del cielo, los astrónomos también pueden estudiar los efectos de los cúmulos de galaxias y otras estructuras a gran escala en la distribución de materia en el universo. Esto puede proporcionar pistas importantes sobre la naturaleza de la materia oscura y la energía oscura, que se cree que son los componentes dominantes del universo pero no son directamente observables.

                La distribución acumulada de estrellas es una herramienta importante para que los astrónomos estudien la estructura a gran escala del universo y verifiquen nuestra comprensión actual de la cosmología.
                """)


    # Tab 4
    with tabs[3]:
        st.markdown('## Estrellas variables')
        expander = st.expander("¿Qué son las estrellas variables?")
        expander.write("""
            Las estrellas variables son aquellas cuya luminosidad cambia con el tiempo. Estos cambios pueden ser periódicos o no periódicos y se deben a una variedad de razones, como cambios en la temperatura, la densidad o la composición de la estrella, o la presencia de compañeros estelares cercanos.

            Las estrellas variables son importantes para los astrónomos porque proporcionan información valiosa sobre la estructura interna de las estrellas y la evolución estelar. Al estudiar cómo cambia la luminosidad de una estrella variable a lo largo del tiempo, los astrónomos pueden inferir su masa, edad, temperatura y otros parámetros importantes.

            Además, las estrellas variables son importantes para la cosmología porque se utilizan como indicadores de distancia en el universo cercano. Al medir el brillo aparente de una estrella variable y compararlo con su brillo intrínseco conocido, los astrónomos pueden estimar la distancia a la estrella y, por lo tanto, a la galaxia en la que se encuentra.

            Hay muchos tipos diferentes de estrellas variables, que se clasifican en función de sus características de luz y los mecanismos que impulsan sus cambios de luminosidad. Algunos ejemplos comunes incluyen:

            - Estrellas pulsantes: estrellas cuya luminosidad cambia debido a la expansión y contracción periódicas de su superficie. Ejemplos incluyen las Cefeidas y las RR Lyrae.
            - Estrellas eruptivas: estrellas cuya luminosidad aumenta repentinamente debido a la liberación de energía almacenada en su interior. Ejemplos incluyen las novas y las supernovas.
            - Estrellas eclipsantes: estrellas que parecen disminuir en brillo periódicamente debido al oscurecimiento mutuo de dos estrellas en órbita cercana. Ejemplos incluyen las binarias eclipsantes.
            - Estrellas variables cataclísmicas: estrellas que experimentan cambios dramáticos en su luminosidad debido a la transferencia de masa de una estrella a otra en un sistema binario cercano.
            """)
        variab = px.histogram(variables, x="Period", nbins=200, log_y=True, template='plotly_dark',
                              title="Histograma del período estelar en el catálogo Hipparcos")
        tipo_espectral_order = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
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
        expander = st.expander(
            "¿Qué quieren decir estos tipos de variabilidad?")
        expander.write("""
                Los diferentes tipos de variabilidad estelar significan lo siguiente:

                - C: No se detectó variabilidad ("constante")
                - D: Variabilidad inducida por duplicidad 
                - M: Posiblemente micro-variable, con amplitud < 0.03 mag (las estrellas clasificadas con alta confianza como micro-variable se marcan como U)
                - P: Variable periódica
                - R: El índice de color V-I fue revisado durante el análisis de variabilidad
                - U: Variable no resuelta que no se encuentra en las otras categorías; esta clase también incluye variables irregulares o semi-regulares, y posiblemente variables con amplitud > 0 ~ 0.03 mag
                
                El porcentaje de nulos en la columna del periodo es mucho mayor (97.85% nulos) que el porcentaje en la columna Tipo de Variabilidad (39.41% de nulos), por tanto habrá muchas más estrellas en la clasificación C que en las demás.
                    """)

    # Tab 5
    with tabs[4]:
        st.markdown('### El diagrama Hertzsprung-Russell')
        expander = st.expander("¿Qué es el diagrama Hertzsprung-Russell?")
        expander.markdown("""
                          El diagrama de Hertzsprung-Russell (HR) es uno de los diagramas más importantes en la astronomía estelar. Fue creado por Ejnar Hertzsprung y Henry Norris Russell en la década de 1910 y es una representación gráfica de la luminosidad estelar en función de su temperatura superficial.
                          En el eje vertical del diagrama, se representa la luminosidad estelar en unidades solares $(L/L_\odot)$, mientras que en el eje horizontal se representa la temperatura superficial estelar en grados Kelvin. De esta forma, las estrellas más luminosas y calientes se sitúan en la parte superior izquierda del diagrama, mientras que las menos luminosas y frías se sitúan en la parte inferior derecha.
                          
                          El diagrama HR permite a los astrónomos clasificar las estrellas según su luminosidad, temperatura y otros parámetros. Por ejemplo, las estrellas de la secuencia principal se sitúan en una banda diagonal que atraviesa el diagrama, conocida como la secuencia principal. También se pueden identificar otras regiones como las gigantes rojas, las supergigantes, las enanas blancas, entre otras.
                          
                          Además, el diagrama HR es una herramienta importante para el estudio de la evolución estelar, ya que permite observar cómo las estrellas cambian a medida que avanzan en su ciclo de vida. De hecho, la posición de una estrella en el diagrama HR puede proporcionar información sobre su edad, masa, estado evolutivo y destino final.
                          
                          Así pues, el diagrama de Hertzsprung-Russell es una herramienta fundamental en la astronomía estelar que permite clasificar, estudiar y entender las propiedades y la evolución de las estrellas.
        """)

        st.markdown('#### La magnitud absoluta y el índice de color')
        expander = st.expander("La magnitud absoluta")
        expander.markdown("""
                          La __magnitud absoluta__ se refiere a la cantidad de luz que emite una estrella y se define como la magnitud aparente que tendría si estuviera a una distancia de 10 parsecs (32,6 años luz) de la Tierra. La magnitud aparente, por otro lado, es la medida de la luminosidad de una estrella tal como se ve desde la Tierra. Es importante destacar que la magnitud absoluta de una estrella es independiente de su distancia a la Tierra y, por lo tanto, es una medida más precisa de su luminosidad que la magnitud aparente.
                        La magnitud absoluta se calcula, con respecto de la magnitud relativa y la distancia, como sigue:""")

        st.latex(r'''M = m - 5 \times \log_{10}\left(d_{pc} \right) + 5''')

        expander = st.expander(
            'El índice de color y la temperatura superficial')
        expander.markdown("""
                          Por otro lado, el __índice de color__ es una medida de la temperatura de una estrella. Se calcula comparando la magnitud aparente de la estrella en dos bandas de color diferentes, generalmente la banda B (azul) y la banda V (visual). El índice de color se define como la diferencia de magnitud entre la banda B y la banda V. Si una estrella tiene un índice de color pequeño, significa que emite más luz en la banda V que en la banda B, lo que sugiere que su temperatura es relativamente baja. Por otro lado, si el índice de color es grande, la estrella emite más luz en la banda B que en la banda V, lo que sugiere que su temperatura es relativamente alta. 

                        Para calcular la temperatura superficial de las estrellas haremos uso de la fórmula:
                            """)

        st.latex(r'''T = \frac{8540\,\text{K}}{(B-V)+0.865}''')
        cols = st.columns(2)

        with cols[0]:
            st.plotly_chart(generar_HR(df_parallax), use_container_width=True)

        with cols[1]:
            st.plotly_chart(generar_HR2(df_parallax), use_container_width=True)
        col1, col2 = st.columns(2)
        with cols[0]:
            st.plotly_chart(generar_HR3D(df_parallax),
                            use_container_width=True)

        with cols[1]:
            st.image('img/HR.jpeg', use_column_width='auto')

if __name__ == '__main__':
    main()
