
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
def get_director(nombre_director:str):
    """  
    
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

    # Convertir a formato str, para evitar error en el webservice
    #formato = json.dumps(formato, ensure_ascii=False, indent=4)

    return formato


# Función: MOTOR RECOMENDADOR PELIS
# *********************************
@app.get("/recomendacion/{nombre_pelicula}")                               
def recomendacion(nombre_pelicula:str):
    """  
    Función que genera una recomendación basada en la coincidencia
    con los géneros y la popularidad.

    Se ingresa un título, se identifican los géneros en que fue clasificada,
    luego ordena la películas que tengan las mismas clasificaciones y genera
    una lista que se vuelve a ordenar por popularidad.

    Resulta en una recomendación basada en dos factores.

    Se puede ir agregando otros factores, como votación y crítica de cine, 
    permitiendo ajustarse a restricciones del lado servidor, en este caso RENDER, 
    que soporta 512MB y un procesamiento limitado.

    Luego de muchas pruebas con sklearn y cosine_similarity, que desbordaban las
    capacidades dadas como restricción, reduje la carga y la velocidad de respuesta.
    
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
    # Verifica si la película existe en nuestra BBDD ('title')
    if nombre_pelicula not in df_work['title'].values:
        print('La película está mal escrita o no está en la BBDD.')
        return None

    # Obtener el registro coincidente
    movie_row = df[df['title'] == nombre_pelicula].iloc[0]

    # Extraer los valores necesarios del registro
    # Aqui se pueden agregar más factores, incluso ponderadores
    # y generar un modelo mucho más complejo, hoy es MVP
    
    title      = movie_row['title']
    generos    = movie_row['generos']
    popularity = movie_row['popularity']

    # Crea variables temporales para cada elemento en la lista 'generos'
    generos_list         = generos.split(', ')
    n                    = len(generos_list)
    variables_temporales = ['x{}'.format(i) for i in range(1, n + 1)]
    # Crea tantas variables como elementos hay en el campo 'generos'
    for i in range(n):
        exec("{} = '{}'".format(variables_temporales[i], generos_list[i]))

    # Filtra películas con coincidencias en los géneros y luego, las ordena por su popularidad
    filtered_movies = df[df['generos'].apply(lambda x: all(g in x for g in generos_list))].sort_values(by='popularity', ascending=False)

    # Elimina la película de entrada de las recomendaciones
    filtered_movies = filtered_movies[filtered_movies['title'] != nombre_pelicula]

    # Filtra las primeras 5 películas recomendadas
    recommended_movies = filtered_movies.head(5)

    # Crea una lista con las películas recomendadas
    tu_lista = []
    for i, row in recommended_movies.iterrows():
        tu_lista.append("{}. {} y su popularidad es {}".format(i+1, row['title'], row['popularity']))

    # Mostrar las películas recomendadas como una lista apilada
    print("Las películas recomendadas son:")
    for peli in tu_lista:
        print(peli)



