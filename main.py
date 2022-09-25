from restaurante import *
from usuario import *

if __name__=="__main__":

    juan=Usuario(1,"mejia","juan","estudiante")
    # id del restaurante y  tipo de informacion
    juan.infoRestaurante("1","comentarios")
    print()
    juan.infoRestaurante("1","ubicacion")
    print()
    juan.infoRestaurante("1","horario")
    print()
    juan.infoRestaurante("1","calificacion")
    print()
    juan.buscarProducto("1","hamburguesa")
    print()
    juan.enviarComentario("1","muy buen restaurante la comida me gusto pero podría mejorar la carne frita mama guevo")

    #Prueba administrador
    admin=Administrador("1","juan")
    admin.agregarRestaurante("Care pinga","bloque 8","12:03am - 8:00 pm")
    print()
    admin.eliminarComentarios("31")

    # Id producto y tipo de cambio
    adminLocal=AdminLocal("1")
    adminLocal.agregarProducto("papas con unicornio",15000,"Ey muy buenas a todos guapisimos","Vicente")
    print()
    adminLocal.actualizarProductos("23","nombre","salchipapasx")
    print()
    adminLocal.actualizarProductos("23","precio","777")
    print()
    adminLocal.actualizarProductos("23","descripcion","trae salchichon de cabra portuguesa")
    print()
    adminLocal.actualizarProductos("23","alias","CR7")
    print()      
    adminLocal.mirarCalificacion()  
    print()  

    adminLocal2=AdminLocal("7")  
    adminLocal2.cambiarInfoRestaurante("nombre","Juanito alimaña")
    print()
    adminLocal2.cambiarInfoRestaurante("ubicacion","bloque 90")
    print()
    adminLocal2.cambiarInfoRestaurante("horario","6:00 am - 9:00pm")
    print()


    don_beto=Restaurante("1")
    print()
    don_beto.mirarProductos("perro")
    print()

    panaderia_miguel=Restaurante("2")
    print()

    panaderia_miguel.mirarProductos("per")
    print()

    panaderia_miguel.mirarCalificacion()
    print()

    pregunte=Restaurante("3")
    print()

    pregunte.mirarProductos("jba")
    print()

    pregunte.mirarCalificacion()
    print()

    don_jose=Restaurante("4")
    print()

    don_jose.mirarProductos("sold")
    print()
    don_jose.mirarCalificacion()
    print()

    providencia=Restaurante("5")
    providencia.mirarProductos("salchip")
    providencia.mirarCalificacion()
    print()

    esquina=Restaurante("6")
    esquina.mirarProductos("hamburgueaxas")
    esquina.mirarCalificacion()
