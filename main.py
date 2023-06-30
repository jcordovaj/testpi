
import pandas as pd
import datetime
from fastapi import FastAPI
from tabulate import tabulate
from datetime import datetime
import openpyxl

app = FastAPI()

df_work = pd.read_excel('dfwork.xlsx', sheet_name='Sheet1', usecols=['id', 'title', 'popularity', 'release_year', 'release_month', 
                  'release_day', 'release_weekday', 'vote_average', 'vote_count', 'budget', 'revenue', 'return', 'director', 'elenco', 'generos'])

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
    Recibe: una cadena de texto con el nombre del mes
    en idioma español.
    
    No valida el idioma, sólo que pertenezca al 
    diccionario.
    
    Si la cadena es inválida, solicitará
    otra cadena válida.
    
    Retorna: La cantidad de películas estrenadas en el mes 'X'
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
    Recibe : Una cadena de texto con el nombre de un día.
    
    Retorna: La suma de películas estrenadas en ese mismo día.
    
    Ejemplo: cantidad_filmaciones_dia/lunes 
             "XXXX películas fueron estrenadas un lunes".
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
    query       = df_work['release_weekday'] == v_tmp_num
    v_num_pelis = len(df_work[query])
  
    # Retorna cantidad de películas
    return {'Un día': v_Dia, 'se estrenaron': v_num_pelis}
   
  
