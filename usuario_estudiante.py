from usuario import *

class Estudiante(Usuario):

    def __init__(self, id: str, apodo: str, nombre: str, carrera:str) -> None:
        super().__init__(id, apodo, nombre)
        self.__carrera=carrera