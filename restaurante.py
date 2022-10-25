import sqlite3 as sql
import re

from textblob import TextBlob
from unicodedata import normalize

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
        self.__calificacion=calificacion
            

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
        return self.__calificacion


    def mirarComentarios(self)-> list:
        
        cur.execute("SELECT comentario,fecha FROM comentarios WHERE id_restaurante=?",(f"{self.id}",))
        lista_comentarios=cur.fetchall()

        return lista_comentarios


    #Se mira también la palabra más repetida 

    """Hay que mirar si quiere una cantidad minima de palabras"""
    
    def mirarpalabrasRepetidas(self,lista_palabras:list) -> dict:
        
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

                    if lista_palabras[j] in repetidas: 
                        repetidas[lista_palabras[j]]+=count #Se guardan las palabras 
                    else:
                        repetidas[lista_palabras[j]]=count #Se guardan las palabras 

        return repetidas

                