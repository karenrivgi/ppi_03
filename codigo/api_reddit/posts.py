class Post:
    """Clase usada para representar los post extraidos mediante la API de reddit.

        atributos:
            - header (str): titulo del post
            - body (str): cuerpo de texto del post
            - image_path (str): path local de la imagen guardada al momento de descargar las imagenes 
            - author (str): autor del post
            - score (int): numero de upvotes del post
            - subreddit (str): nombre del subreddit del cual se recuperó el post
    """

    def __init__(self, header, body, author, score, subreddit, image_path=None):
        self.header = header
        self.body = body
        self.image_path = image_path
        self.author = author
        self.score = score
        self.subreddit = subreddit
