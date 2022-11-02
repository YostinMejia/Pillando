from restaurante import *

from admin_bd import *
from admin_general import *
from admin_locales import *

from usuario_estudiante import *
from usuario_profesor import *
from usuario_universidadadminstrador import *


if __name__=="__main__":

    # Prueba administrador general Listo
    # admingeneral=AdministradorGeneral("4","pan","rodrigo","gerente")
    # admingeneral.actualizarCalificacionComentarios("2") #importante porque aveces se acaba el espacio para traducir
    # admingeneral.actualizarCalificacionRestaurante("2")
    # admingeneral.actualizarCalificacionRestaurante("6")


    #Prueba administrador base de datos  Listo
    # adminbd=AdministradorBd("5","ruco","lamelo","administrador")
    # adminbd.agregarRestaurante("prueba final","bloque 8","12pm-23am")
    # adminbd.eliminarRestaurante("11")
    # adminbd.eliminarComentarios("43")

    #Prueba administrador del local

    # adminlocal=AdministradorLocal("2","pacho","samuel","2")
    # adminlocal.agregarProducto("hamburguesa con cangrejo",21000,"trae cangrejo y queso","cangreburguer")
    
    # adminlocal.actualizarProducto("29","precio","90000000")
    # adminlocal.actualizarProducto("29","nombre","paloma")
    # adminlocal.actualizarProducto("29","descripcion","paloma")
    # adminlocal.actualizarProducto("29","alias","peru")
    # adminlocal.actualizarProducto("29","eliminar","peru")


    # adminlocal.cambiarInfoRestaurante("nombre","perritos y algo mas")
    # adminlocal.cambiarInfoRestaurante("ubicacion","bloque 3")
    # adminlocal.cambiarInfoRestaurante("horario","2pm-12pm")

    # print(adminlocal.mirarCalificacion())
    # adminlocal.graficarCalificacion()
    # print(adminlocal.palabrasRepetidas(["menús"]))

    # rest=Restaurante("2")

    #Usuarios Listo
    user_estudiante=Estudiante("2","canca","pablo","sistemas")
    # print(user_estudiante.misComentarios())
    # print(user_estudiante.enviarComentarioProducto("7","salchipapas deliciosa, muy fresca y orgánica"))
    # print(user_estudiante.enviarComentarioRestaurante("10","Buena comida, excelente atención de sara"))
    # print(user_estudiante.infoRestaurante("2","comentarios"))
    # print(user_estudiante.infoRestaurante("10","calificacion"))
    # print(user_estudiante.infoRestaurante("10","horario"))
    # print(user_estudiante.infoRestaurante("10","ubicacion"))
    # print(user_estudiante.buscarProductosGeneral("salchiipapa"))
    # print(user_estudiante.buscarProductosRestaurante("hamburguesa","Abarrotes Don José")) #Hay que respetar las mayusculas y tildes en los nombres

