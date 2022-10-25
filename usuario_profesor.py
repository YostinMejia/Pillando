from usuario import *

class Profesor(Usuario):

    def __init__(self, id: str, apodo: str, nombre: str, cursos:str, comentarios=[]) -> None:
        super().__init__(id, apodo, nombre, comentarios)
        self.__cursos=cursos
    