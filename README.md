- [Análisis del catálogo astronómico Hipparcos](#análisis-del-catálogo-astronómico-hipparcos)
  - [Estructura del proyecto](#estructura-del-proyecto)
  - [Análisis de datos](#análisis-de-datos)
  - [App de Streamlit](#app-de-streamlit)
  - [Cómo ejecutar el código](#cómo-ejecutar-el-código)
  - [TO-DO](#to-do)
  - [Contribuciones](#contribuciones)


# Análisis del catálogo astronómico Hipparcos
Este es un proyecto que busca analizar el catálogo astronómico Hipparcos, que contiene información detallada sobre las estrellas de nuestra galaxia. El objetivo es utilizar técnicas de análisis de datos para extraer información útil sobre la distribución y características de las estrellas en nuestra galaxia.

![Diagrama Hertzsprung-Russell](img/HR.png)

Si quieres ver la presentación de los datos pincha [aquí](https://www.linkedin.com/posts/enrique-vasallo_data-science-github-activity-7060328901415190528-NmH8?utm_source=share&utm_medium=member_desktop)

## Estructura del proyecto
El proyecto está organizado de la siguiente manera:

- data/: Carpeta que contiene los archivos de datos del catálogo Hipparcos en formato CSV, así como otros datos necesarios para diferentes partes del proyecto en formato parquet.
- notebooks/: Carpeta que contiene los Jupyter Notebooks utilizados para realizar el análisis de datos, entrenamiento y evaluación de modelos de machine learning, etc.
- app.py : La aplicación principal desarrollada con Streamlit, donde podemos aprender más sobre los parámetros estelares y la información que aporta el catálogo Hipparcos.
- pages/: Carpeta que contiene páginas complementarias a la app principal de Streamlit, como una página de información sobre el satélite Hipparcos y otra que permite clasificar estrellas según sus características.
- utils/: Carpeta que contiene una serie de funciones útiles que se han ido utilizando durante el desarrollo del proyecto.
- img/: Carpeta que contiene imágenes que se usan durante el proyecto, como imágenes de estrellas y gráficos generados durante el análisis de datos.
- output/: Carpeta que contiene los modelos de Machine Learning que son usados en la app de streamlit para la clasificación estelar, en formato pickle.

## Análisis de datos
En el análisis de datos se empleó Python y varias librerías populares, tales como Pandas, NumPy, Matplotlib y Scikit-learn. Los Jupyter Notebooks, que se encuentran en la carpeta notebooks/, contienen todo el código utilizado para llevar a cabo el análisis, junto con explicaciones detalladas de cada paso del proceso.

Algunos de los análisis realizados incluyen:

- Preprocesamiento de datos utilizando el algoritmo KNN.
- Visualización de la distribución de estrellas en nuestra galaxia.
- Análisis de la distribución de temperaturas y luminosidades de las estrellas.
- Identificación de patrones y agrupaciones de estrellas en el catálogo.
- Implementación de modelos de machine learning para la clasificación estelar.

## App de [Streamlit](https://vasallo94-hipparcos-app-m3yxrf.streamlit.app/ "Cuando la abras dale tiempo a que termine de correr la app")

## Cómo ejecutar el código
Para ejecutar el código en este proyecto, se recomienda clonar el repositorio y crear un entorno virtual de Python utilizando virtualenv o conda. A continuación, se deben instalar las dependencias listadas en el archivo requirements.txt. Finalmente, los Jupyter Notebooks se pueden ejecutar desde la carpeta notebooks/.

## TO-DO
- Realizar un análisis más detallado de la luminosidad, masa y radio de las estrellas del catálogo.
- Estudiar más a fondo la variabilidad estelar, los sistemas binarios y los cúmulos estelares
- Crear mapas de la Vía Láctea para visualizar la distribución de estrellas.
- Optimizar la app de Streamlit y el cuaderno principal hipparcos.ipynb para reducir su peso.

## Contribuciones
Se agradecen las contribuciones al proyecto y cualquier sugerencia. Si deseas contribuir, asegúrate de crear una rama separada y enviar una solicitud de extracción una vez que hayas finalizado tus cambios. También se agradecen los informes de errores y las sugerencias de mejoras.

