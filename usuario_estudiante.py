from usuario import *

class Estudiante(Usuario):

    def __init__(self, id: str, apodo: str, nombre: str, carrera:str, comentarios=[]) -> None:
        super().__init__(id, apodo, nombre, comentarios)
        self.__carrera=carrera

juan=Estudiante("1","panchi","juan","sistemas")
# juan.buscarProductosGeneral("salchipapa")
print(juan.infoRestaurante("1","calificacion"))