import sqlite3 as sql

con=sql.connect("database.db")
cur=con.cursor()

def dbRestaurante(restaurante):   
    #qmark style 
    cur.executemany("INSERT INTO restaurante VALUES(?,?,?,?,?,?,?)",restaurante)
    con.commit()
    con.close()

def dbProductos(productos):
    #qmark style
    cur.executemany("INSERT INTO productos VALUES(?,?,?,?,?,?)",productos)
    con.commit()
    cur.close()

def dbComentarios(comentario):
    #qmark style
    cur.executemany("INSERT INTO comentarios VALUES(?,?,?,?)",comentario)
    con.commit()
    cur.close()

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import date
from textblob import TextBlob
import re
from unicodedata import normalize
import matplotlib.pyplot as mtp

#Limpia el str antes de hacer un select a la bd
def limpiarStr(palabra):
    # -> NFD y eliminar diacríticos
    palabra = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", palabra), 0, re.I)
    palabra=re.sub("[^\w\s]","",palabra)
    palabra=re.sub("[0-9_]","",palabra)
    # -> NFC
    palabra= normalize( 'NFC', palabra)
    return palabra

#Se busca el producto
def buscarProducto(producto):

    producto=limpiarStr(producto)

#hay que mirar si el restarurante está abierto---------

    if len(producto)>=3:

        cur.execute("SELECT * FROM productos WHERE nombre LIKE ?",(f"{producto}%",))
        lista_productos=cur.fetchall()

        if len(lista_productos)==0:

            print(f"{producto} no se encuntra disponible")
            print("Ingrese un producto valido")
            #Llamamos la misma funcion
            producto=limpiarStr(input("-> "))
            buscarProducto(producto)
            
        else:
            temp=producto[0:len(producto)//2]
            cur.execute("SELECT * FROM productos WHERE nombre LIKE ?",(f"{temp}%",))
            productos=cur.fetchall()
            print(productos)

    else:
        print(f"{producto} no se encuntra disponible")
        print("Ingrese un producto valido")
        #Llamamos la misma funcion
        producto=limpiarStr(input("-> "))
        buscarProducto(producto)

#El usuario puede crear un objeto restaurante y este se puede almacenar en un json para no repetirlo
class Restaurante:

    def __init__(self,id:str) -> None:
        self.id=str(id)

        #Se guardan los datos basicos que estan en la tabla restaurante
        cur.execute(f"SELECT * FROM restaurante WHERE id=?",(f"{self.id}",))
        datos=cur.fetchall()
        self.nombre=datos[0][1]
        self.ubicacion=datos[0][3]
        self.horario=datos[0][4]

        #Se guardan los productos de la tabla productos
        cur.execute(f"SELECT * FROM productos WHERE id_restaurante=?",(f"{self.id}",))
        productos=cur.fetchall()
        self.productos=productos
            
        #Se guardan los comentarios
        cur.execute(f"SELECT comentario,fecha FROM comentarios WHERE id_restaurante=?",(f"{self.id}",))
        comentarios=cur.fetchall()
        self.comentarios=comentarios

        #Luego cuando el usuario quiera ver la calificacion se otorga la calificacion
        self.calificacion=0
        
    def buscarProducto(self):
        pass

    def mirarUbicacion(self):
        cur.execute("SELECT ubicacion FROM restaurante")
        ubicacion=cur.fetchone()
        print(f" {self.nombre} queda en el {ubicacion[0]}")
    
    def mirarHorario(self):
        cur.execute("SELECT horario FROM restaurante")
        horario=cur.fetchone()
        print(f"{self.nombre} tiene un horario de {horario[0]}")

    def mirarCalificacion(self):
        
        cur.execute(f"SELECT comentario,fecha FROM comentarios WHERE id_restaurante=?",(f"{self.id}",))
        comentarios=cur.fetchall()
        # print(comentarios)
        self.comentarios=comentarios
        calificacion=0
        for i in range(len(comentarios)):
            txt=TextBlob(comentarios[i][0]).translate(from_lang="es", to="en") #Se traduce cada comentario
            analisis=SentimentIntensityAnalyzer().polarity_scores(txt) #Se analizan los sentimientos
            calificacion+=analisis["compound"] #Se le asigna el valor arrojado por el analisis 

        calificacion/=len(comentarios) #Se halla el promedio
        
        print("la calificacion",calificacion)
        #Graficar la calificacion por medio de fechas
        #utilizar el analisis de sentimientos

    def mirarComentarios(self):
        
        cur.execute("SELECT comentario,fecha FROM comentarios WHERE id_restaurante=?",(f"{self.id}",))
        lista_comentarios=cur.fetchall()

        if lista_comentarios==[]:
            print("No hay comentarios")
        else:
            self.comentarios=lista_comentarios
            for i in lista_comentarios:
                print(i[0],f"Publicado el {i[1]}\n")

don_beto=Restaurante("1")
don_beto.mirarCalificacion()

class Usuario:
    def __init__(self,id,apodo) -> None:
        self.id=id
        self.apodo=apodo
    
    def enviarComentario(self,restaurante:str,comentario:str):
        # date(año,mes,dia)
        pass

    def infoRestaurante(self,restaurante:Restaurante):
        pass
    
    
