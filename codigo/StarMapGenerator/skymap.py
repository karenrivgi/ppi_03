# IMPORTAMOS LAS LIBRERÍAS A USAR
# librerías para el manejo de la ubicacion y hora
from datetime import datetime
from geopy import Nominatim
from tzwhere import tzwhere
from pytz import timezone, utc
import numpy as np
import pandas as pd
import os
import math

# Matplotlib para mostrar nuestro mapa del cielo
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle

# Librería SkyField para datos estelares y proyecciones
from skyfield.api import Star, load, wgs84
from skyfield.data import hipparcos, stellarium
from skyfield.projections import build_stereographic_projection
from skyfield.api import Loader

from geopy.exc import GeocoderUnavailable
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderServiceError
from tkinter import messagebox

def generar_mapa(
        fecha_hora,
        lugar,
        size: int,
        magnitud_lim=8,
        nombres_estrellas=True,
        planeta='mars',
        cons_color='y',
        cultura='maya'):
    
    """
    Genera un gráfico del mapa estelar basado en una fecha y ubicación y demás parámetros pasados 
    por el usuario.
        
    Se apoya en librerías como geopy y datetime para hacer el tratamiento de los parámetros, luego
    con la librería skyfield y sus datos obtiene lo necesario para realizar el gráfico con matplotlib
    y las personalizaciones especificadas."""

    load = Loader(os.path.dirname(__file__))
    warning = False # Avertencia en caso de que el planeta no se pueda visualizar
    geopy_problem = False # Para manejo de datos en caso de fallo en servidores geopy

    # -------------------------
    # CARGAR DATOS

    # de421 (de SkyField) Muestra la posición de la tierra y el sol en el
    # espacio
    eph = load('de421.bsp')

    # El catálogo de estrellas Hiparco del data de skifield contiene
    # información las estrellas
    with load.open(hipparcos.URL) as f:
        # Lo cargamos como un dataframe
        stars = hipparcos.load_dataframe(f)

    # -------------------------
    # PROCESAR UBICACIÓN Y FECHA

    # Obtenemos la ubicación del usuario solicitando la infor en el formato:
    # país, provincia y ciudad
    locationstr = lugar  # 'Colombia, Antioquia, Medellin'

    # Obtenemos la hora en el formato: año-mes-dia hora
    when = fecha_hora  # '2023-01-01 00:00'

    # Hacemos uso de geopy para obtener de la ubicación su latitud y longitud
    try:
        locator = Nominatim(user_agent='my_request')
        location = locator.geocode(locationstr)
        lat, long = location.latitude, location.longitude
    
    except GeocoderUnavailable:
        # Manejar la excepción de GeocoderUnavailable
        if locationstr != 'Colombia, Antioquia, Medellin':
            messagebox.showinfo("GeocoderUnavailable", "The servers that help us to position your location are not working at the moment, but we can show you the map in our default location: Colombia, Antioquia, Medellin.")
        lat, long =  6.2443382, -75.573553
        geopy_problem = True
    
    except:
        raise
    

    # Convertimos el string dado por el usuario en un objeto tipo datetime
    dt = datetime.strptime(when, '%Y-%m-%d %H:%M')

    # Obtener la zona horaria correspondiente a las coordenadas
    timezone_str = tzwhere.tzwhere().tzNameAt(lat, long)
    local = timezone(timezone_str)

    # Convertir la fecha y hora local a UTC (hora estándar que es igual en
    # todo el mundo)
    local_dt = local.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(utc)

    # Convertir la fecha y hora UTC a un objeto "Time" para realizar cálculos
    # astronómicos.
    ts = load.timescale()
    t = ts.from_datetime(utc_dt)

    # -------------------------
    # CREACIÓN DE LA PROYECCIÓN DE LA ESFERA CELESTE EN UN PLANO

    # Encontramos la ubicación de la tierra de de421.bsp
    earth = eph['earth']

    # Crea un objeto "observador" en una ubicación geográfica específica y en
    # un momento determinado.
    observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=long).at(t)

    # Centramos el punto de observación en la mitad del cielo, justo arriba de la cabeza del observador
    # (cenit), creando una estrella falsa como punto central

    # Convertimos las coordenadas del observador a coordenadas astronómicas
    ra, dec, distance = observer.radec()
    # Creamos la estrella falsa (punto en el cielo y centro de la gráfica) con
    # las coordenadas anteriores
    center_object = Star(ra=ra, dec=dec)

    # Encontramos el centro relativo a la tierra en la fecha pasada y
    # construimos la proyección estereográfica del cielo con ayuda de skyfield

    # La tierra el (fecha), observa (punto falso (cenit del observador))
    center = earth.at(t).observe(center_object)
    # Construye la proyección estereográfica centrada en el cenit del
    # observador.
    projection = build_stereographic_projection(center)

    # -------------------------
    # POSICIONAMIENTO DE LAS ESTRELLAS EN LA PROYECCIÓN

    # Observamos las estrellas desde la tierra y guardamos sus posiciones, luego las proyectamos en nuestra
    # gráfica en el plano 2D, y guardamos sus nuevas coordenadas en términos
    # de x y y

    # Observamos las estrellas desde la posición en la tierra en el tiempo
    # especificado (t)
    star_positions = earth.at(t).observe(Star.from_dataframe(stars))

    # En base a la proyección estereográfica hecha con centro el cenit del observador,
    # encontramos la posición de la estrella en un plano 2D y guardamos esos
    # datos en el dataframe stars
    stars['x'], stars['y'] = projection(star_positions)

    '''
    Las estrellas tienen magnitudes aparentes variables que definen qué tan brillantes son en comparación con la estrella más brillante de nuestro cielo.
    Cuanto mayor es la magnitud, menos brillante nos parece la estrella, y queremos representar eso en el plano 2D
    '''

    chart_size = int(size * 0.02)  # Tamaño del mapa estelar
    max_star_size = 100  # Tamaño máximo de la estrella (en el gráfico)
    # No mostrará las estrellas que tengan una magnitud mayor: entre menor es
    # su magnitud, más brillante es
    limiting_magnitude = magnitud_lim

    # Creamos una máscara para filtrar por la magnitud límite
    bright_stars = (stars.magnitude <= limiting_magnitude)
    # Obtenemos las estrellas en el catálogo hiparco que cumplen con la
    # condición de magnitud
    magnitude = stars['magnitude'][bright_stars]

    # -------------------------
    # NOMBRAR LAS ESTRELLAS MÁS BRILLANTES MOSTRADAS EN EL MAPA*

    def in_circle(row):
        center_x = 0
        center_y = 0
        radius = 1
        x = row["x"]
        y = row["y"]

        dist = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)
        return dist < radius

    bright_stars_label = (stars.magnitude <= 1.5)
    brightest_for_labels = stars[stars.apply(
        in_circle, 1) & bright_stars_label]

    names_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)),
        "names.csv")
    
    names_csv = pd.read_csv(names_path)

    brightest_and_labels = names_csv[names_csv["HIP"].isin(
        list(brightest_for_labels.index))]
    brightest_for_labels = brightest_for_labels.loc[brightest_and_labels["HIP"]]
        

    # -------------------------
    # CONSTRUIR LAS CONSTELACIONES

    # Obtenemos las constelaciones basadas en una cultura
    constellations = get_constellations(cultura)

    # Hacemos una lista de las estrellas en las que empieza y termina cada
    # arista
    edges = [edge for name, edges in constellations for edge in edges]
    edges_star1 = [star1 for star1, star2 in edges]
    edges_star2 = [star2 for star1, star2 in edges]

    # Las líneas de constelación comenzarán cada una en el x,y de una estrella y terminarán en las
    # x,y de otra. Hacemos la conversión de las coordenadas en la forma en que
    # matplotlib las espera
    xy1 = stars[['x', 'y']].loc[edges_star1].values
    xy2 = stars[['x', 'y']].loc[edges_star2].values
    lines_xy = np.rollaxis(np.array([xy1, xy2]), 1)

    # -------------------------
    # POSICIONAR UN PLANETA EN LA PROYECCIÓN

    # Si queremos observar un planeta, extraemos su posición en la fecha y ubicacion actual
    # Usando la efemerides guardadas en eph

    if planeta:

        planets_b = ['jupiter', 'saturn', 'uranus', 'neptune', 'pluto']
        if planeta in planets_b:
            ef = f"{planeta} barycenter"
            planet = eph[ef]
        else:    
            planet = eph[planeta]

        planet_position = earth.at(t).observe(planet)
        planet_x, planet_y = projection(planet_position)
        
        # Advertirmos al usuario en caso de que no se pueda ver el planeta
        if planet_x < -0.9 or planet_x > 0.9 or planet_y < -0.9 or planet_y > 0.9:
            warning = True

    # ----------------------------------------
    # CONSTRUCCIÓN DEL GRÁFICO

    # Crear una figura con el tamaño especificado
    fig, ax = plt.subplots(
        figsize=(
            chart_size, chart_size), tight_layout={
            'pad': 0})

    # Configurar el color de fondo de la figura
    fig.set_facecolor("black")

    # Crear un círculo para el fondo de la proyección
    # Fondo para la proyección
    border = plt.Circle((0, 0), 1, color='black', fill=True)
    ax.add_patch(border)

    # Calcular el tamaño del marcador que representa el brillo de la estrella
    # Calcula qué tan grande será el circulo
    marker_size = max_star_size * 10 ** (magnitude / -2.5)

    # Dibujar las líneas de la constelación
    ax.add_collection(LineCollection(lines_xy, colors=cons_color))

    # Diagrama de dispersión usando la ubicación x,y de las estrellas
    # y el tamaño del marcador que representa el brillo.
    ax.scatter(stars['x'][bright_stars], stars['y'][bright_stars],
               s=marker_size, color='white', marker='.', linewidths=0,
               zorder=2)

    # Si se especificó el planeta, agregarlo al gráfico
    if planeta and not warning:
        ax.scatter(
            planet_x,
            planet_y,
            color='red',
            s=500,
            marker='.',
            label = planeta.capitalize())
        ax.legend()

    # Si se especificó mostrar los nombres de las estrellas, agregarlos al
    # gráfico y a la variable a retornar

    stars_name_list = None

    if nombres_estrellas:
        # Para cada estrella brillante, agregar el nombre como una etiqueta en
        # la ubicación correspondiente
        for label, x, y in zip(
                brightest_and_labels["common name"], brightest_for_labels["x"], brightest_for_labels["y"]):
            ax.annotate(
                label, xy=(
                    x, y), xytext=(
                    0.5, -0.5), textcoords="offset points", color="white", fontsize=6)
            
        # Actualiza la variable con los nombres de estrellas a visualizar
        stars_name_list = brightest_and_labels["common name"].tolist()
        
    # Configurar el horizonte de la gráfica, no mostrará lo que esté fuera de
    # este horizonte
    horizon = Circle((0, 0), radius=1, transform=ax.transData)
    for col in ax.collections:
        col.set_clip_path(horizon)

    # Configurar los límites de los ejes y desactivar los ejes
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.axis('off')

    # font1 = {'family':'serif','color':'black','size':15}
    # ax.set_title(locationstr + " " + when, fontdict = font1)

    # Retorna la figura creada y demás variables para el posterior manejo
    return fig, warning, geopy_problem, stars_name_list


def get_constellations(culture):
    """ Retorna un objeto que representa las constelaciones de una cultura especifica

    Analiza el archivo.fab de Skyfield correspondiente a la cultura especificada
    como parámetro.
    """

    # Configura la ruta de acceso a la carpeta Constellations
    constelaciones_path = os.path.join(
        os.path.dirname(__file__), "Constellations")

    # Guarda en constelation la ruta al archivo .fab correspondiente a la
    # cultura especificada
    if culture == 'modern':
        constelation = os.path.join(
            constelaciones_path,
            'constellationship_modern.fab')
    elif culture == 'maya':
        constelation = os.path.join(
            constelaciones_path,
            'constellationship_maya.fab')
    elif culture == 'chinese':
        constelation = os.path.join(
            constelaciones_path,
            'constellationship_chinese.fab')
    elif culture == 'egyptian':
        constelation = os.path.join(
            constelaciones_path,
            'constellationship_egyptian.fab')
    else:
        raise ValueError(f"Cultura {culture} no soportada")

    # Abre el archivo y hace la conversión necesaria para manipularlo
    with open(constelation, "rb") as f:
        constellations = stellarium.parse_constellations(f)

    return constellations   
