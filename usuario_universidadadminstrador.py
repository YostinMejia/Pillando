from usuario import *

class UniversidadAdminstrador(Usuario):

    def __init__(self, id: str, apodo: str, nombre: str, cargo:str,comentarios=[]) -> None:
        super().__init__(id, apodo, nombre, comentarios)
        self.__cargo=cargo
        