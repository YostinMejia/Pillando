from datetime import date
import sqlite3 as sql
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import spacy
from textblob import TextBlob

from restaurante import *

#Inicia coneccion con la bd
con=sql.connect("database.db")
cur=con.cursor()

class Usuario:
    
    def __init__(self,id:str, apodo:str, nombre:str )-> None:
        self.__id=id
        self.__apodo=apodo
        self.__nombre=nombre
    
    def misComentarios(self)->tuple:
        cur.execute("SELECT comentario, fecha FROM comentarios WHERE id_usuario= ?" ,(self.__id,))
        comentarios=cur.fetchall()
        restaurantes_comentarios=["restaurantes"]
        restaurantes_comentarios.append(comentarios)
        

        cur.execute("SELECT comentario, fecha FROM comentarios_productos WHERE id_usuario= ?" ,(self.__id,))
        comentarios=cur.fetchall()
        productos_comentados=["productos"]
        productos_comentados.append(comentarios)

        return restaurantes_comentarios, productos_comentados


    def __enviarComentario(self, producto_o_restaurante:str , id:str, txt:str )->tuple:
        #Cargamos Spacy en español
        nlp=spacy.load("es_core_news_lg")

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
        

        enviar=[None,id,None,comentario,date.today(),analisis["compound"],no_stop_words,self.__id]

        return enviar


    def enviarComentarioProducto(self , id_producto:str, txt:str)->str:

        cur.execute("SELECT id_restaurante FROM productos WHERE id=?",(id_producto,))
        id_restaurante=cur.fetchone()
        
        if id_restaurante==None:

            return("No hay ningun prodcuto con esa id")

        else:    
            id_restaurante=id_restaurante[0]

            enviar=self.__enviarComentario("producto", id_producto, txt)

            enviar[2]=id_restaurante
            enviar=tuple(enviar)


            cur.execute("INSERT INTO comentarios_productos VALUES(?,?,?,?,?,?,?,?)", enviar)
            con.commit()

            return "Comentario enviado"
        
    def enviarComentarioRestaurante(self,id_restaurante:str,txt:str)-> str:


        enviar=self.__enviarComentario("restaurante",id_restaurante, txt)
        enviar.pop(2)
        enviar=tuple(enviar)

        #qmark style
        cur.execute("INSERT INTO comentarios VALUES(?,?,?,?,?,?,?)",enviar)
        con.commit()

        return "Comentario enviado"

    
    #--------------------Hay que mirar que el chat bot revise los id y según el nombre que arroje el ususario ponga los id----------------------

    def infoRestaurante(self, id_restaurante:str, info:str)-> str|list:

        obj_temp=Restaurante(str(id_restaurante))

        if "comentarios" in info: #comentarios
            dato=obj_temp.mirarComentarios()

        if "calificacion"  in info: #calificacion
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

            dato=(estrellas,calificacion)

        if "horario"  in info: #horario
            dato=(obj_temp.mirarHorario())
        if "ubicacion"  in info: #ubicacion
            dato=(obj_temp.mirarUbicacion())
        
        return dato

    def buscarProductosGeneral(self,nombre_producto:str)-> None:

        cur.execute("SELECT * FROM productos WHERE (nombre LIKE ? OR alias LIKE ?)",(f"{nombre_producto}%",f"{nombre_producto}%",))
        productos=cur.fetchall()
        list_restaurantes=[]

        #Si sen encuentra el producto en local solicitado

        if (productos)!=None and len(productos)!=0:

            for i in range(len(productos)):

                cur.execute("SELECT * FROM restaurante WHERE id=?",(f"{productos[i][2]}"))
                restaurante=cur.fetchone()
                list_restaurantes.append(restaurante)

                if productos[i][4]!=None:
                    if productos[i][5]!=None:
                        print(f"{productos[i][5]} cuesta {productos[i][3]}, esta disponible en {restaurante[1]} {restaurante[2]}. \n Descripción: {productos[i][4]} \n")
                        
                    else:
                        print(f"{productos[i][1]} cuesta {productos[i][3]}, esta disponible en {restaurante[1]} {restaurante[2]}. \n Descripción: {productos[i][4]} \n")
                else:
                    print(f"{productos[i][1]} cuesta {productos[i][3]}, esta disponible en {restaurante[1]} {restaurante[2]}. \n")   
        else:

            nombre_productos_recortado=nombre_producto[0:(len(nombre_producto))//2]

            cur.execute("SELECT * FROM productos WHERE nombre LIKE ? OR alias LIKE ?",(f"{nombre_productos_recortado}%",f"{nombre_productos_recortado}%",))
            productos=cur.fetchall()

            if (productos)!=None and len(productos)!=0:

                for i in range(len(productos)):
                    cur.execute("SELECT * FROM restaurante WHERE id=?",(f"{productos[i][2]}"))
                    restaurante=cur.fetchone()
                    list_restaurantes.append(restaurante)


                    if productos[i][4]!=None:
                        if productos[i][5]!=None:
                            print(f"{productos[i][5]} cuesta {productos[i][3]}, esta disponible en {restaurante[1]} {restaurante[2]}. \n Descripción: {productos[i][4]} \n")
                        else:
                            print(f"{productos[i][1]} cuesta {productos[i][3]}, esta disponible en {restaurante[1]} {restaurante[2]}. \n Descripción: {productos[i][4]} \n")
                    else:
                        print(f"{productos[i][1]} cuesta {productos[i][3]}, esta disponible en {restaurante[1]} {restaurante[2]}. \n")   
                
            #Si no en encuentra
            else:
                print(f"Le toco salir de la universidad a buscar porque aquí no hay {nombre_producto}")
        
        return productos,list_restaurantes


    def buscarProductosRestaurante(self,nombre_producto:str,nombre_resaurante:str=None )-> None:
        
        cur.execute("SELECT id FROM restaurante WHERE nombre= ? ",(f"{nombre_resaurante}",))
        id_restaurante=cur.fetchone()
        
        productos=None
        list_restaurantes=[]

        if id_restaurante!=None:

            cur.execute("SELECT * FROM productos WHERE nombre LIKE ? and id_restaurante= ? ",(f"{nombre_producto}%" ,f"{id_restaurante[0]}",))
            productos=cur.fetchall()

            if productos!=None and len(productos)!=0:

                for i in range(len(productos)):

                    #Se seleccionan los datos del restaurante
                    
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
                print(f"El local {nombre_resaurante} no tiene {nombre_producto} ")
            
        
        else:
            print(f"El local {nombre_resaurante} no esta registrado o revise si escribio bien el nombre")
        
        return productos, list_restaurantes

       