
import pandas as pd
import datetime
from fastapi import FastAPI
from tabulate import tabulate
from datetime import datetime
import openpyxl

app = FastAPI()

df_work = pd.read_excel('dfwork.xlsx', sheet_name='Sheet1', usecols=['title', 'popularity', 'release_date', 'release_year', 'release_month', 
                  'release_day', 'num_dia', 'vote_average', 'vote_count', 'budget', 'revenue', 'return', 'director', 'elenco'])

# Función: PELIS X MES
# ********************
@app.get('/') #ruta raíz
def get_root():
    return 'API para consulta de datos de películas'

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):                            
   
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
    #return {'mes': mes, 'cantidad': cant} 


