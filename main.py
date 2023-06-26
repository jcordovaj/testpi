
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

    # Estructurar la consulta
    query       = df_work['release_month'] == v_numMes
    v_num_pelis = len(df_work[query])

    # Retorna el resultado de la consulta
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

    # Guarda valor temporal
    v_tmp_num = dic_semana[v_Dia]

    # Valida el ingreso de cadenas inválidas 
    if v_tmp_num is None:
        raise ValueError('Día ingresado es inválido.')

    # Estructurar la consulta
    query       = df_work['num_dia'] == v_tmp_num
    v_num_pelis = len(df_work[query])
  
    # Retorna cantidad de películas
    return {'Un día': v_Dia, 'se estrenaron': v_num_pelis}
   
  
# Función: SCORE PELI
# *******************
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    """

    """
    # Convertir la cadena a tipo título
    #v_nom_pel = titulo.title()
    
    query = df_work['title'] == titulo
    movie = df_work.loc[query, ['title', 'release_year', 'popularity']].head(1)
    
    if not movie.empty:
        titulo       = movie['title'].iloc[0]
        anio_estreno = movie['release_year'].iloc[0]
        score        = movie['popularity'].iloc[0]
        return {'La película': titulo, 'fue estrenada': str(anio_estreno), 'con una popularidad de': str(score)}
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
    
    query = df_work['title'] == titulo
    movie = df_work.loc[query, ['title', 'release_year', 'vote_count', 'vote_average']].head(1)
    if not movie.empty:
        v_titulo       = movie['title'].iloc[0]
        v_prom_votos   = movie['vote_average'].iloc[0]
        v_qtty_votos   = movie['vote_count'].iloc[0]
        v_anio_estreno = movie['release_year'].iloc[0]
        if v_qtty_votos < 2000:
            return {"Puntaje insuficiente!!"}
        else:
            return {"La película": titulo, "fue estrenada en el año": str(v_anio_estreno), " sus votos totales son": str(v_qtty_votos),
                    "con un promedio de": str(v_prom_votos)}
    else:
        return {"No se encontró la película": titulo}


# Función: EXITO X ACTOR
# **********************
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    """
    Función que busca un actor y retorna el número de películas en que
    ha participado, el acumulado de ingresos y su promedio.
    
    Recibe: Una cadena de texto, que es el nombre de un actor.
    
    Retorna: Nombre del actor, número de películas en las que participó,
    el acumulado de ingresos 'revenue' y el promedio ('revenue'/número de películas)
    
    Ejemplo: 'El actor X ha participado de Y cantidad de filmaciones, con 
    un un promedio de Z por filmación'
    """
   
    # Inicializa contador y acumulador
    
    v_contador    = 0
    v_sum_revenue = 0
        
    for v_elenco in df_work['elenco']:
        try:
            if nombre_actor in v_elenco.split(','):
                v_contador += 1
                v_revenue = df_work.loc[df_work['elenco'] == v_elenco, 'revenue'].values[0]
                v_sum_revenue += v_revenue
        except AttributeError:
            pass
    
    # Formateo de los valores
    v_contador_format = '{:,}'.format(v_contador)
    v_sum_revenue_format = '${:,.2f}'.format(v_sum_revenue)
    v_prom_revenue = '${:,.2f}'.format(v_sum_revenue / v_contador)
    
    # Retorna resultado
    return {'El actor': nombre_actor, 'N° de pelis en que ha participado': str(v_contador_format), 'Con un retorno total de': str(v_sum_revenue_format),
            'Su retorno promedio es': str(v_prom_revenue)}


# Función: EXITO X DIRECTOR
# *************************
@app.get("/get_director/{nombre_director}")                               
async def get_director(nombre_director:str):
    """  
       Función de consulta que retorna el número de películas que un director ha dirigido y su éxito, 
       medido como la suma de ingresos (revenue) de las películas, siempre que exista esa información.
 
       La función busca la cadena de texto dentro del campo 'director'.

       Recibe: Una cadena de texto, nombre del director. No valida variantes del nombre, ni su grafía,
       es decir, si encuentra una cadena igual, retornará los valores de la columna 'revenue', fecha 
       de lanzamiento, costos ('budget') y ganancia generada ('revenue' menos 'budget').

       Retorna: La cantidad de producciones, fechas de lanzamiento, costo, ingresos y utilidad.
    """

    # Inicializa varibles 
    #v_nom_dire = nombre_director.title()
    num_title   = 0
    peliculas   = []

    # Recorre el df y busca coincidencias de la cadena en la columna 'director' 
    for i in range(len(df_work)):
        director = df_work.loc[i, 'director']
        if isinstance(director, str) and nombre_director in director.split(','):
            num_title += 1
            title = df_work.loc[i, 'title']
            release_date = df_work.loc[i, 'release_date']
            budget = df_work.loc[i, 'budget']
            revenue = df_work.loc[i, 'revenue']
            utilidad = revenue - budget
            peliculas.append((title, release_date, budget, revenue, utilidad))

  
    #return {'director':v_nom_dire, 'retorno_total_director':respuesta, 
    #'peliculas':respuesta, 'anio':respuesta,, 'retorno_pelicula':respuesta, 
    #'budget_pelicula':respuesta, 'revenue_pelicula':respuesta}
  
    #print(f"El Director {v_nom_dire} ha dirigido {num_title} producciones.")
    #print("La lista de películas, con sus respectivas fechas de lanzamiento, costo, ingresos y utilidad, es la siguiente:")
    lst_nom_cols   = ['Nombre Película', 'Fecha Lanzamiento', 'Costo (USD)', 'Ingresos (USD)', 'Utilidad (USD)']
    lst_formateada = []

    for fila in peliculas:
        fila_formateada = [
            fila[0],
            datetime.strptime(str(fila[1]), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"),
            "${:.2f}".format(fila[2]),
            "${:.2f}".format(fila[3]),
            "${:.2f}".format(fila[4])
        ]
        lst_formateada.append({"El Director": v_nom_dire, "Lista": fila_formateada})

    peliculas = tabulate(lst_formateada, headers=lst_nom_cols, tablefmt="grid")

    return{peliculas}
