import sqlite3 as sql
import re

from textblob import TextBlob
from unicodedata import normalize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import spacy

#Cargamos Spacy en español
nlp=spacy.load("es_core_news_lg")

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
        cur.execute(f"SELECT * FROM restaurante WHERE id=?",(self.id,))
        datos=cur.fetchall()
        self.nombre=datos[0][1]
        self.ubicacion=datos[0][2]
        self.horario=datos[0][4]

        #Se guardan los productos de la tabla productos
        self.productos=productos
            
        #Se guardan los comentarios
        self.comentarios=int(datos[0][3])

        #Luego cuando el usuario quiera ver la calificacion se otorga la calificacion
        self.calificacion=calificacion


    def mirarProductos(self,eleccion:str):
        eleccion=limpiarStr(eleccion)
    
        cur.execute("SELECT * FROM productos WHERE id_restaurante= ? and (nombre LIKE ? OR alias LIKE ?)",(f"{self.id}",f"{eleccion}%",f"{eleccion}%",))
        productos=cur.fetchall()

        #Si sen encuentra el producto en local solicitado
        if len(productos)!=0:

            for i in range(len(productos)):
                if productos[i][4]!=None:
                    if productos[i][5]!=None:
                        print(f"{productos[i][5]} cuesta {productos[i][3]}, esta disponible en {self.nombre} {self.ubicacion}. \n descripción: {productos[i][4]} ")
                    else:
                        print(f"{productos[i][1]} cuesta {productos[i][3]}, esta disponible en {self.nombre} {self.ubicacion}. \n descripción: {productos[i][4]}")
                else:
                    print(f"{productos[i][1]} cuesta {productos[i][3]}, esta disponible en {self.nombre} {self.ubicacion}.")
        
        #Si no en encuentra
        else:
            #Se recorta la palabra y se vulve a buscar en el mismo local
            tamano=len(eleccion)
            eleccion2=eleccion
            eleccion=eleccion[0:(tamano//2)]
            cur.execute("SELECT * FROM productos WHERE id_restaurante= ? and (nombre LIKE ? OR alias LIKE ?)",(f"{self.id}",f"{eleccion}%",f"{eleccion}%",))
            productos=cur.fetchall()

            #si no se encuentra nada en el local solicitado
            if len(productos)==0:
                print(f"{eleccion2} no está disponible en {self.nombre}")

                pregunta=input("¿Desea ver si esta disponible en otro local?-> ")
                pregunta=limpiarStr(pregunta).lower()
                #Solo se controla si escribe "si" -----------------------------chatobot-----------------------------
                #Si desea buscar en todos los locales
                if pregunta=="si":
                    cur.execute("SELECT * FROM productos WHERE nombre LIKE ? OR alias LIKE ?",(f"{eleccion}%",f"{eleccion}%",))
                    productos=cur.fetchall()

                    #Si se encuentra el producto en cualquier local
                    if len(productos)!=0:

                        for i in range(len(productos)):

                            # Se busca el(los) nombre(s) del restaurante que lo tiene y su ubicacion
                            id_restaurante=productos[i][2]
                            cur.execute("SELECT nombre,ubicacion FROM restaurante WHERE id=?",(id_restaurante,))
                            restaurante=cur.fetchall()

                            if productos[i][4]!=None:
                                if productos[i][5]!=None:
                                    print(f"{productos[i][5]} cuesta {productos[i][3]} y está disponible en  \n{restaurante[0][0]} {restaurante[0][1]}. \n descripción: {productos[i][4]} \n")
                                else:
                                    print(f"{productos[i][1]} cuesta {productos[i][3]} y está disponible en  \n{restaurante[0][0]} {restaurante[0][1]}. \n descripción: {productos[i][4]} \n")
                            else:
                                print(f"{productos[i][1]} cuesta {productos[i][3]} y está disponible en \n{restaurante[0][0]} {restaurante[0][1]}. \n")
                    
                    #Si no se encuentra nada en ningun local
                    else:
                        print(f"Le toco salir de la universidad a buscar porque aquí no hay {eleccion2}")
            

    def mirarUbicacion(self):
        cur.execute("SELECT ubicacion FROM restaurante")
        ubicacion=cur.fetchall()
        print (f" {self.nombre} queda en el {ubicacion[0][0]}")
    
    def mirarHorario(self):
        cur.execute("SELECT horario FROM restaurante")
        horario=cur.fetchall()
        print (f"{self.nombre} tiene un horario de {horario[0][0]}")

    def mirarCalificacion(self):
        cur.execute("SELECT calificacion FROM restaurante WHERE id=?",(f"{self.id}",))
        calificacion=cur.fetchall()
        calificacion=calificacion[0][0]

        if calificacion>=0.4:
            if calificacion<=0.55:
                estrellas="★ ★ ☆"
            elif calificacion>=0.55 and calificacion<=0.6:
                estrellas="★ ★ ★"
            elif calificacion>=0.6 and calificacion<=0.7:
                estrellas="★ ★ ★ ☆"
            else:
                estrellas="★ ★ ★ ★ ★"
        else:
            if calificacion>-0.5:
                estrellas="☆ "
            else:
                estrellas="🗑️"

        return estrellas

    def mirarComentarios(self)-> list:
        
        cur.execute("SELECT comentario,fecha FROM comentarios WHERE id_restaurante=?",(f"{self.id}",))
        lista_comentarios=cur.fetchall()

        return lista_comentarios


    #Se mira también la palabra más repetida 

    """Hay que mirar si quiere una cantidad minima de palabras"""
    
    def palabrasRepetidas(self,lista_palabras:list) -> dict:
        
        cur.execute("SELECT no_stop_words FROM comentarios")
        lista_comentarios=cur.fetchall()

        repetidas={}

        #Si no selecciono ninguna palabra en especifico
        if lista_palabras==None:

            #Se miran todas las palabras y se guarda cuantas veces estan repetidas
            for i in range(len(lista_comentarios)):
                
                palabras=TextBlob(lista_comentarios[i][0])  #Se guarda el no stop words
                contando=palabras.word_counts   #Se cuentan las palabras
                llaves=list(contando.keys())

                # #Por primera vez, se pueden guardar todas las palabras ya que el dict repetidas está vacio
                if i==0:
                    repetidas=dict(contando)
                else:    
                    for j in llaves:
                        if i in repetidas: #Se guardan las palabras 
                            repetidas[j]+=contando[j]
                        else:
                            repetidas[j]=contando[j]
                            
        #Si selecciono una o varias palabras se buscan
        else:
            for i in range(len(lista_comentarios)):
            #Se miran todas las palabras y se guarda cuantas veces estan repetidas
                contando=TextBlob(lista_comentarios[i][0])

                for j in range(len(lista_palabras)):
                    count=contando.word_counts[lista_palabras[j]]

                    if lista_palabras[j] in repetidas: #Se guardan las palabras 
                        repetidas[lista_palabras[j]]+=count
                    else:
                        repetidas[lista_palabras[j]]=count

        return repetidas

                