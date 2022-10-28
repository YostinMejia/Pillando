from restaurante import *

from admin_bd import *
from admin_general import *
from admin_locales import *

from usuario_estudiante import *
from usuario_profesor import *
from usuario_universidadadminstrador import *


if __name__=="__main__":

    # Prueba administrador general Listo
    admingeneral=AdministradorGeneral("4","pan","rodrigo","gerente")
    admingeneral.actualizarCalificacionComentarios("2")
    admingeneral.actualizarCalificacionRestaurante("2")
    
    #Prueba administrador base de datos  Listo
    # adminbd=AdministradorBd("5","ruco","lamelo","administrador")
    # adminbd.agregarRestaurante("Todo a Mil","bloque 12","12pm-23am")
    # adminbd.eliminarRestaurante("5")
    # adminbd.eliminarComentarios("37")


    #Usuarios Listo
    # user_estudiante=Estudiante("2","canca","pablo","sistemas")
    # print(user_estudiante.enviarComentarioProducto("7","haburguesa deliciosa, muy fresca y orgánica, adicionalmente con precios muy buenos!"))
    # print(user_estudiante.enviarComentarioRestaurante("10","Buena comida, excelente atención de Paola, lugar muy agradable y muy buena música . Cerveza artesanal deliciosa"))
    # print(user_estudiante.infoRestaurante("10","comentarios"))
    # print(user_estudiante.infoRestaurante("10","calificacion"))
    # print(user_estudiante.infoRestaurante("10","horario"))
    # print(user_estudiante.infoRestaurante("10","ubicacion"))
    # print(user_estudiante.buscarProductosGeneral("salchipapa"))
    # print(user_estudiante.buscarProductosRestaurante("hamburguesa","Abarrotes Don José")) #Hay que respetar las mayusculas y tildes en los nombres

