from datetime import date
import sqlite3 as sql
from tempfile import TemporaryDirectory
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from translate import Translator
import re
import spacy

from restaurante import *

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
        #qmark style
        comentario=txt

        palabra=Translator(from_lang="es", to_lang="en").translate(comentario) #Se traduce cada comentario
        analisis=SentimentIntensityAnalyzer().polarity_scores(palabra) 

        numeros=re.findall("[0-9]",txt)         #Se buscan los numeros 
        txt=list(txt)         #se convierte el comentario en lista
        for i in numeros:
            txt.remove(i)         #Se eliminan los numeros del comentario ya que spacy no los cuenta como stop
        
        
        txt="".join(txt) #Se convierte en string la lista
        #Se usa spacy (nlp)
        temp_txt=nlp(txt)
        for i in temp_txt:
            if (i.is_stop or i.is_punct):
                txt.remove(i) # Se eliminan los stop words
        
        enviar=(None,id_restaurante,comentario,date.today(),analisis["compound"],txt,)

        #qmark style
        cur.execute("INSERT INTO comentarios VALUES(?,?,?,?)",enviar)
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
  

