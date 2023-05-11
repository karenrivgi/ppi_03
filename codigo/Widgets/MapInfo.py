import tkinter as tk
from tkinter import ttk
from os.path import abspath, dirname, join
from Widgets.Helpers import WebScrapping
from tkhtmlview import HTMLLabel


class MapInfo:
    """Clase encargada de crear el widget correspondiente a la 
    funcionalidad que permite conocer la informacion de los astros en el
    mapa generado.

    Atributos:
    - user (User): instancia del usuario.
    - starMap (tk.Canvas): canvas base
    - inner_frame (tk.Frame): frame sobre el cual se agrega la informacion
    del mapa

    Metodos:
    - destroy(): destruye el canvas base.
    """

    recursos_path = join(dirname(dirname(abspath(__file__))), "Recursos")

    def do_nothing():
        pass

    def destroy(self):
        """Destruye el canvas base."""

        self.starMap.destroy()

    def __init__(self, master: tk.Canvas, estrellas=None, planeta=None,
                 constelacion=None, user=None) -> None:
        """Metodo constructor encargado de crear la instancia del widget
        y de construir la interfaz grafica.

        Parametros:
        - master (tk.Canvas): contenedor padre sobre el cual se crea el 
        widget
        - estrellas (list): lista de las estrellas presentes en el mapa 
        generado
        - planetas (str): nombre del planeta consultado en el mapa
        - constelaciones (str): nombre de la constelacion seleccionada
        en el mapa
        - user (User): instancia del usuario que esta usando la aplicacion
        """

        # instancia del usuario
        self.user = user

        # Frame contenedor
        self.starMap = tk.Frame(
            master,
            width=764,
            height=750,
            background="black",
            highlightthickness=0)
        self.starMap.update_idletasks()
        self.starMap.pack(expand=True)

        # Crea un scrollbar vertical y lo posiciona, para visualizar todo el
        # contenido
        scrollbar = ttk.Scrollbar(master=self.starMap, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # crea un canvas contenedor
        canvas = tk.Canvas(
            master=self.starMap,
            yscrollcommand=scrollbar.set,
            width=745,
            height=750,
            background="black")
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=canvas.yview)

        # crea un frame interior sobre el cual se podrá scrollear
        self.inner_frame = tk.Frame(canvas, background="black")
        canvas.create_window(
            (0, 0), window=self.inner_frame, anchor="nw", width=745)

        # extraemos la informacion del mapa, pormedio de la funcion de web scrapping
        mapinfo = WebScrapping.map_info(constelacion, estrellas, planeta)

        # llenamos el frame interno con la informacion extraida
        for key in mapinfo.keys():

            if key == 'Stars':

                for star in mapinfo[key]:
                    my_label = HTMLLabel(self.inner_frame, html=star)

                    # Adjust label
                    my_label.pack(pady=3, fill="both", expand=True)

            else:
                my_label = HTMLLabel(self.inner_frame, html=mapinfo[key])

                # Adjust label
                my_label.pack(pady=3, fill="both", expand=True)

        # event listener que ayuda a lograr el scrolleo sobre el frame interno
        self.inner_frame.bind(
            "<Configure>", lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")))
