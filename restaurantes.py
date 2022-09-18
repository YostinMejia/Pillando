from datetime import date
from itertools import product
import sqlite3 as sql
import re

import matplotlib.pyplot as mtp
from textblob import TextBlob
from unicodedata import normalize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import chatbot 

#Inicia coneccion con la bd
con=sql.connect("database.db")
cur=con.cursor()

#Limpia el str antes de hacer un select a la bd
def limpiarStr(palabra):
    # -> NFD y eliminar diacríticos
    palabra = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", palabra), 0, re.I)
    palabra=re.sub("[^\w\s]","",palabra)
    # -> NFC
    palabra= normalize( 'NFC', palabra)
    return palabra


#El usuario puede crear un objeto restaurante y este se puede almacenar en un json para no repetirlo
class Restaurante:

    def __init__(self,id:str,productos="",comentarios=[],calificacion=0) -> None:
        
        self.id=str(id)

        #Se guardan los datos basicos que estan en la tabla restaurante
        cur.execute(f"SELECT * FROM restaurante WHERE id=?",(f"{self.id}",))
        datos=cur.fetchall()
        self.nombre=datos[0][1]
        self.ubicacion=datos[0][3]
        self.horario=datos[0][4]

        #Se guardan los productos de la tabla productos
        self.productos=productos
            
        #Se guardan los comentarios
        self.comentarios=comentarios

        #Luego cuando el usuario quiera ver la calificacion se otorga la calificacion
        self.calificacion=calificacion


    def mirarProductos(self,eleccion:str):
        eleccion=limpiarStr(eleccion)
    
        cur.execute("SELECT * FROM productos WHERE id_restaurante= ? and (nombre LIKE ? OR alias LIKE ?)",(f"{self.id}",f"{eleccion}%",f"{eleccion}%",))
        productos=cur.fetchall()
        
        if len(productos)!=0:
            for i in range(len(productos)):
                if productos[i][4]!=None:
                    if productos[i][5]!=None:
                        print(f"{productos[i][5]} cuesta {productos[i][3]}, esta disponible en {self.ubicacion}. \n descripción: {productos[i][4]} ")
                    else:
                        print(f"{productos[i][1]} cuesta {productos[i][3]}, esta disponible en {self.ubicacion}. \n descripción: {productos[i][4]}")
                else:
                    print(f"{productos[i][1]} cuesta {productos[i][3]}, esta disponible en {self.ubicacion}.")
        else:
            print(f"Este producto no está disponible en {self.nombre}")

            pregunta=input("¿Desea ver si esta disponible en otro local?-> ")
            pregunta=limpiarStr(pregunta).lower()
            #Solo se controla si escribe "si" -----------------------------chatobot-----------------------------
            if pregunta=="si":
                cur.execute("SELECT * FROM productos WHERE nombre LIKE ? OR alias LIKE ?",(f"{eleccion}%",f"{eleccion}%",))
                productos=cur.fetchall()
                if len(productos)!=0:
                    for i in range(len(productos)):
                        if productos[i][4]!=None:
                            if productos[i][5]!=None:
                                print(f"{productos[i][5]} cuesta {productos[i][3]} y está disponible en \n{self.nombre} {self.ubicacion}. \n descripción: {productos[i][4]} ")
                            else:
                                print(f"{productos[i][1]} cuesta {productos[i][3]} y está disponible en \n{self.nombre} {self.ubicacion}. \n descripción: {productos[i][4]}")
                        else:
                            print(f"{productos[i][1]} cuesta {productos[i][3]} y está disponible en \n{self.nombre} {self.ubicacion}.")
                else:
                    print(f"Le toco salir de la u a buscar porque aquí no hay {eleccion}")
                     

    def mirarUbicacion(self):
        cur.execute("SELECT ubicacion FROM restaurante")
        ubicacion=cur.fetchall()
        print (f" {self.nombre} queda en el {ubicacion[0][0]}")
    
    def mirarHorario(self):
        cur.execute("SELECT horario FROM restaurante")
        horario=cur.fetchall()
        print (f"{self.nombre} tiene un horario de {horario[0][0]}")

    def mirarCalificacion(self):
        
        cur.execute(f"SELECT comentario,fecha FROM comentarios WHERE id_restaurante=?",(f"{self.id}",))
        comentarios=cur.fetchall()
        self.comentarios=comentarios
        calificacion=0

        reseña=[]
        fechas=[]
        for i in range(len(comentarios)):

            txt=TextBlob(comentarios[i][0]).translate(from_lang="es", to="en") #Se traduce cada comentario
            analisis=SentimentIntensityAnalyzer().polarity_scores(txt) #Se analizan los sentimientos
            calificacion+=analisis["compound"] #Se le asigna el valor arrojado por el analisis 

            #append para graficar
            fechas.append(comentarios[i][1])
            reseña.append(analisis["compound"])

        #Se halla el promedio
        calificacion/=len(comentarios)
        self.calificacion=calificacion

        if calificacion>=0.4:
            if calificacion<=0.55:
                calificacion="★ ★ ☆"
            elif calificacion>=0.55 and calificacion<=0.6:
                calificacion="★ ★ ★"
            elif calificacion>=0.6 and calificacion<=0.7:
                calificacion="★ ★ ★ ☆"
            else:
                calificacion="★ ★ ★ ★ ★"
        else:
            if calificacion>-0.5:
                calificacion="☆ "
            else:
                calificacion="🗑️"

        print(calificacion)

        #Config para graficar
        mtp.style.use(['dark_background'])
        mtp.plot(fechas,reseña,linestyle="-",color="g",label=F"RESEÑA DE LOS COMENTARIOS DE {self.nombre}")
        mtp.legend()
        mtp.xlabel("FECHA")
        mtp.ylabel("CALIFICACIÓN")
        mtp.title(f"Calificación comentarios")
        mtp.show()


    def mirarComentarios(self):
        
        cur.execute("SELECT comentario,fecha FROM comentarios WHERE id_restaurante=?",(f"{self.id}",))
        lista_comentarios=cur.fetchall()

        if lista_comentarios==[]:
            print("No hay comentarios")
        else:
            self.comentarios=lista_comentarios
            for i in lista_comentarios:
                print(i[0],f"Publicado el {i[1]}\n")


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
        cur.close()
        
    
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
        con.close()
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
        
        print("cambiando la descripcion de",nombre)
        if cambio=="1":
            nombre=input("Nuevo nombre: ")
            nombre=limpiarStr(nombre)
        elif cambio=="2":
            precio=input(input("Nuevo precio: "))
        elif cambio=="3":
            descripcion=input("Nueva descripcion: ")
        elif cambio=="4":
            alias=input("Nuevo alias: ")
        
        actualizacion=(nombre,precio,descripcion,alias,id,)
        

        cur.execute("UPDATE productos SET nombre=? , precio=?, descripcion=?, alias=? WHERE id=? ",actualizacion)
        print("producto actualizado")

        con.commit()
        cur.close()
        
    def ingresarProducto(self,prod_nombre:str,id_restaurante:str,prod_precio:int,prod_descripcion:str,prod_alias:str)-> None:

        # id nombre id_restaurante precio descripcion(opcional) alias(si tiene algun nombre propio del local)
        productos=(None,prod_nombre,id_restaurante,prod_precio,prod_descripcion,prod_alias,)  
        cur.execute("INSERT INTO productos VALUES(?,?,?,?,?,?)",productos)
        print("Producto Agregado")
        con.commit()
        cur.close()

    def eliminarComentarios(self,id_comentario:str)-> None:

        cur.executemany("DELETE FROM comentarios WHERE id= ? ",(id_comentario,))
        print("Comentario eliminado")
        con.commit()
        cur.close()

#Cerramos coneccion con la bd
cur.close()
if __name__=="__main__":


    # juan=Usuario(1,"mejia","juan","estudiante")
    # juan.infoRestaurante("1","5")
    # admin=Administrador("1","juan")
    # admin.actualizarProductos("1","3")
    # admin.ingresarProducto("hamburguesa nazi","1",15000,"beibi dale suave cuando bajes","105f")

    # don_beto=Restaurante("1")
    # don_beto.mirarProductos("salchip")
    # don_beto.mirarCalificacion()

    # panaderia_miguel=Restaurante("2")
    # panaderia_miguel.mirarProductos("per")
    # panaderia_miguel.mirarCalificacion()

    # pregunte=Restaurante("3")
    # pregunte.mirarProductos("jba")
    # pregunte.mirarCalificacion()

    # don_jose=Restaurante("4")
    # don_jose.mirarProductos("sold")
    # don_jose.mirarCalificacion()

    # providencia=Restaurante("5")
    # providencia.mirarProductos("salchip")
    # providencia.mirarCalificacion()

    # esquina=Restaurante("6")
    # esquina.mirarProductos("salchip")
    # esquina.mirarCalificacion()

    pass
