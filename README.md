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
Los detalles del ETL se puede ver en 

