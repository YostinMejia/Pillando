import sqlite3 as sql
from restaurante import *

#Inicia coneccion con la bd
con=sql.connect("database.db")
cur=con.cursor()

class Administrador():
    def __init__(self,id:str,nombre:str) -> None:
        self.id=id
        self.nombre=nombre

    def agregarRestaurante(self,nombre:str,ubicacion:str,horario:str)-> None:

        #qmark style 
        restaurante=(None,nombre,ubicacion,0,horario,)
        cur.execute("INSERT INTO restaurante VALUES(?,?,?,?,?)",restaurante)
        print("Restaurante ingresado")
        con.commit()


    def eliminarComentarios(self,comentario:str)-> None:
        cur.execute("DELETE FROM comentarios WHERE id= ?",(f"{comentario}",))
        con.commit()
        print("Comentario eliminado")
        # cur.execute("SELECT * FROM comentarios WHERE id=?",(f"{id_comentario}",))
        # dato=cur.fetchall()
        # print(dato)
        
class AdminLocal:

    def __init__(self,id_restaurante:str) -> None:
        self.id_restaurante:str=id_restaurante

    def agregarProducto(self,prod_nombre:str ,prod_precio:int ,prod_descripcion:str ,prod_alias:str)-> None:

        producto=(None,prod_nombre,self.id_restaurante,prod_precio,prod_descripcion,prod_alias,)
        
        cur.execute("INSERT INTO productos VALUES(?,?,?,?,?,?)",producto)
        con.commit()
        print("Producto Agregado")
        
    
    def actualizarProductos(self,id:str,dato:str,cambio:str)-> None:
        
        cur.execute("SELECT * FROM productos WHERE id=? ",(f"{id}",))
        producto=cur.fetchall()

        nombre=producto[0][1] #1
        precio=producto[0][3] #2
        descripcion=producto[0][4] #3
        alias=producto[0][5] #4
        
        if dato!="eliminar":

            if dato=="nombre":
                nombre=limpiarStr(nombre)
                nombre=cambio
            elif dato=="precio":
                precio=int(cambio)
            elif dato=="descripcion":
                descripcion=cambio
            elif dato=="alias":
                alias=cambio
            
            else:
                cambio=input("Digite un cambio valido: ")
                self.actualizarProductos(id,cambio)

            #Se aplica el cambio seleccionado
            actualizacion=(nombre,precio,descripcion,alias,id,)
            cur.execute("UPDATE productos SET nombre=? , precio=?, descripcion=?, alias=? WHERE id=? ",actualizacion)
            con.commit()
            print("producto actualizado")
        
        #Eliminar producto por id
        else:
            cur.execute("DELETE FROM productos WHERE id=? ",(f"{id}"),)
            con.commit()
            print("Producto eliminado")
        
    def cambiarInfoRestaurante(self,dato:str,cambio:str):

        if dato=="nombre":
            cur.execute("UPDATE restaurante SET nombre=? WHERE id=?",(f"{cambio}",f"{self.id_restaurante}",))
            con.commit()
        elif dato=="ubicacion":
            cur.execute("UPDATE restaurante SET ubicacion=? WHERE id=?",(f"{cambio}",f"{self.id_restaurante}",))
            con.commit()
        elif dato=="horario":
            cur.execute("UPDATE restaurante SET horario=? WHERE id=?",(f"{cambio}",f"{self.id_restaurante}",))
            con.commit()
    
    def mirarCalificacion(self):
        obj_temp=Restaurante(self.id_restaurante)
        obj_temp.mirarCalificacion()

    def mirarComentarios(self,palabra=False):
        obj_temp=Restaurante(self.id_restaurante)
        obj_temp.mirarComentariosAdmin(palabra)
