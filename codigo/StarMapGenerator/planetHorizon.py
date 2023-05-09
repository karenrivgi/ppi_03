from skyfield.api import wgs84, load
from skyfield.almanac import find_discrete, risings_and_settings
from pytz import timezone

from datetime import datetime, timedelta
from geopy import Nominatim
from tzwhere import tzwhere
from pytz import timezone, utc

from geopy.exc import GeocoderUnavailable
from tkinter import messagebox


def when_above_horizon(place, date, object):
    """
    Función que recibe una ubicación geográfica, una fecha y el nombre de un objeto celeste
    y devuelve una lista de strings con los momentos en que el objeto está arriba del horizonte.

    Args:
        place (str): Nombre de la ubicación geográfica.
        date (str): Fecha en formato 'YYYY-MM-DD'.
        object (str): Nombre del objeto celeste a analizar.

    Returns:
        list: Lista con los momentos en que el objeto está justo arriba del horizonte.
    """

    locationstr = place
    when = date

    # Hacemos uso de geopy para obtener de la ubicación su latitud y longitud
    try:
        locator = Nominatim(user_agent='my_request')
        location = locator.geocode(locationstr)
        lat, long = location.latitude, location.longitude
    except GeocoderUnavailable:
        # Manejar la excepción de GeocoderUnavailable
        if locationstr != 'Colombia, Antioquia, Medellin':
            messagebox.showinfo(
                "GeocoderUnavailable",
                "The servers that help us to position your location are not working at the moment, but we can show you the time in our default location: Colombia, Antioquia, Medellin.")
        lat, long = 6.2443382, -75.573553

    # Convertimos el string dado por el usuario en un objeto tipo datetime
    dt = datetime.strptime(when, '%Y-%m-%d')

    # Obtener la zona horaria correspondiente a las coordenadas
    timezone_str = tzwhere.tzwhere().tzNameAt(lat, long)
    local = timezone(timezone_str)

    # Convertir la fecha a UTC
    local_dt = local.localize(dt, is_dst=None)
    utc_dt = local_dt.astimezone(timezone('UTC'))

    # Convertir la fecha y hora UTC a un objeto "Time" para realizar cálculos
    # astronómicos.
    ts = load.timescale()

    # Crear objeto time para el inicio y fin del intervalo de tiempo
    t0 = ts.from_datetime(utc_dt)
    t1 = t0 + timedelta(days=1)

    # Crea un objeto "observador" en una ubicación geográfica específica y en
    # un momento determinado.
    observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=long)

    # Cargamos las efemérides del objeto celeste que queremos mirar
    eph = load('de421.bsp')
    body = eph[f'{object}']

    # Obtiene la información de los momentos en que el objeto está arriba y
    # abajo del horizonte.
    f = risings_and_settings(eph, body, observer)

    # Crea una lista para almacenar los momentos en que el objeto está arriba
    # del horizonte 
    times = []

    # Recorre los momentos en que el objeto está arriba y abajo del horizonte
    # y los agrega a la lista.
    for t, updown in zip(*find_discrete(t0, t1, f)):
        # si updown es verdadero, significa que el objeto celeste está
        # ascendiendo en el horizonte
        if updown:
            times.append(
                f"Rises on {t.astimezone(local).strftime('%A %d, %m, %Y')} at {t.astimezone(local).strftime('%H:%M')}")
        else:
            times.append(
                f"Sets on {t.astimezone(local).strftime('%A %d, %m, %Y')} at {t.astimezone(local).strftime('%H:%M')}")

    # retornamos la lista con las fechas y horas en que el objeto celeste se
    # eleva o se pone en el horizonte
    return times
