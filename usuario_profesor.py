from usuario import *

class Profesor(Usuario):

    def __init__(self, id: str, apodo: str, nombre: str, cursos:str) -> None:
        super().__init__(id, apodo, nombre)
        self.__cursos=cursos
    