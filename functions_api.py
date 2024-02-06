# FUNCIONES  

import pandas as pd
import numpy as np
import operator
from fastapi import HTTPException

# Dataset que utilizaremos 

df_user_reviews = pd.read_parquet("df_user_reviews.parquet")
df_user_data = pd.read_parquet("df_user_data.parquet")
df_user_for_genre = pd.read_parquet("df_userforgenre.parquet")
df_item_developer_year = pd.read_parquet("df_item_developer_year.parquet")
df_best_developer = pd.read_parquet("df_best_developer.parquet")
df_pivot_norm = pd.read_parquet("df_pivot_norm.parquet")
df_item_sim = pd.read_parquet("df_item_sim.parquet")
df_user_sim = pd.read_parquet("df_user_sim.parquet")


      
def developer(desarrollador: str):
    '''
    Esta función devuelve información sobre una empresa desarrolladora de videojuegos.
         
    Args:
        desarrollador (str): Nombre del desarrollador de videojuegos.
    
    Returns:
        dict: Un diccionario que contiene:
            - 'cantidad_por_año' (dict): Cantidad de items desarrollados por año.
            - 'porcentaje_gratis_por_año' (dict): Porcentaje de contenido gratuito por año de la empresa desarrolladora.
    '''
    try:
        # Filtramos el dataframe por desarrollador de interés
        data_filtrada = df_item_developer_year[df_item_developer_year["developer"] == desarrollador]

        # La cantidad de items por año
        cantidad_por_año = data_filtrada.groupby("release_year")["item_id"].count()

        # La cantidad de elementos gratis por año
        cantidad_gratis_por_año = data_filtrada[data_filtrada["price"] == 0.0].groupby("release_year")["item_id"].count()

        # El porcentaje de elementos gratis por año
        porcentaje_gratis_por_año = (cantidad_gratis_por_año / cantidad_por_año * 100).fillna(0).astype(int)

        # Agregamos el símbolo de porcentaje (%) al valor del porcentaje
        porcentaje_gratis_por_año = porcentaje_gratis_por_año.astype(str) + '%'

        result_dict = {
            "cantidad_por_año": cantidad_por_año.to_dict(),
            "porcentaje_gratis_por_año": porcentaje_gratis_por_año.to_dict()
        }

        return result_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")



