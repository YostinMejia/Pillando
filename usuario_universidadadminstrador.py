from usuario import *

class UniversidadAdminstrador(Usuario):

    def __init__(self, id: str, apodo: str, nombre: str, cargo:str) -> None:
        super().__init__(id, apodo, nombre)
        self.__cargo=cargo
        