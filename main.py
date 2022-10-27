from restaurante import *

from admin_bd import *
from admin_general import *
from admin_locales import *

from usuario_estudiante import *
from usuario_profesor import *
from usuario_universidadadminstrador import *


if __name__=="__main__":
    
    # juan=Estudiante("1","brayan","juan","sistemas")
    # print(juan.mirarComentarios())
    # # id del restaurante y  tipo de informacion
    # juan.enviarComentarioProducto("23","Gran Barbacoa de pollo curry de mariscos. Precioso sabores frescos con productos locales.")
    # juan.enviarComentarioProducto("2","Carne de pollo y curries fantástico. Me encanta. Gran trabajo Ton Khao.")
    # juan.enviarComentarioRestaurante("5","Comida deliciosa! Y servido por la encantadora Kiefie hizo y agradable experiencia en un restaurante de comidas")
    # juan.enviarComentarioRestaurante("5","Este lugar es un favorito, y en un día soleado de invierno, almuerzo gloriosamente aquí era perfecto. Tuve la ensalada de pollo con yogurt quinoa minty, que era tan delicioso aderezo y unas copas de Pinot Grigio.")
    # juan.buscarProductosRestaurante("salchipapa","Don Beto") #Hay que escribir el nombre respetando mayusculas
    # juan.infoRestaurante("1","comentarios")
    # print()
    # juan.infoRestaurante("1","ubicacion")
    # print()
    # juan.infoRestaurante("1","horario")
    # print()
    # juan.infoRestaurante("1","calificacion")
    # print()
    # juan.buscarProducto("1","hamburguesa")
    # print()
    # juan.enviarComentario("4","muy buena comida , me encantó")

    #Prueba administrador general Listo
    # admingeneral=AdministradorGeneral("4","pan","rodrigo","gerente")
    # admingeneral.actualizarCalificacionComentarios("2")
    # admingeneral.actualizarCalificacionRestaurante("2")
    
    #Prueba administrador base de datos  Listo
    adminbd=AdministradorBd("5","ruco","lamelo","administrador")
    # adminbd.agregarRestaurante("Todo a Mil","bloque 12","12pm-23am")
    # adminbd.eliminarRestaurante("5")
    adminbd.eliminarComentarios("36")

    
    # adminbd.eliminarRestaurante("9")

    
    # adminLocal=AdminwistradorLocal("3","pedro","pedro","5")
    # adminLocal.graficarCalificacion()

