
import pandas as pd
import datetime
from fastapi import FastAPI
from tabulate import tabulate
from datetime import datetime
import openpyxl

app = FastAPI()

df_work = pd.read_excel('dfwork.xlsx', sheet_name='Sheet1', usecols=['title', 'popularity', 'release_date', 'release_year', 'release_month', 
                  'release_day', 'num_dia', 'vote_average', 'vote_count', 'budget', 'revenue', 'return', 'director', 'elenco'])

# Función: Root
# ********************
@app.get('/') #ruta raíz
def get_root():
    return 'API para consulta de datos de películas'

# Función: PELIS X MES
# ********************
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    """
    
    """
    # Crear diccionario con los nombres de los meses y su valor numérico
    # Mapea la cadena ingresada y si pertenece, la convierte a su valor numérico
    dic_map_meses = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}
    
    # Para controlar las cadenas ingresadas, primero se convierten a minúsculas
    # luego, se obtiene su valor numérico
    mes      = mes.lower()
    v_numMes = dic_map_meses.get(mes)

    # Valida el ingreso de cadenas inválidas 
    if v_numMes is None:
        raise ValueError('Mes ingresado es inválido.')

    # Realizar la consulta en el DataFrame
    query       = df_work['release_month'] == v_numMes
    v_num_pelis = len(df_work[query])

    # Imprime el resultado de la consulta
    return {'Mes consultado': mes, 'Estrenos totales': v_num_pelis}

# Función: PELIS X DÍA
# ********************
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
  
    """
    
    """
    # Diccionario semana
    dic_semana={'lunes':1,'martes':2,'miércoles':3,'jueves':4,'viernes':5,'sábado':6,'domingo':7}
    
    # Valida 'v_Dia' y convertir cadena a minúscula
    v_Dia = dia.lower()

    #while v_Dia not in dic_semana:
    #    v_Dia = input("Ingrese un día de la semana válido: ").lower()

    # Guarda valor temporal
    v_tmp_num = dic_semana[v_Dia]

    # Contar películas por día de la semana
    #v_suma_pelis = df_work[df_work['num_dia'] == v_tmp_num]['num_dia'].count()

    # Valida el ingreso de cadenas inválidas 
    if v_tmp_num is None:
        raise ValueError('Día ingresado es inválido.')

    # Realizar la consulta en el DataFrame
    query       = df_work['num_dia'] == v_tmp_num
    v_num_pelis = len(df_work[query])
  
    # Retorna cantidad de películas
    return {'Un día': v_Dia, 'se estrenaron': v_suma_pelis}
   
  
# Función: SCORE PELI
# *******************
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    """

    """
    # Convertir la cadena a tipo título
    v_nom_pel = titulo.title()
    query = df_work['title'] == v_nom_pel
    movie = df_work.loc[query, ['title', 'release_year', 'popularity']].head(1)
    if not movie.empty:
        titulo       = movie['title'].iloc[0]
        anio_estreno = movie['release_year'].iloc[0]
        score        = movie['popularity'].iloc[0]
        return {'La película': v_nom_pel, 'fue estrenada': anio_estreno, 'con una popularidad de': score}
    else:
        return {"No se encontró la película": v_nom_pel}


# Función: VOTOS X PELI
# *********************
@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    """ 
    Se ingresa el título de una filmación esperando como respuesta el título, 
    la cantidad de votos y el valor promedio de las votaciones. 
    
    La misma variable deberá de contar con al menos 2000 valoraciones, caso 
    contrario, debemos contar con un mensaje avisando que no cumple esta condición, 
    ergo, no se devuelve ningun valor.
    """
    # Convertir el título a minúsculas
    v_titulo = titulo.title()
    query = df_work['title'] == v_titulo
    movie = df_work.loc[query, ['title', 'release_year', 'vote_count', 'vote_average']].head(1)
    if not movie.empty:
        v_titulo       = movie['title'].iloc[0]
        v_med_votos    = movie['vote_average'].iloc[0]
        v_qtty_votos   = movie['vote_count'].iloc[0]
        v_anio_estreno = movie['release_year'].iloc[0]
        if v_qtty_votos < 2000:
            return {"Puntaje insuficiente!!"}
        else:
            return {"La película": v_titulo, "fue estrenada en el año": v_anio_estreno, " sus votos totales son": v_qtty_votos,
                    "con un promedio de": v_med_votos}
    else:
        return {"No se encontró la película": v_titulo}