def userdata(user_id:str):
    '''
    Esta función devuelve información sobre un usuario según su 'user_id'.
         
    Args:
        user_id (str): Identificador único del usuario.
    
    Returns:
        dict: Un diccionario que contiene información sobre el usuario.
            - 'cantidad_dinero' (int): Cantidad de dinero gastado por el usuario.
            - 'porcentaje_recomendacion' (float): Porcentaje de recomendaciones realizadas por el usuario.
            - 'total_items' (int): Cantidad de items que tiene el usuario.
    '''
    

    try:
        # Filtramos por el usuario 
        user = df_user_reviews[df_user_reviews["user_id"] == user_id]

        # Verificamos si se encontraron datos para el usuario
        if user.empty:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # La cantidad de dinero gastado para el usuario
        cantidad = int(df_user_data[df_user_data["user_id"]== user_id]["price"].iloc[0].item())

        # Buscamos el count_item para el usuario   
        conteo_items = int(df_user_data[df_user_data["user_id"]== user_id]["items_count"].iloc[0].item())

        # Total de recomendaciones realizadas por el usuario 
        total_recomendaciones = user["reviews_recommend"].sum()

        # Total de reviews realizada por todos los usuarios
        total_reviews = len(df_user_reviews["user_id"].unique())

        # Porcentaje de recomendaciones realizadas por el usuario   
        porcentaje_recomendaciones = (total_recomendaciones / total_reviews) * 100

        return {
            "cantidad_dinero": cantidad,
            "porcentaje_recomendacion": round(porcentaje_recomendaciones, 2),
            "total_items": conteo_items
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

def userforgenre(genero):
    '''
    Esta función devuelve el usuario que más horas de juego en un género específico y 
    las horas jugadas por año de lanzamiento.
         
    Args:
        genero (str): Género del videojuego.
    
    Returns:
        dict: Un diccionario que contiene el usuarios con más horas de juego en el género dado y la cantidad de horas jugadas por año.
            - 'top_user' (str): El usuario que más horas jugó dicho género.
            - 'hour_list' : lista de horas jugadas por año.
    '''
    
    try:
        # Filtramos el DataFrame por el género dado
        genre_data = df_user_for_genre[df_user_for_genre["genres"] == genero]

        # Verificamos si hay datos para el género
        if genre_data.empty:
            return f"No hay datos para el género {genero}."

        # Usuario con más horas jugadas para ese género
        top_user = genre_data.loc[genre_data["played_hours"].idxmax()]["user_id"]

        # Lista de acumulación de horas jugadas por año
        hours_by_year = genre_data.groupby("release_year")["played_hours"].sum().reset_index()

        hours_by_year = hours_by_year.rename(columns={"release_year": "Año", "played_hours": "Horas"})

        hours_list = hours_by_year.to_dict(orient="records")

        # Diccionario de retorno
        result = {
            "Usuario con más horas jugadas para Género {}".format(genero): top_user,
            "Horas jugadas": hours_list
        }

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


def best_developer_year(anio):
    """
    Obtiene los mejores desarrolladores de videojuegos para un año específico,
    basándose en comentarios recomendados y positivos.

    Args:
        anio (int): Año para el cual se desea obtener los mejores desarrolladores.

    Returns:
        List[Dict[str, str]]: Una lista de diccionarios que contiene los mejores desarrolladores
        para el año dado. 
    """
    
    try:
        # Filtramos por el año dado y solo con comentarios recomendados y positivos
        df_filtrado = df_best_developer[(df_best_developer["year"] == anio) & (df_best_developer["reviews_recommend"] == True) & (df_best_developer["sentiment_analysis"] == 2)]

        # Verificamos si hay datos para el año
        if df_filtrado.empty:
            return f"No hay datos para el año {anio}."

        # Agrupamos por desarrollador y contamos la cantidad de juegos recomendados
        desarrolladores_top = df_filtrado.groupby("developer")["item_id"].count().reset_index()

        # Verificamos si hay desarrolladores encontrados
        if desarrolladores_top.empty:
            return f"No hay desarrolladores encontrados para el año {anio}."

        # Ordenamos en orden descendente y seleccionar los tres primeros
        desarrolladores_top = desarrolladores_top.sort_values(by="item_id", ascending=False).head(3)

        # Creamos el resultado en el formato deseado
        resultado = [{"Puesto " + str(i+1): desarrollador} for i, desarrollador in enumerate(desarrolladores_top['developer'])]

        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

def developer_reviews_analysis(desarrolladora):
    """
    Analiza los comentarios de una desarrolladora de videojuegos en términos de sentimiento.

    Args:
        desarrolladora (str): Nombre de la desarrolladora de videojuegos.

    Returns:
        dict: Un diccionario que contiene el análisis de sentimiento de los comentarios de la desarrolladora.
            {
                "Desarrolladora": {
                    "Negative": int,  # Cantidad de comentarios negativos
                    "Positive": int   # Cantidad de comentarios positivos
                }
            }

      
    """
    try:
        # Filtramos por desarrolladora
        df_filtrado = df_best_developer[df_best_developer["developer"] == desarrolladora]

        if df_filtrado.empty:
            return f"No hay datos para la desarrolladora {desarrolladora}."

        # Contamos la cantidad de registros con análisis de sentimiento 0, 1 y 2
        conteo_sentimientos = df_filtrado["sentiment_analysis"].value_counts()

        # Convertimos los valores de conteo_sentimientos a tipos nativos de Python
        resultado = {
            desarrolladora: {
                "Negative": int(conteo_sentimientos.get(0, 0)),
                "Positive": int(conteo_sentimientos.get(2, 0))
            }
        }

        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


def recomendacion_juego(game):
    '''
    Muestra una lista de juegos similares a un juego dado.

    Args:
        game (str): El nombre del juego para el cual se desean encontrar juegos similares.

    Returns:
        None: Un diccionario con 5 nombres de juegos recomendados.

    '''
    try:
        # Obtenemos la lista de juegos similares ordenados
        similar_games = df_item_sim.sort_values(by=game, ascending=False).iloc[1:6]

        # Verificamos si hay datos para el juego dado
        if similar_games.empty:
            return f"No hay datos para el juego {game}."

        count = 1
        contador = 1
        recomendaciones = {}

        for item in similar_games:
            if contador <= 5:
                item = str(item)
                recomendaciones[count] = item
                count += 1
                contador += 1
            else:
                break

        return recomendaciones

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

def recomendacion_usuario(user):
    '''
    Genera una lista de los juegos más recomendados para un usuario, 
    basándose en las calificaciones de usuarios similares.

    Args:
        user (str): El nombre de usuario para el cual se desean generar recomendaciones.

    Returns:
        list: Una lista de los juegos más recomendados para el usuario basado en la calificación de usuarios similares.

    '''
    try:
        # Verificamos si el usuario está presente en las columnas de pivot_norm
        if user not in df_pivot_norm.columns:
            return f"No hay datos disponibles para el usuario {user}."

        # Obtenemos los usuarios más similares al usuario dado
        sim_users = df_user_sim.sort_values(by=user, ascending=False).index[1:11]

        best = []  # Juegos mejor calificados por usuarios similares
        most_common = {}  # Cuántas veces se recomienda cada juego

        # Para cada usuario similar, encontraremos el juego mejor calificado y lo agregaremos a la lista 'best'
        for i in sim_users:
            i = str(i)
            max_score = df_pivot_norm.loc[:, i].max()
            best.append(df_pivot_norm[df_pivot_norm.loc[:, i] == max_score].index.tolist())

        # Contamos cuántas veces se recomienda cada juego
        for i in range(len(best)):
            for j in best[i]:
                if j in most_common:
                    most_common[j] += 1
                else:
                    most_common[j] = 1

        # Ordenamos los juegos por la frecuencia de recomendación en orden descendente
        sorted_list = sorted(most_common.items(), key=lambda x: x[1], reverse=True)

        recomendaciones = {}
        contador = 1

        # Devolvemos los 5 juegos más recomendados
        for juego, _ in sorted_list:
            if contador <= 5:
                recomendaciones[contador] = juego
                contador += 1
            else:
                break

        return recomendaciones

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")