# Función: SCORE PELI
# *******************
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    """
    Función de consulta que recibe e nombre de una película
    y muestra su score de popularidad.

    Recibe: Una cadena de texto 'titulo'. Si la cadena no
    no se encuentra o está mal escrita, genera un mensaje
    de advertencia ('No se encontró la película').

    Retorna: Una frase, con el título de la peli, año de estreno,
    y su popularidad.
    
    "La película': titulo, 'fue estrenada': str(anio_estreno), 'con una popularidad de': str(score)
    """    
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

    Recibe  : Una cadena de texto, valida si está en la BBDD.

    Retorna : Si la película tiene más de 2000 votos, su título, año de estreno, votos, y promedio
    de votos. Si tiene menos de 2000 votos, un mensaje "Puntaje insuficiente!!"
    
    """
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
                v_contador    += 1
                v_revenue      = df_work.loc[df_work['elenco'] == v_elenco, 'revenue'].values[0]
                v_sum_revenue += v_revenue
        except AttributeError:
            pass
    
    # Formateo de los valores
    v_contador_format    = '{:,}'.format(v_contador)
    v_sum_revenue_format = '${:,.2f}'.format(v_sum_revenue)
    v_prom_revenue       = '${:,.2f}'.format(v_sum_revenue / v_contador)
    
    # Retorna resultado
    return {'El actor': nombre_actor, 'N° de pelis en que ha participado': str(v_contador_format), 'Con un retorno total de': str(v_sum_revenue_format),
            'Su retorno promedio es': str(v_prom_revenue)}


# Función: EXITO X DIRECTOR
# *************************
@app.get("/get_director/{nombre_director}")                               
def get_director(nombre_director:str):
    """  
    Función de consulta.
    
    Recibe  : Cadena de texto que el nombre de un director de cine.
    
    No valida grafía, si la cadena coincide, realiza la búsqueda.
    
    Retorna : Nombre del director, las películas dirigidas, luego
    genera una lista con el nombre de cada película, año de lanzamiento,
    presupuesto, ingresos y utilidad.
    """
    # Filtra filas que coinciden con la cadena ingresada
    # Crea un subconjunto del df, sólo con las cols de la consulta.
    tmp_data = df_work[df_work['director'] == nombre_director]

    # Calcular el retorno acumulado
    retorno_acumulado = tmp_data['revenue'].sum()

    # Crear la lista de películas para el Director ingresado
    peliculas = []
    for index, row in tmp_data.iterrows():
        titulo  = row['title']
        estreno = row['release_year']
        retorno = row['revenue']
        budget  = row['budget']
        profit  = row['revenue'] - row['budget']

        # Crear el diccionario para cada película
        pelicula = {
            'Titulo' : titulo,
            'Estreno': str(estreno),
            'Retorno': str(retorno),
            'Budget' : str(budget),
            'Profit' : str(profit)
        }
        peliculas.append(pelicula)

    # Estructurar diccionario de salida 
    formato = {
        'Director'          : nombre_director,
        'Total revenue'     : str(retorno_acumulado),
        'Lista de películas': peliculas
    }

    return formato


# Función: MOTOR RECOMENDADOR PELIS SRP
# *************************************
@app.get("/recomendacion/{nombre_pelicula}")                               
def recomendacion(nombre_pelicula:str):
    """  
    Función que genera una recomendación basada en la coincidencia 
    con los géneros y la popularidad.

    Se ingresa un título, se identifican los géneros en que fue clasificada,
    luego busca y ordena la películas que tengan las mismas clasificaciones, 
    supone que son parecidas y genera una lista que se reclasifica por 
    popularidad.

    Resulta en una recomendación basada en dos factores.

    Se puede ir agregando otros factores, como votación y crítica de cine, 
    permitiendo ajustarse a restricciones del lado servidor, en este caso RENDER, 
    que soporta 512MB y un procesamiento limitado, lo que generaba problemas por
    el tamaño de la base y luego, con el procesamiento de los algoritmos de ML.

    Luego de muchas pruebas con sklearn y cosine_similarity, que desbordaban las
    capacidades dadas como restricción, reduje la carga y la velocidad de respuesta,
    proveyendo una solución funcional y performante.
    
    Recibe: Una cadena de texto, si no halla un nombre coincidente retorna un mensaje
    'La película está mal escrita o no está en la BBDD.'
    
    Retorna: Una lista con: el n° de id en la BBDD, el nombre y la popularidad
    
    Ejemplo:
    Las películas recomendadas son:
    26526. Guardians of the Galaxy Vol. 2 y su popularidad es 185.330992
    26525. Thor: Ragnarok y su popularidad es 57.283628
    23717. Guardians of the Galaxy y su popularidad es 53.291601
    38778. Now You See Me 2 y su popularidad es 39.540653
    25494. Kingsman: The Secret Service y su popularidad es 28.224212
        
    """
    # Verificar si la película está en la columna 'title'
    if nombre_pelicula not in df_work['title'].values:
        srp = 'La película no está en el dataframe.'
        return srp

    # Obtener registro coincidente
    movie_row = df_work[df_work['title'] == nombre_pelicula].iloc[0]

    # Extraer que nos sirven del registro
    id         = movie_row['id']
    title      = movie_row['title']
    generos    = movie_row['generos']
    popularity = movie_row['popularity']

    # Crear variables temporales por cada elemento dentro de la variable 'generos'
    # Crea una variable por cada genero en la lista
    # Luego busca pelis con los mismos generos y los ordena por coincidencias, donde
    # 3 coincidencias es mayor que dos coincidencias y 2 es mayor que 1 coincidencia

    generos_list         = generos.split(', ')
    n                    = len(generos_list)
    
    variables_temporales = ['x{}'.format(i) for i in range(1, n + 1)]
    for i in range(n):
        exec("{} = '{}'".format(variables_temporales[i], generos_list[i]))

    # Filtra películas con coincidencias en los géneros y luego las reclasifica por popularidad
    matriz_resultados = df_work[df_work['generos'].apply(lambda x: all(g in x for g in generos_list))].sort_values(by='popularity', ascending=False)

    # Elimina la película ingresada como variable de la lista de recomendaciones
    matriz_resultados = matriz_resultados[matriz_resultados['title'] != nombre_pelicula]

    # Obtiene las primeras 5 películas recomendadas
    pelis_recomendadas = matriz_resultados.head(5)

    # Crear lista con pelis recomendadas
    srp  = ""
    lst_srp = []
    for i, row in pelis_recomendadas.iterrows():
        id_pel      = row['id']
        titulo      = row['title']
        popularidad = row['popularity']
        
        # Crear el diccionario para cada película
        pelis = {
            'Id'          : str(id_pel),
            'Titulo'      : (titulo),
            'Popularidad' : str(popularidad)
                }
    lst_srp.append(pelis)
        
    # Arma diccionario con la salida 
    srp = {
    "Las películas recomendadas son:" : (""),
    " "                               : (lst_srp)
          }
    
    return srp 



