import sqlite3 as sql
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy

from usuario import *


#Inicia coneccion con la bd
con=sql.connect("database.db")
cur=con.cursor()

class AdministradorGeneral(Usuario):

    def __init__(self, id: str, apodo: str, nombre: str, cargo:str) -> None:
        super().__init__(id, apodo, nombre)
        self.__cargo=cargo

    def actualizarCalificacionRestaurante(self,id_restaurante:str):
        
        cur.execute("SELECT calificacion FROM comentarios WHERE id_restaurante=?",(id_restaurante,))
        comentarios=cur.fetchall()
        # print(comentarios)
        calificacion=0

        actualizo_calificacion=0

        if len(comentarios)==0:
            print("El restaurante no tiene comentarios ")
        else:
            for i in range(len(comentarios)):

                #Si el comentario no tiene calificacion se llama otra funcion para que lo califique
                if comentarios[i][0]==None:
                        self.actualizarCalificacionComentarios(id_restaurante)
                        actualizo_calificacion+=1

                else:
                    calificacion+=comentarios[i][0]


            #Si se actualizo algun comentario entonces se vuelve a ejecutar
            if actualizo_calificacion!=0:
                self.actualizarCalificacionRestaurante(id_restaurante)

            #Si no se actualizo ningun comentario
            else:
                #El promdio de calificacion
                calificacion/=len(comentarios)


            datos=(calificacion,id_restaurante,)
            cur.execute(f"UPDATE restaurante SET calificacion=? WHERE id=? ",datos)
            con.commit()

            print("calificacion actualizada")


    """Esta es importante porque a veces se acaba el espacion en memoria para traducir entonces deja de funcionar el analisis de sentiemientos
    Por lo que se debe de mirar que no arroje el mismo "compound" en todos los comentarios"""
    
    """Hay que mirar que si se este traduciendo y no se haya agotado la memoria TRY EXCEPT"""

    def actualizarCalificacionComentarios(self, id_restaurante:str):
        #Cargamos Spacy en español
        nlp=spacy.load("es_core_news_lg")
        #qmark style
        cur.execute("SELECT id,comentario,no_stop_words FROM comentarios WHERE id_restaurante=?",(f"{id_restaurante}",))
        datos= cur.fetchall()


        for i in range(len(datos)):
            id_comentario=datos[i][0]

            comentario=datos[i][1]
            
            # #Se analiza el senimiento del comentario
            traducido=TextBlob(comentario).translate(from_lang="es", to="en")
            analisis=SentimentIntensityAnalyzer().polarity_scores(traducido) 

            comentario=nlp(comentario)

            limpiado=[]

            # Si ya está no_stop_word entonces no se actualiza
            if datos[i][2]==None:
                for i in comentario:
                    if (not i.is_stop and not i.is_punct and not i.is_digit): # Se buscan stop words , caracteres especiales números
                        limpiado.append(i.text) 
                limpiado=" ".join(limpiado) #Se convierte a string
                
                enviar=(analisis["compound"],limpiado,id_comentario,)

                #qmark style
                cur.execute("UPDATE comentarios SET calificacion=? , no_stop_words=? WHERE id=? ",enviar)
                con.commit()
                print("no stop words y sentimiento actualizados actualizado")

            else:
                enviar=(analisis["compound"],id_comentario,)
                cur.execute("UPDATE comentarios SET calificacion=? WHERE id=? ",enviar)
                con.commit()
                print("sentimiento actualizado")