# IMPORTAMOS LAS LIBRERÍAS A USAR

# librerías para el manejo de la ubicacion y hora
from datetime import datetime
from geopy import Nominatim
from tzwhere import tzwhere
from pytz import timezone, utc
import numpy as np
import pandas as pd

# Matplotlib para mostrar nuestro mapa del cielo
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle

# Librería SkyField para datos estelares y proyecciones
from skyfield.api import Star, load, wgs84
from skyfield.data import hipparcos, stellarium
from skyfield.projections import build_stereographic_projection

def generar_mapa(fecha_hora, lugar):

    # de421 (de SkyField) Muestra la posición de la tierra y el sol en el espacio
    eph = load('de421.bsp')

    # El catálogo de estrellas Hiparco del data de skifield contiene información sobre la ubicación y demás características de las estrellas
    # Lo cargamos como un dataframe

    with load.open(hipparcos.URL) as f:
        stars = hipparcos.load_dataframe(f)

    # Obtenemos la ubicación del usuario solicitando la infor en el formato: país, departamento o provincia y ciudad
    locationstr =  lugar #'Colombia, Antioquia, Medellin'

    # Obtenemos la hora en el formato: año-mes-dia hora
    when =  fecha_hora #'2023-01-01 00:00'

    # Hacemos uso de geopy para obtener de la ubicación su latitud y longitud
    locator = Nominatim(user_agent='my_request') 
    location = locator.geocode(locationstr)
    lat, long = 6.2540146, -75.23649364737614

    # Convertimos el string dado por el usuario en un objeto tipo datetime
    dt = datetime.strptime(when, '%Y-%m-%d %H:%M')

    # define datetime and convert to utc based on our timezone ***
    timezone_str = tzwhere.tzwhere().tzNameAt(lat, long)
    local = timezone(timezone_str)

    # get UTC from local timezone and datetime ***
    local_dt = local.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(utc)

    # Encontramos la ubicación de la tierra de de421.bsp find location of earth and sun and set the observer position
    earth = eph['earth']

    # Definimos el tiempo de observación del datetime UTC 
    ts = load.timescale()
    t = ts.from_datetime(utc_dt)

    # Definimos un observador usando los datos del sistema geodésico mundial ("único sistema de referencia de coordenadas geográficas mundial utilizado hoy en día y que permite localizar cualquier punto de la Tierra" - https://www.aragon.es/documents/20127/2555757/Busqueda+de+COORDENADAS+GEOGRAFICAS+%282%29.pdf/547291f2-8704-2aa4-1a76-c6c4bfb60d0e?t=1624276052810#:~:text=El%20datum%20WGS84%20es%20el,en%20los%20dispositivos%20GPS%20comerciales.)
    observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=long).at(t)

    # Definimos la posición en el espacio a la que miraremos (Cenit del observaor) define the position in the sky where we will be looking
    #position = observer.from_altaz(alt_degrees=90, az_degrees=0)

    # Centramos el punto de observación en la mitad del cielo, justo arriba de la cabeza del observador (cenit), creando una estrella falsa como punto central

    ra, dec, distance = observer.radec() # Convertimos las coordenadas del observador a coordenadas astronómicas
    center_object = Star(ra=ra, dec=dec) # Creamos la estrella falsa (punto en el cielo y centro de la gráfica) con las coordenadas anteriores

    # Encontramos el centro relativo a la tierra en la fecha pasada y construimos la proyección estereográfica del cielo con ayuda de skyfield 

    center = earth.at(t).observe(center_object) # La tierra el (fecha), observa (punto falso (cenit del observador))
    projection = build_stereographic_projection(center)
    field_of_view_degrees = 180.0

    # Observamos las estrellas desde la posición en la tierra y las proyectamos en el mapa, permitiendo calcular sus posiciones
    # en tèrminos de x y y* (nuevas columnas del dataframe) al proyectarlas en un plano 2D

    star_positions = earth.at(t).observe(Star.from_dataframe(stars)) # Observamos las estrellas desde la posición en la tierra en el tiempo especificado (t)
    stars['x'], stars['y'] = projection(star_positions) # En base a la proyección estereográfica hecha con centro el cenit del observador, 
                                                        # encontramos la posición de la estrella en un plano 2D y guardamos esos datos en el dataframe stars

    #Las estrellas tienen magnitudes aparentes variables que definen qué tan brillantes son en comparación con la estrella más brillante de nuestro cielo. 
    #Cuanto mayor es la magnitud, menos brillante nos parece la estrella, y queremos representar eso en el plano 2D
    
    chart_size = 10 # Tamaño del mapa estelar
    max_star_size = 100 # Tamaño máximo de la estrella (en el gráfico)
    limiting_magnitude = 8 # No mostrará las estrellas que tengan magnitud mayor que 10: entre menor es su magnitud, más brillante es

    bright_stars = (stars.magnitude <= limiting_magnitude) # Creamos una máscara para filtrar por la magnitud límite

    magnitude = stars['magnitude'][bright_stars] # Obtenemos las estrellas en el catálogo hiparco que cumplen con la condición de magnitud

    
    # Obtenemos estrellas más brillantes y obtenemos sus nombres
    import math
    def in_circle(row):
        center_x = 0
        center_y = 0
        radius = 1
        x = row["x"]
        y = row["y"]

        dist = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)
        return dist < radius

    bright_stars_label = (stars.magnitude <= 2) 
    oppp = stars.apply(in_circle, 1) & bright_stars_label
    brightest_for_labels = stars[stars.apply(in_circle, 1) & bright_stars_label]

    names_csv = pd.read_csv("names.csv")
    brightest_and_labels = names_csv[names_csv["HIP"].isin(list(brightest_for_labels.index))]
    brightest_for_labels = brightest_for_labels.loc[brightest_and_labels["HIP"]]


    # Los contornos de la constelación provienen de Stellarium. Hacemos una lista
    # de las estrellas en las que cada borde protagoniza y la estrella en la que cada borde
    # termina.

    # Hay que borrar el archivo cada vez, para que cargue el nuevo
    #url = ('https://raw.githubusercontent.com/Stellarium/stellarium/master/skycultures/maya/constellationship.fab')
    url = ('https://raw.githubusercontent.com/Stellarium/stellarium/master/skycultures/modern/constellationship.fab')

    with load.open(url) as f:
        constellations = stellarium.parse_constellations(f)

    edges = [edge for name, edges in constellations for edge in edges]
    edges_star1 = [star1 for star1, star2 in edges]
    edges_star2 = [star2 for star1, star2 in edges]

    # Las líneas de constelación comenzarán cada una en la (x, y) de una estrella y un final
    # en la (x, y) de otra. Tenemos que "rollaxis" la coordenada resultante
    # matriz en la forma que Matplotlib espera.

    xy1 = stars[['x', 'y']].loc[edges_star1].values
    xy2 = stars[['x', 'y']].loc[edges_star2].values
    lines_xy = np.rollaxis(np.array([xy1, xy2]), 1)

    fig, ax = plt.subplots(figsize=(chart_size, chart_size)) # Define el tamaño de la gráfica
    
    border = plt.Circle((0, 0), 1, color='black', fill=True) # Fondo para la proyección
    ax.add_patch(border)

    marker_size = max_star_size * 10 ** (magnitude / -2.5) #Calcula qué tan grande será el circulito (En base al cálculo descrito en la img)
    #marker_size = (0.5 + limiting_magnitude - magnitude) ** 2.0

    # Dibujar las lineas de las constelaciones.

    ax.add_collection(LineCollection(lines_xy, colors='y'))

    #Diagrama de dispersión usando su ubicación x e y, el tamaño del marcador que representa el brillo.
    ax.scatter(stars['x'][bright_stars], stars['y'][bright_stars], 
    s=marker_size, color='white', marker='.', linewidths=0, 
    zorder=2)

    # Ponerle la equiqueta a cada estrella de las más brillantes
    for label, x, y in zip(brightest_and_labels["common name"],brightest_for_labels["x"], brightest_for_labels["y"]):
        ax.annotate(label,
        xy=(x, y),                          # Poner la etiqueta en el punto
        xytext=(0.5,-0.5),                  # un poco desfasada
        textcoords = "offset points", color="white",
        fontsize=6)

    horizon = Circle((0, 0), radius=1, transform=ax.transData)
    for col in ax.collections:
        col.set_clip_path(horizon)


    # Otras configuraciones
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.axis('off')

    font1 = {'family':'serif','color':'black','size':15}

    ax.set_title(locationstr + " " + when, fontdict = font1)
    plt.savefig("map.png")

    return fig      