import datetime
import tkinter as tk
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from StarMapGenerator import skymap
from tkinter import filedialog
from os.path import abspath, dirname, join
# from api_reddit import make_posts_reddit


class StarMap:

    recursos_path = join(dirname(dirname(abspath(__file__))),"Recursos")

    canvas_skymap = None
    fecha_hora_str = None
    ubicacion_str = None

    def save_data(self):

        # Accedemos a las variables globales de fecha, hora y ubicación
        global fecha_hora_str, ubicacion_str

        # Obtenemos la fecha y hora ingresadas por el usuario
        fecha = self.date.get()
        hora = self.hour.get()

        # Convertimos la fecha y hora a objetos datetime
        fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d')
        hora_obj = datetime.datetime.strptime(hora, '%H:%M')

        # Combinamos la fecha y hora en un solo objeto datetime
        fecha_hora_obj = fecha_obj.replace(hour=hora_obj.hour, minute=hora_obj.minute)

        # Convertimos el objeto datetime a una cadena de texto y lo guardamos en la variable global
        fecha_hora_str = fecha_hora_obj.strftime('%Y-%m-%d %H:%M')

        # Obtenemos los valores de los campos de entrada para la ubicación
        pais = self.country.get()
        departamento = self.province.get()
        ciudad = self.city.get()

        # Unimos los valores en una cadena de texto separada por comas y lo guardamos en la variable global
        ubicacion_str = f"{pais}, {departamento}, {ciudad}"

        # Mostramos un mensaje al usuario indicando que los datos han sido guardados
        messagebox.showinfo("Guardado", "Los datos han sido guardados.")

        # Habilitar el botón "Mostrar gráfico"
        self.submitButton.config(state='normal')
    
    def show_image(self):
        
        global fecha_hora_str, ubicacion_str, canvas_skymap
        
        # Crear la figura y el canvas
        if self.user:
            self.user.guardar_historial([fecha_hora_str, ubicacion_str])

        fig = skymap.generar_mapa(fecha_hora_str, ubicacion_str, self.figMaster.winfo_height())
        canvas = FigureCanvasTkAgg(fig, master= self.figMaster)
        canvas_skymap = canvas
        canvas.draw()
        canvas.get_tk_widget().grid(column = 0, row = 0, pady= 20)

        self.downloadButton.config(state='normal')
        self.shareButton.config(state='normal')
        #Mostrar la ventana de Tkinter
        self.starMap.mainloop()

    def save_image(self):
        global canvas_skymap

        # Obtener el nombre del archivo y la ubicación donde se guardará la imagen
        filename = filedialog.asksaveasfilename(defaultextension=".png")
        if filename == '':
            return
        # Guardar el archivo en la ruta pasada con el nombre seleccionado
        canvas_skymap.print_png(filename)
    
    '''
    def share_image(self):
        make_posts_reddit.make_post()
    '''

    def __init__(self, master: tk.Tk, user = None) -> None:

        self.user = user

        self.starMap = tk.Canvas(master, width= 764, height= 750, background= "black", highlightthickness=0)
        self.starMap.update_idletasks()
        # self.starMap.place(x= posx, y= posy)
        self.starMap.grid(sticky="nsew")

        ###
        self.canvasPosition = tk.Canvas(self.starMap, highlightthickness=0, background= "black")
        self.canvasPosition.update_idletasks()
        self.canvasPosition.grid(row=0, column=0, sticky="nsew")
        self.canvasPosition.grid_anchor("center")

        self.countryText = tk.Label(self.canvasPosition, text= "Country", font = ("BeVietnamPro-Bold", int(12)), width = 15, fg = "#ffffff", bg= "black")
        self.countryText.grid(row = 0, column = 0)

        self.provinceText = tk.Label(self.canvasPosition, text= "Province", font = ("BeVietnamPro-Bold", int(12)), width = 15, fg = "#ffffff", bg= "black")
        self.provinceText.grid(row = 0, column = 1)

        self.cityText = tk.Label(self.canvasPosition, text= "City", font = ("BeVietnamPro-Bold", int(12)), width = 15, fg = "#ffffff", bg= "black")
        self.cityText.grid(row = 0, column = 2)
        
        self.country = tk.Entry(
            master=self.canvasPosition,
            bd = 0,
            highlightthickness = 0,
            font=("BeVietnamPro 12"), width = 15)
        
        self.country.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.province = tk.Entry(
            master=self.canvasPosition,
            bd = 0,
            highlightthickness = 0,
            font=("BeVietnamPro 12"), width = 15)
        
        self.province.grid(row = 1, column = 1, padx = 5, pady = 5)

        self.city = tk.Entry(
            master=self.canvasPosition,
            bd = 0,
            highlightthickness = 0,
            font=("BeVietnamPro 12"), width = 15)
        
        self.city.grid(row = 1, column = 2, padx = 5, pady = 5)

        ###
        self.canvasDate = tk.Canvas(self.starMap, highlightthickness=0, background= "black")
        self.canvasDate.update_idletasks()
        self.canvasDate.grid(row=1, column=0, sticky="nsew")
        self.canvasDate.grid_anchor("center")

        self.dateText = tk.Label(self.canvasDate, text= "Date", font = ("BeVietnamPro-Bold", int(12)), width = 15, fg = "#ffffff", bg= "black")
        self.dateText.grid(row = 0, column = 0)

        self.hourText = tk.Label(self.canvasDate, text= "Hour", font = ("BeVietnamPro-Bold", int(12)), width = 15, fg = "#ffffff", bg= "black")
        self.hourText.grid(row = 0, column = 1)


        self.date = tk.Entry(
            master=self.canvasDate,
            bd = 0,
            highlightthickness = 0,
            font=("BeVietnamPro 12"), width = 15)
        #print(self.date.winfo_width())
        
        self.date.grid(row = 1, column = 0, padx = 5, pady = 5)


        self.hour = tk.Entry(
            master=self.canvasDate,
            bd = 0,
            highlightthickness = 0,
            font=("BeVietnamPro 12"), width = 15)
        
        self.hour.grid(row = 1, column = 1, padx = 5, pady = 5)
    
        ###
        self.buttonParent = tk.Canvas(self.starMap, highlightthickness=0, background= "black")
        self.buttonParent.update_idletasks()
        self.buttonParent.grid(row=2,column=0, sticky="nsew")
        self.buttonParent.grid_anchor("center")

        self.img0 = tk.PhotoImage(file = join(StarMap.recursos_path,"SubmitButton.png"))
        self.submitButton = tk.Button(
            master= self.buttonParent,
            image = self.img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.show_image,
            relief = "flat",
            state="disabled",
            bg= "black")
        
        self.submitButton.grid(row=0, column=1, columnspan=2, padx = 5, pady = 5)

        self.img1 = tk.PhotoImage(file = join(StarMap.recursos_path,"SaveButon.png"))
        self.saveButton = tk.Button(
            master= self.buttonParent,
            image = self.img1,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.save_data,
            relief = "flat",
            bg= "black")
        
        self.saveButton.grid(row=0, column=0, padx = 5, pady = 5)
        
        if self.user:

            self.img2 = tk.PhotoImage(file = join(StarMap.recursos_path,"DownloadButton.png"))

            self.downloadButton = tk.Button(
                master= self.buttonParent,
                image = self.img2,
                borderwidth = 0,
                highlightthickness = 0,
                command = self.save_image,
                relief = "flat",
                state="disabled",
                bg= "black")
            
            self.downloadButton.grid(row=1, column=0, padx = 5, pady = 5)

            self.img3 = tk.PhotoImage(file = join(StarMap.recursos_path,"ShareButton.png"))

            self.shareButton = tk.Button(
                master= self.buttonParent,
                image = self.img3,
                borderwidth = 0,
                highlightthickness = 0,
                command = self.save_data,
                relief = "flat",
                state="disabled",
                bg= "black")
            
            self.shareButton.grid(row=1, column=1, padx = 5, pady = 5)

        
        self.figMaster = tk.Canvas(self.starMap, highlightthickness=0, background= "black")
        self.figMaster.update_idletasks()
        self.figMaster.grid(row=3, column = 0, sticky="nsew")
        self.figMaster.grid_anchor("s")
        self.figMaster.update_idletasks()
        #print(self.figMaster.winfo_height())

        self.canvasStarsInfo = tk.Canvas(self.starMap, width= 220, highlightthickness=0, background= "black")
        self.figMaster.update_idletasks()
        self.canvasStarsInfo.grid(row = 0, column = 1, rowspan=4, sticky="ns")