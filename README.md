# Sistema de Recomendación de Videojuegos

## introducción

Este proyecto simula el rol integral de un MLOps Engineer, fusionando las funciones de un Data Engineer y Data Scientist. Esta iniciativa representa una parte esencial de la fase de LABS en el bootcamp de Henry, enfocándose en la práctica de habilidades técnicas y soft skills necesarias en el mercado laboral. Se desarrolló un caso de negocio real utilizando conjuntos de datos públicos de la industria de videojuegos, específicamente de la plataforma videojuegos Steam. La meta principal fue desarrollar un Producto Mínimo Viable (MVP) que incluya una API desplegada en un servicio en la nube. El proyecto se basó en conjuntos de datos proporcionados y tenía como objetivo la implementación de dos modelos de Machine Learning. Estos modelos abordan la tarea de realizar un análisis de sentimientos sobre los comentarios de usuarios de juegos, así como proporcionar recomendaciones de juegos basadas en el nombre de un juego o en los gustos de un usuario en particular.

## Herramientas utilizadas
  * Visual Studio Code como editor de codigo
  * Python como lenguaje de programacion
  * GitHub como repositorio del proyecto
  * FastAPI como framework
  * Render
## Etapas del proyecto 
  ### Transformación de datos:
En esta etapa de ingenieria de datos se realizó un proceso de ETL, extracción, transformación y carga, donde se recibió 3 archivos JSON con información acerca de los videjuegos, los jugadores y las reseñas de estos. Dos de los conjuntos de datos presentaban estructuras anidadas, es decir, contenían columnas que almacenaban diccionarios o listas de diccionarios. Se implementaron diversas estrategias para convertir las claves de estos diccionarios en columnas separadas. Posteriormente, se llevaron a cabo acciones para gestionar los valores nulos en variables críticas para el proyecto. Además, se eliminaron columnas con un alto número de valores nulos o aquellas que no contribuían significativamente al proyecto, con el objetivo de mejorar el rendimiento de la API y considerando las restricciones de almacenamiento en el deploy.

 * [Steam Games ETL](https://github.com/CristVald/Game-recommendation-system-PI/blob/main/Jupyter%20Notebooks/1_steam_games_ETL.ipynb) en este archivo trabajamos la información sobre los juegos disponibles en la plataforma Steam, también incluye datos como géneros, etiquetas, especificaciones, desarrolladores, año de lanzamiento, precio y otros atributos relevantes de cada juego.
 * [User Items ETL](https://github.com/CristVald/Game-recommendation-system-PI/blob/main/Jupyter%20Notebooks/1_user_items_ETL.ipynb) en este archivo realizamos el proceso de ETL sobre los ítems relacionados con usuarios australiano. También debimos realizar un proceso de desanidado porque encontramos listas como datos. 
 * [User Reviews ETL](https://github.com/CristVald/Game-recommendation-system-PI/blob/main/Jupyter%20Notebooks/1_user_reviews_ETL.ipynb) en este archivo realizamos el proceso de ETL sobre las reseñas de juegos específicamente realizadas por usuarios australianos.Aquí también observamos la presencia de listas las cuales tuvimos que desanidar.

 ### Feature engineering

Una de las solicitudes para este proyecto consistió en aplicar un análisis de sentimiento a las reseñas de los usuarios. Para lograr esto, se introdujo una nueva columna llamada 'sentiment_analysis' en sustitución de la columna que originalmente contenía las reseñas. Esta nueva columna clasifica los sentimientos de los comentarios según la siguiente escala:

* 0 para comentarios negativos,
* 1 para comentarios neutrales o sin reseña, y
* 2 para comentarios positivos.

En el contexto de esta prueba de concepto, se implementó un análisis de sentimiento básico utilizando TextBlob, una biblioteca de procesamiento de lenguaje natural (NLP) en Python.
