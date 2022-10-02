"""Guardar los datos una sola vez y luego el administrador puede actualizar los comentarios y calificación, 
para poder usar la herencia y no llamar todo de la base de datos, disminuir el tiempo de ejecución"""

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
        comentario=(None,id_restaurante,comentario,date.today(),)

        #qmark style
        cur.execute("INSERT INTO comentarios VALUES(?,?,?,?)",comentario)
        print("Comentario enviado")
        con.commit()
    
    #--------------------Hay que mirar que el chat bot revise los id y según el nombre que arroje el ususario ponga los id----------------------

    def infoRestaurante(self,id_restaurante:str,info:str)-> None:

        obj_temp=Restaurante(str(id_restaurante))
        info=str(info)

        if info=="comentarios": #comentarios
            obj_temp.mirarComentarios()
        elif info=="calificacion": #calificacion
            obj_temp.mirarCalificacion()
        elif info=="horario": #horario
            obj_temp.mirarHorario()
        elif info=="ubicacion": #ubicacion
            obj_temp.mirarUbicacion()
    
    def buscarProducto(self,id_restaurante:str,producto:str):
        obj_temp=Restaurante(id_restaurante)
        obj_temp.mirarProductos(producto)
  

