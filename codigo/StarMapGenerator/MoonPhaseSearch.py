import datetime
from skyfield.api import load
from skyfield.framelib import ecliptic_frame


def moon_phase(year, month, day, hour=0, minute=0, second=0):
    """
    Calcula la fase de la Luna en una fecha y hora dadas.

    Args:
    - year (int): Año.
    - month (int): Mes.
    - day (int): Día.
    - hour (int): opcional, Hora (por defecto es 0).
    - minute (int): opcional, Minutos (por defecto es 0).
    - second (int): opcional, Segundos (por defecto es 0).

    Retorna:
    - Una tupla con tres valores: el ángulo de la fase lunar y el porcentaje de la
    Luna iluminada y el numero de la imagen correspondiente a la fase lunar (0-15).
    """

    # Cargar la escala de tiempo.
    ts = load.timescale()

    # Crear un objeto Time en función de los parámetros de entrada.
    t = ts.utc(year, month, day, hour, minute, second)

    # Cargar los cuerpos celestes necesarios desde el archivo de421.bsp.
    eph = load('de421.bsp')
    sun, moon, earth = eph['sun'], eph['moon'], eph['earth']

    # Obtener las posiciones de la Tierra, el Sol y la Luna en el tiempo t.
    earth_t = earth.at(t)
    sun_t = earth_t.observe(sun).apparent()
    moon_t = earth_t.observe(moon).apparent()

    # Calcular las longitudes eclípticas del Sol y la Luna.
    _, sunlon, _ = sun_t.frame_latlon(ecliptic_frame)
    _, moonlon, _ = moon_t.frame_latlon(ecliptic_frame)

    # La fase de la luna se define como el angulo entre la luna y el sol a lo
    # largo de la eliptica
    phase = (moonlon.degrees - sunlon.degrees) % 360.0

    # Calcular el porcentaje de la Luna iluminada.
    percent_illuminated = 100.0 * moon_t.fraction_illuminated(sun)

    # Obtener el numero de imagen en base al ángulo
    image_num = obtain_phase_image(phase)

    return phase, percent_illuminated, image_num


def obtain_phase_image(angle):
    """
    Calcula la fase lunar en función del ángulo dado en grados.

    Args:
        angle (float): ángulo en grados.

    Returns:
        int: número de fase lunar (0 a 15) correspondiente al ángulo dado,
            o None si el ángulo no corresponde a ninguna fase lunar.

    """
    # Diccionario con los intervalos de ángulo (en grados) para cada fase
    # lunar.
    intervalos = {
        0: (348.75, 11.25),  # Luna nueva
        15: (11.25, 33.75),
        14: (33.75, 56.25),
        13: (56.25, 78.75),
        12: (78.75, 101.25),  # Cuarto creciente
        11: (101.25, 123.75),
        10: (123.75, 146.25),
        9: (146.25, 168.75),
        8: (168.75, 191.25),  # Luna llena
        7: (191.25, 213.75),
        6: (213.75, 236.25),
        5: (236.25, 258.75),
        4: (258.75, 281.25),  # Cuarto menguante
        3: (281.25, 303.75),
        2: (303.75, 326.25),
        1: (326.25, 348.75),
    }

    # Comprobamos si el ángulo se corresponde con la Luna nueva (fase 0).
    if angle > 348.75 or angle < 11.25:
        return 0

    # Comprobamos si el ángulo se corresponde con alguna fase lunar.
    for fase, intervalo in intervalos.items():
        if intervalo[0] <= angle < intervalo[1]:
            return fase

    # Si el ángulo no se corresponde con ninguna fase lunar, devolvemos None.
    return None
