from datetime import date
import sqlite3 as sql
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import spacy

from administradores import *

#Cargamos Spacy en español
nlp=spacy.load("es_core_news_lg")

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
        
    def enviarComentario(self,id_restaurante:str,txt:str)-> None:

        comentario=txt

        traducido=TextBlob(comentario).translate(from_lang="es", to="en") #Se traduce el comentario
        analisis=SentimentIntensityAnalyzer().polarity_scores(traducido) 

        comentario=nlp(comentario)
        limpiado=[]
       
        for i in comentario:
            if (not i.is_stop and not i.is_punct and (re.search("[0-9]", i.text)==None)): # Se buscan stop words o números
                limpiado.append(i.text) 

        limpiado=" ".join(limpiado) #Se convierte a string
        comentario=comentario.text #Se convierte el objeto nlp por el texto
        
        enviar=(None,id_restaurante,comentario,date.today(),analisis["compound"],limpiado,)
        #qmark style
        cur.execute("INSERT INTO comentarios VALUES(?,?,?,?,?,?)",enviar)
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
  

