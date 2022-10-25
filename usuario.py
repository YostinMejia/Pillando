from datetime import date
import sqlite3 as sql
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import spacy

from restaurante import *

#Inicia coneccion con la bd
con=sql.connect("database.db")
cur=con.cursor()

class Usuario:
    def __init__(self,id:str,apodo:str,nombre:str,comentarios=[]) -> None:
        self.__id=id
        self.__apodo=apodo
        self.__nombre=nombre
        self.__comentarios=comentarios
        
    def enviarComentario(self,id_restaurante:str,txt:str)-> None:
        #Cargamos Spacy en español
        nlp=spacy.load("es_core_news_lg")
        self.__comentarios.append([id_restaurante,txt])

        comentario=txt

        traducido=TextBlob(comentario).translate(from_lang="es", to="en") #Se traduce el comentario
        analisis=SentimentIntensityAnalyzer().polarity_scores(traducido) 

        comentario=nlp(comentario)
        no_stop_words=[]
       
       #Se eliminan las no stop words
        for i in comentario:
            if (not i.is_stop and not i.is_punct and (re.search("[0-9]", i.text)==None)): # Se buscan stop words o números
                no_stop_words.append(i.text) 

        no_stop_words=" ".join(no_stop_words) #Se convierte a string
        comentario=comentario.text #Se convierte el objeto nlp por el texto
        
        enviar=(None,id_restaurante,comentario,date.today(),analisis["compound"],no_stop_words,)
        #qmark style
        cur.execute("INSERT INTO comentarios VALUES(?,?,?,?,?,?)",enviar)
        print("Comentario enviado")
        con.commit()
    
    #--------------------Hay que mirar que el chat bot revise los id y según el nombre que arroje el ususario ponga los id----------------------

    def infoRestaurante(self,id_restaurante:str,info:str)-> str|list:

        obj_temp=Restaurante(str(id_restaurante))
        info=str(info)
        dato=""

        if info=="comentarios": #comentarios
            dato=obj_temp.mirarComentarios()

        elif info=="calificacion": #calificacion
            calificacion=obj_temp.mirarCalificacion()
            
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

            return estrellas,calificacion

        elif info=="horario": #horario
            dato=obj_temp.mirarHorario()
        elif info=="ubicacion": #ubicacion
            dato=obj_temp.mirarUbicacion()
        
        return dato

    def buscarProductosGeneral(self,nombre_producto:str)-> None:

        cur.execute("SELECT * FROM productos WHERE (nombre LIKE ? OR alias LIKE ?)",(f"{nombre_producto}%",f"{nombre_producto}%",))
        productos=cur.fetchall()
        list_restaurantes=[]
        #Si sen encuentra el producto en local solicitado
        if len(productos)!=0:

            for i in range(len(productos)):
                cur.execute("SELECT * FROM restaurante WHERE id=?",(f"{productos[i][2]}"))
                restaurante=cur.fetchone()
                list_restaurantes.append(restaurante)

                if productos[i][4]!=None:
                    if productos[i][5]!=None:
                        print(f"{productos[i][5]} cuesta {productos[i][3]}, esta disponible en {restaurante[1]} {restaurante[2]}. \n Descripción: {productos[i][4]} ")
                    else:
                        print(f"{productos[i][1]} cuesta {productos[i][3]}, esta disponible en {restaurante[1]} {restaurante[2]}. \n Descripción: {productos[i][4]}")
                else:
                    print(f"{productos[i][1]} cuesta {productos[i][3]}, esta disponible en {restaurante[1]} {restaurante[2]}.")   
        else:

            nombre_productos_recortado=nombre_producto[0:(len(nombre_producto))//2]

            cur.execute("SELECT * FROM productos WHERE nombre LIKE ? OR alias LIKE ?",(f"{nombre_productos_recortado}%",f"{nombre_productos_recortado}%",))
            productos=cur.fetchall()
            if len(productos)!=0:

                for i in range(len(productos)):
                    cur.execute("SELECT * FROM restaurante WHERE id=?",(f"{productos[i][2]}"))
                    restaurante=cur.fetchone()
                    list_restaurantes.append(restaurante)


                    if productos[i][4]!=None:
                        if productos[i][5]!=None:
                            print(f"{productos[i][5]} cuesta {productos[i][3]}, esta disponible en {restaurante[1]} {restaurante[2]}. \n Descripción: {productos[i][4]} ")
                        else:
                            print(f"{productos[i][1]} cuesta {productos[i][3]}, esta disponible en {restaurante[1]} {restaurante[2]}. \n Descripción: {productos[i][4]}")
                    else:
                        print(f"{productos[i][1]} cuesta {productos[i][3]}, esta disponible en {restaurante[1]} {restaurante[2]}.")   
                
            #Si no en encuentra
            else:
                print(f"Le toco salir de la universidad a buscar porque aquí no hay {nombre_producto}")
        
        return productos,list_restaurantes


    def buscarProductosRestaurante(self,nombre_producto:str,nombre_resaurante:str=None )-> None:
        
        cur.execute("SELECT id FROM restaurante WHERE nombre= ? ",(f"{nombre_resaurante}",))
        id_restaurante=cur.fetchone()
        
        if len(id_restaurante)!=0:

            cur.execute("SELECT * FROM productos WHERE nombre LIKE ? and id_restaurante= ? ",(f"{nombre_producto}%" ,f"{id_restaurante[0]}",))
            productos=cur.fetchall()

            if len(productos)!=0:
                for i in range(len(productos)):

                    #Se seleccionan los datos del restaurante
                    
                    cur.execute("SELECT * FROM restaurante WHERE id=?",(f"{productos[i][2]}"))
                    restaurante=cur.fetchone()

                    if productos[i][4]!=None:
                        if productos[i][5]!=None:
                            print(f"{productos[i][5]} cuesta {productos[i][3]}, esta disponible en {restaurante[1]} {restaurante[2]}. \n Descripción: {productos[i][4]} ")
                        else:
                            print(f"{productos[i][1]} cuesta {productos[i][3]}, esta disponible en {restaurante[1]} {restaurante[2]}. \n Descripción: {productos[i][4]}")
                    else:
                        print(f"{productos[i][1]} cuesta {productos[i][3]}, esta disponible en {restaurante[1]} {restaurante[2]}.")   
            
                return productos
            
            else:
                print(f"El local {nombre_resaurante} no tiene {nombre_producto} ")

        else:
            print(f"El local {nombre_resaurante} no esta registrado o revise si escribio bien el nombre")
