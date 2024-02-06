import pandas as pd
from textblob import TextBlob as TB
import re

def ver_tipo_datos(df):
    '''
    Obtiene los tipos de datos en un dataFrame y si este contiene valores nulos.

    Parameters:
        df (pandas.DataFrame): El DataFrame que queremos analizar.

    Returns:
        pandas.DataFrame: Un DataFrame que contiene el resumen de cada columna, 
        incluyendo:
        - "nombre_campo": Nombre de la columna.
        - "tipo_datos": Tipos de datos únicos presentes por columna.
        - "no_nulos_%": Porcentaje de valores no nulos por columna.
        - "nulos_%": Porcentaje de valores nulos por columna.
        - "nulos": Cantidad de valores nulos por columna.
    '''

    dict = {"nombre_campo": [], "tipo_datos": [], "no_nulos_%": [], "nulos_%": [], "nulos": []}

    for column in df.columns:
        porcentaje_no_nulos = (df[column].count() / len(df)) * 100
        dict["nombre_campo"].append(column)
        dict["tipo_datos"].append(df[column].apply(type).unique())
        dict["no_nulos_%"].append(round(porcentaje_no_nulos, 2))
        dict["nulos_%"].append(round(100-porcentaje_no_nulos, 2))
        dict["nulos"].append(df[column].isnull().sum())

    info = pd.DataFrame(dict)
        
    return info


def porcentaje_faltante(df):
    """
    Esta función calcula el porcentaje de valores faltantes para cada 
    columna en un DataFrame.

    Parámetros:
    - df (pandas.DataFrame): El DataFrame de entrada.

    Resultado:
    - info_faltantes (pandas.DataFrame): 
        Un nuevo DataFrame que contiene dos columnas: "Columna" y 
        "Porcentaje Faltante". La columna "Columna" contiene los nombres de 
        las columnas del DataFrame original, y la columna "Porcentaje Faltante" 
        contiene el porcentaje de valores faltantes redondeado a dos decimales 
        para cada columna.
    """

    porcentaje_faltantes = (df.isna().mean() * 100).round(2)
    info_faltantes = pd.DataFrame({"Columna": df.columns, "Porcentaje Faltante": porcentaje_faltantes})

    return info_faltantes


def analisis_sentimiento(review):
    '''
    Realiza un análisis de sentimiento sobre un texto  y 
    devuelve un valor numérico que representa el sentimiento.

    Esta función utiliza la librería TextBlob para analizar el sentimiento sobre texto dado y
    asigna un valor numérico de acuerdo a la polaridad del sentimiento.

    Parameters:
        review (str): El texto que se va a analizar para determinar su sentimiento.

    Returns:
        int: Un valor numérico que representa el sentimiento del texto:
             - 0 para sentimiento negativo.
             - 1 para sentimiento neutral o no clasificable.
             - 2 para sentimiento positivo.
    '''
    if review is None:
        return 1
    analisis= TB(review)
    polaridad = analisis.sentiment.polarity
    if polaridad < -0.2:
        return 0  
    elif polaridad > 0.2: 
        return 2 
    else:
        return 1 
    
def review_por_sentimiento(reviews, sentiments):
    '''
    Imprime ejemplos de reviews para cada categoría de análisis de sentimiento.

    Esta función recibe dos listas paralelas, `reviews` que contiene los textos de las reviews
    y "sentiments" que contiene los valores de sentimiento correspondientes a cada review.
    
    Parameters:
        reviews (list): Una lista de strings que representan los textos de las reviews.
        sentiments (list): Una lista de enteros que representan los valores de sentimiento
                          asociados a cada review (0, 1, o 2).

    Returns:
        None: La función imprime los ejemplos de reviews para cada categoría de sentimiento.
    '''
    for sentiment_value in range(3):
        print(f"Para la categoría de análisis de sentimiento {sentiment_value} se tienen estos ejemplos de reviews:")
        sentiment_reviews = [review for review, sentiment in zip(reviews, sentiments) if sentiment == sentiment_value]
        
        for i, review in enumerate(sentiment_reviews[:3], start=1):
            print(f"Review {i}: {review}")
        
        print("\n")

