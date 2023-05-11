import tkinter as tk
from tkinter import ttk
from api_reddit import get_posts_data


class Newsfeed:
    """Esta clase se encarga de instanciar el widget sobre el cual se mostrarán los
    diferentes post sacados de los subreddits seleccionados previamente.

        atributos de instancia:
            - master (tk.Canvas): instancia del contenedor principal del widget
            - newsfeed (tk.Frame): instancia del frame contenedor de todos los widgets
            necesarios para mostrar los posts
            - scrollbar (tk.Scrollbar): instancia del scrollbar para permitir el desplazamiento vertical
            en el widget
            - post_container (tk.Canvas): instancia del canvas contenedor que permite organizar la estructura
            junto con el scrollbar
            - post_frame (tk.Frame): instancia del frame que contendrá la estructura de los diferentes post

        metodos:
            - create_widgets(): funcion encargada de crear la estructura del newsfeed
            - add_posts(): funcion encargada de crear cada estructura de un post
            - get_posts(): funcion encargada de recuperar los posts por medio de la API de reddit
    """

    def destroy(self):
        """Destruye el widget del objeto tkinter."""
        self.newsfeed.destroy()

    def __init__(self, master, user):
        """constructor encargado de crear la estrucrura del newsfeed

            parametros:
                - master (tk.Canvas)
                - user (Usuario)
        """

        self.master = master
        self.newsfeed = tk.Frame(
            self.master,
            width=master.winfo_reqwidth(),
            height=750)
        self.create_widgets()
        self.get_posts()
        master.create_window((0, 0), window=self.newsfeed, anchor="nw")
        # self.newsfeed.place(x = 0, y = 0)

    def create_widgets(self):
        """encargada de crear las instancias de los widgets necesarios, y
        posicionarlos adecuadamente en el contenedor principal del newsfeed
        """

        # crear la scrollbar y el canvas contenedor que nos permitirá el
        # desplazamiento vertical
        self.scrollbar = ttk.Scrollbar(self.newsfeed, orient="vertical")
        self.post_container = tk.Canvas(
            self.newsfeed,
            width=self.newsfeed.winfo_reqwidth() -
            self.scrollbar.winfo_reqwidth(),
            height=self.newsfeed.winfo_reqheight())

        # enlazar el scrollbar al canvas contenedor y posicionamiento de ambos
        # en el frame contenedor del newsfeed
        self.post_container.configure(yscrollcommand=self.scrollbar.set)
        self.post_container.pack(side="left", fill="both", expand=True)
        self.scrollbar.configure(command=self.post_container.yview)
        self.scrollbar.pack(side="right", fill="y")

        # creación del frame contenedor de todos los post que posteriormente se
        # anexaŕan
        self.post_frame = tk.Frame(self.post_container, bg="#2255a5")

        # anexión de eventListener qjue permitirá la actualización constante de
        # la región del desplazamiento vertical
        self.post_frame.bind(
            "<Configure>", lambda e: self.post_container.configure(
                scrollregion=self.post_container.bbox("all")))

        # posicionamiento del frame de los post, en el canvas que permite el
        # desplazamiento vertical
        self.post_container.create_window(
            (0,
             0),
            window=self.post_frame,
            anchor="nw",
            width=self.post_container.winfo_reqwidth())

    def add_posts(self, post):
        """encargada de crear la estructura de cada post y anexarlo al contenedor de todos los posts"""

        # crear el frame de cada post
        new_post = tk.Frame(self.post_frame, padx=10, pady=10, bg="black")

        # crear el label del titulo
        header_label = tk.Label(
            new_post,
            text=post.header,
            font=(
                "Arial",
                19,
                "bold"),
            fg="#47a3cb",
            bg="black",
            wraplength=self.post_container.winfo_reqwidth() -
            20)
        header_label.pack(side="top", fill="x", pady=5)

        # agregar el label del body, si hay body
        if post.body:
            body_label = tk.Label(
                new_post,
                text=post.body,
                font=(
                    "BeVietnamPro-Bold",
                    15),
                fg="white",
                bg="black",
                wraplength=self.post_container.winfo_reqwidth() -
                20)
            body_label.pack(side="top", fill="x", pady=5)

        # agregar label de imagen, si hay imagen
        if post.image_path:
            try:
                image = tk.PhotoImage(file=post.image_path)
                image_label = tk.Label(new_post, image=image, bg="black")
                image_label.image = image
                image_label.pack(side="top", fill="x", pady=5)
            except tk.TclError:
                pass

        # agregar label de upvotes
        upvotes_label = tk.Label(
            new_post,
            text="Upvotes: " +
            post.score,
            font=(
                "BeVietnamPro-Bold",
                14,
                "bold"),
            fg="#47a3cb",
            bg="black")
        upvotes_label.pack(side="top", fill="x", pady=5)

        # agregar label del subreddit del que se recuperó la informacion
        subreddit_label = tk.Label(
            new_post,
            text="Subreddit: " +
            post.subreddit,
            font=(
                "BeVietnamPro-Bold",
                12,
                "bold"),
            fg="white",
            bg="black")
        subreddit_label.pack(side="top", fill="x", pady=5)

        # agregar el label de la persona que hizo el post
        author_label = tk.Label(
            new_post,
            text="Author: " +
            post.author,
            font=(
                "BeVietnamPro-Bold",
                12,
                "bold"),
            fg="white",
            bg="black")
        author_label.pack(side="top", fill="x", pady=5)

        new_post.pack(fill="x", pady=5)

    def get_posts(self):

        # recuperar los post por medio de la conexión a la API
        posts = get_posts_data.get_posts(4)
        # print(len(posts))

        # crear cada post y anexarlo al newsfeed
        for post in posts:
            self.add_posts(post)
