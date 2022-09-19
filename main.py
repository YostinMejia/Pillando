from restaurante import *
from usuario import *

if __name__=="__main__":


    juan=Usuario(1,"mejia","juan","estudiante")
    #id del restaurante y  tipo de informacion
    juan.infoRestaurante("1","5")
    print()
    juan.infoRestaurante("1","3")
    print()
    juan.infoRestaurante("1","2")

    print()

    admin=Administrador("1","juan")

    #Id producto y tipo de cambio
    admin.actualizarProductos("1","3")
    print()
    admin.ingresarProducto("hamburguesa nazi","1",15000,"beibi dale suave cuando bajes","105f")
    print()

    don_beto=Restaurante("1")
    print()
    don_beto.mirarProductos("salchipapas")
    print()

    don_beto.mirarCalificacion()
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
    esquina.mirarProductos("salchip")
    esquina.mirarCalificacion()

    pass