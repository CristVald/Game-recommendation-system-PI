# Importaciones
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import functions_api as fa
from fastapi import HTTPException

import importlib
importlib.reload(fa)

# Se instancia la aplicación
app = FastAPI()

# Funciones
@app.get(path = '/developer',
          description = """ <font color="blue">
                        1. Haz clik en "Try it out".<br>
                        2. Ingresa el nombre del desarrollador. <br>
                        3. Ve a la parte de respuestas para ver la cantidad de items y porcentaje de contenido gratuito por año de ese desarrollador.
                        </font>
                        """,
         tags=["Consultas Generales"])
def developer(desarrollador: str = Query(..., 
                            description="Desarrollador del videojuego", 
                            example='Valve')):
    return fa.developer(desarrollador)


@app.get(path = '/userdata',
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haz clik en "Try it out".<br>
                        2. Ingrese el user_id.<br>
                        3. Ve a la parte de respuestas para ver la cantidad de dinero gastado por el usuario, el porcentaje de recomendación que realiza y cantidad de items que tiene el mismo.
                        </font>
                        """,
         tags=["Consultas Generales"])
def userdata(user_id: str = Query(..., 
                                description="Identificador único del usuario", 
                                example="EchoXSilence")):
        
    return fa.userdata(user_id)
    
    
@app.get(path = '/userforgenre',
          description = """ <font color="blue">
                        1. Haz clik en "Try it out".<br>
                        2. Ingresa el género.<br>
                        3. Ve a la parte de respuestas para ver al usuario que más horas ha jugado dicho genero y una lista de la cantidad de horas por año.
                        </font>
                        """,
         tags=["Consultas Generales"])
def userforgenre(genero: str = Query(..., 
                            description="Género del videojuego", 
                            example='Simulation')):
    return fa.userforgenre(genero)


@app.get(path = '/best_developer_year',
          description = """ <font color="blue">
                        1. Haz clik en "Try it out".<br>
                        2. Ingresa el año.<br>
                        3. Ve a la parte de respuestas para ver a la mejor desarrolladora por año, basado en recomendaciónes positivas.
                        </font>
                        """,
         tags=["Consultas Generales"])
def best_developer_year(anio: int = Query(..., 
                            description="Mejor desarrolladora del año", 
                            example= 2012)):
    return fa.best_developer_year(anio)



@app.get(path = '/developer_reviews_analysis',
          description = """ <font color="blue">
                        1. Haz clik en "Try it out".<br>
                        2. Ingresa la empresa desarrolladora.<br>
                        3. Ve a la parte de respuestas para ver un diccionario con el nombre del desarrollador y la cantidad de opiniones positivas o negativas obtenidas por la misma.
                        </font>
                        """,
         tags=["Consultas Generales"])
def developer_reviews_analysis(desarrolladora: str = Query(..., 
                            description="Cantidad de opiniones positivas o negativas", 
                            example= "Smartly Dressed Games")):
    return fa.developer_reviews_analysis(desarrolladora)





@app.get('/recomendacion_juego',
         description=""" <font color="blue">
                    INSTRUCCIONES<br>
                    1. Haz clik en "Try it out".<br>
                    2. Ingresa el nombre de un juego.<br>
                    3. Ve a la parte de respuestas para ver los juegos recomendados.
                    </font>
                    """,
         tags=["Recomendación"])
def recomendacion_juego(game: str = Query(..., 
                                         description="Juego a partir del cuál se hace la recomendación de otros juego", 
                                         example="Killing Floor")):
    return fa.recomendacion_juego(game)




@app.get('/recomendacion_usuario',
         description=""" <font color="blue">
                    INSTRUCCIONES<br>
                    1. Haz clik en "Try it out".<br>
                    2. Ingresa el id del usuario.<br>
                    3. Ve a la parte de respuestas para ver los juegos recomendados para ese usuario.
                    </font>
                    """,
         tags=["Recomendación"])


def recomendacion_usuario(user: str = Query(..., 
                                         description="Usuario a partir del cuál se hace la recomendación de los juego", 
                                         example="barkboy")):
    return fa.recomendacion_usuario(user) 