def duplicados(df, columna):
    '''
    Verifica y muestra filas duplicadas en un DataFrame basado en una columna específica.

    Esta función toma como entrada un DataFrame y el nombre de una columna específica.
    Luego, identifica las filas duplicadas basadas en el contenido de la columna especificada,
    las filtra y las ordena para una comparación más sencilla.

    Parameters:
        df (pandas.DataFrame): El DataFrame en el que se buscarán filas duplicadas.
        columna (str): El nombre de la columna basada en la cual se verificarán las duplicaciones.

    Returns:
        pandas.DataFrame or str: Un DataFrame que contiene las filas duplicadas filtradas y ordenadas,
        listas para su inspección y comparación, o el mensaje "No hay duplicados" si no se encuentran duplicados.
    '''

    duplicated_rows = df[df.duplicated(subset=columna, keep=False)]
    if duplicated_rows.empty:
        return "No hay duplicados"
    
    duplicated_rows_sorted = duplicated_rows.sort_values(by=columna)
    return duplicated_rows_sorted

def separar_año(date):
    '''
    Extrae el año de una fecha en formato 'yyyy-mm-dd' y maneja valores nulos.

    Esta función toma como entrada una fecha en formato 'yyyy-mm-dd' y devuelve el año de la fecha si
    el dato es válido. Si la fecha es nula o inconsistente, devuelve 'Dato no disponible'.

    Parameters:
        fecha (str or float or None): La fecha en formato 'yyyy-mm-dd'.

    Returns:
        str: El año de la fecha si es válido, 'Dato no disponible' si es nula o el formato es incorrecto.
    '''
    if pd.notna(date):
        if re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            return date.split("-")[0]
    return "Dato no disponible"
    
def reemplazar_flotante(value):
    '''
    Reemplaza valores no numéricos y nulos en una columna con 0.0.

    Esta función toma un valor como entrada y trata de convertirlo a un número float.
    Si la conversión es exitosa, el valor numérico se mantiene. Si la conversión falla o
    el valor es nulo, se devuelve 0.0 en su lugar.

    Parameters:
        value: El valor que se va a intentar convertir a un número float o nulo.

    Returns:
        float: El valor numérico si la conversión es exitosa o nulo, o 0.0 si la conversión falla.
    '''
    if pd.isna(value):
        return 0.0
    try:
        float_value = float(value)
        return float_value
    except:
        return 0.0
    
def transformar_fecha(fecha:str):  
    '''
    Convierte una cadena de fecha en un formato específico a otro formato de fecha.
    
    Args:
        cadena_fecha (str): Cadena de fecha en el formato "Month Day, Year" 
        (por ejemplo, "September 1, 2023").
    
    Returns:
        str: Cadena de fecha en el formato "YYYY-MM-DD" o un mensaje de error 
        si la cadena no cumple el formato esperado.
    '''
    match = re.search(r"(\w+\s\d{1,2},\s\d{4})", fecha)
    if match:
        fecha_str = match.group(1)
        try:
            fecha_dt = pd.to_datetime(fecha_str)
            return fecha_dt.strftime("%Y-%m-%d")
        except:
            return "Fecha inválida"
    else:
        return "Formato inválido"

def resumen_porcentaje(df, columna):
    '''
    Cuenta la cantidad de True/False luego calcula el porcentaje.

    Parameters:
        - df (DataFrame): El DataFrame que contiene los datos.
        - columna (str): El nombre de la columna en el DataFrame 
         para la cual se desea generar el resumen.

    Returns:
        DataFrame: Un DataFrame que resume la cantidad y 
        el porcentaje de True/False en la columna especificada.
    '''
    
    counts = df[columna].value_counts()
    percentages = round(100 * counts / len(df),2)
    df_results = pd.DataFrame({
        "Cantidad": counts,
        "Porcentaje": percentages
    })
    return df_results

def bigote_max(columna):
    '''
    Calcula el valor del bigote superior y la cantidad de valores atípicos 
    en una columna.

    Parameters:
        - columna (pandas.Series): La columna de datos para la cual 
        se desea calcular el bigote superior y encontrar valores atípicos.

    Returns:
        None
    '''
    # Cuartiles
    q1 = columna.describe()[4]
    q3 = columna.describe()[6]

    # Valor del vigote
    bigote_max = round(q3 + 1.5*(q3 - q1), 2)
    print(f"El bigote superior de la variable {columna.name} se ubica en:", bigote_max)

    # Cantidad de atípicos
    print(f"Hay {(columna > bigote_max).sum()} valores atípicos en la variable {columna.name}")