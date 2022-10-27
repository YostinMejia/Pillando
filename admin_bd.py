import sqlite3 as sql

from usuario import *

#Inicia coneccion con la bd
con=sql.connect("database.db")
cur=con.cursor()

class AdministradorBd(Usuario):

    def __init__(self, id: str, apodo: str, nombre: str, cargo:str,comentarios=...) -> None:
        super().__init__(id, apodo, nombre, comentarios)
        self.__cargo=cargo


    def agregarRestaurante(self,nombre:str,ubicacion:str,horario:str)-> None:
        nombre=nombre.lower()
        ubicacion=ubicacion.lower()
        
        #qmark style 
        restaurante=(None,nombre,ubicacion,0,horario,)
        cur.execute("INSERT INTO restaurante VALUES(?,?,?,?,?)",restaurante)
        print("Restaurante ingresado")
        con.commit()
    
    def eliminarRestaurante(self, id_restaurante:str)-> None:

        #elimina el restaurante de la tabla "restaurante"
        cur.execute("DELETE FROM restaurante WHERE id=?",(id_restaurante))
        #productos del restaurante
        cur.execute("DELETE FROM productos WHERE id_restaurante=? ",(id_restaurante))
        #comentarios de su restaurante
        cur.execute("DELETE FROM comentarios WHERE id_restaurante=? ",(id_restaurante))
        #comentarios de sus productos
        cur.execute("DELETE FROM comentarios_productos WHERE id_restaurante=? ",(id_restaurante))
        
        con.commit()

        print("Restaurante eliminado")


    def eliminarComentarios(self, id_comentario:str)-> None:
        cur.execute("DELETE FROM comentarios WHERE id= ?",(id_comentario,))
        con.commit()
        print("Comentario eliminado")

