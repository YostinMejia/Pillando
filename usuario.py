from datetime import date
import sqlite3 as sql

from restaurante import *

#Inicia coneccion con la bd
con=sql.connect("database.db")
cur=con.cursor()

class Usuario:
    def __init__(self,id:str,apodo:str,nombre:str,carrera:str,comentarios=[]) -> None:
        self.id=id
        self.apodo=apodo
        self.nombre=nombre
        self.carerra=carrera
        self.comentarios=comentarios
        
    def enviarComentario(self,id_restaurante:str,comentario:str)-> None:
        #qmark style
        comentario=(None,id_restaurante,comentario,date.today(),self.id),

        #qmark style
        cur.executemany("INSERT INTO comentarios VALUES(?,?,?,?,?)",comentario)
        print("Comentario enviado")

        con.commit()
         
        
    
    #--------------------Hay que mirar que el chat bot revise los id y según el nombre que arroje el ususario ponga los id----------------------

    def infoRestaurante(self,id_restaurante:Restaurante,info:str)-> None:

        obj_temp=Restaurante(str(id_restaurante))
        info=str(info)
        if info=="1":#Productos
            producto=input("¿cual producto desea buscar?: ")
            obj_temp.mirarProductos(producto)
        elif info=="2": #comentarios
            obj_temp.mirarComentarios()
        elif info=="3": #calificacion
            obj_temp.mirarCalificacion()
        elif info=="4": #horario
            obj_temp.mirarHorario()
        elif info=="5": #ubicacion
            obj_temp.mirarUbicacion()
        

class Administrador:
    def __init__(self,id:str,nombre:str) -> None:
        self.id=id
        self.nombre=nombre

    def agregarRestaurante(self,nombre:str,productos:list,ubicacion:str,calificacion:int,horario:str,comentarios:list)-> None:

        #qmark style 
        restaurante=(None,nombre,"",ubicacion,0,horario,""),
        cur.executemany("INSERT INTO restaurante VALUES(?,?,?,?,?,?,?)",restaurante)
        print("Restaurante ingresado")
        con.commit()
        # if comentarios!=None:
    
    def actualizarProductos(self,id_producto:str,cambio:str)-> None:
        
        cur.execute("SELECT * FROM productos WHERE id=? ",(id_producto,))
        producto=cur.fetchall()
        id=producto[0][0]
        id_restaurante=producto[0][2] 

        nombre=producto[0][1] #1
        precio=producto[0][3] #2
        descripcion=producto[0][4] #3
        alias=producto[0][5] #4
        
        if cambio=="1":
            nombre=input("Nuevo nombre: ")
            nombre=limpiarStr(nombre)
        elif cambio=="2":
            precio=input(input("Nuevo precio: "))
        elif cambio=="3":
            descripcion=input("Nueva descripcion: ")
        elif cambio=="4":
            alias=input("Nuevo alias: ")
        #Eliminar producto por id
        elif cambio=="5":
            eliminar=input("id del producto a eliminar: ")
            eliminar=limpiarStr(eliminar)
            cur.execute("DELETE FROM productos WHERE id=? ",(eliminar,))
            print("Producto eliminado")

        actualizacion=(nombre,precio,descripcion,alias,id,)
        

        cur.execute("UPDATE productos SET nombre=? , precio=?, descripcion=?, alias=? WHERE id=? ",actualizacion)
        print("producto actualizado")

        con.commit()
         
        
    def ingresarProducto(self,prod_nombre:str,id_restaurante:str,prod_precio:int,prod_descripcion:str,prod_alias:str)-> None:

        # id nombre id_restaurante precio descripcion(opcional) alias(si tiene algun nombre propio del local)
        productos=(None,prod_nombre,id_restaurante,prod_precio,prod_descripcion,prod_alias,)  
        cur.execute("INSERT INTO productos VALUES(?,?,?,?,?,?)",productos)
        print("Producto Agregado")
        con.commit()
         

    def eliminarComentarios(self,id_comentario:str)-> None:

        cur.executemany("DELETE FROM comentarios WHERE id= ? ",(id_comentario,))
        print("Comentario eliminado")
        con.commit()
         

 
