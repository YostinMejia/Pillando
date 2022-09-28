import sqlite3 as sql
import re

import matplotlib.pyplot as mtp
from textblob import TextBlob
from unicodedata import normalize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from translate import Translator


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
        self.comentarios=comentarios

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

        print(estrellas)

        #Config para graficar
        mtp.style.use(['dark_background'])
        mtp.plot(fechas,reseña,linestyle="-",color="g",label=F"RESEÑA DE LOS COMENTARIOS DE {self.nombre}")
        mtp.legend()
        mtp.xlabel("FECHA")
        mtp.ylabel("CALIFICACIÓN")
        mtp.title(f"Calificación comentarios")
        mtp.show()
        
        return calificacion


    def mirarComentarios(self):
        
        cur.execute("SELECT comentario,fecha FROM comentarios WHERE id_restaurante=?",(f"{self.id}",))
        lista_comentarios=cur.fetchall()

        if lista_comentarios==[]:
            print("No hay comentarios")
        else:
            self.comentarios=lista_comentarios
            for i in lista_comentarios:
                print(i[0],f"Publicado el {i[1]}\n")


    #Se mira también la palabra más repetida 
    def mirarComentariosAdmin(self,palabra=False):

        cur.execute("SELECT comentario,fecha FROM comentarios WHERE id_restaurante=?",(f"{self.id}",))
        lista_comentarios=cur.fetchall()

        repetidas={}
        #Algunas de las palabras que no evalua el sentiemiento deseado
        palabras_clave=["barato","caro","costoso","carísimo","baratisimo","valioso","económico","rebajado",
        "increíble","volveremos","exquisita","exquisito","apretados","llena","lleno","recomendable","ricos","gustó"]
        
        if lista_comentarios==[]:
            print("No hay comentarios")
        else:

            if palabra==False:
                self.comentarios=lista_comentarios
                repetidas={}
                #Se miran todas las palabras y se guarda cuantas veces estan repetidas
                for i in lista_comentarios:
                    print(i[0],f"Publicado el {i[1]}\n")
                    contando=TextBlob(i[0])
                    contando=contando.word_counts
                    llaves=list(contando.keys())
                    for i in llaves:

                        # Se evalua el sentimiento para guardar solamente las palbaras no neutrales 
                        print(i,end=" ")
                        palabra=Translator(from_lang="es", to_lang="en").translate(i) #Se traduce cada comentario
                        print(palabra,end=" ")
                        analisis=SentimentIntensityAnalyzer().polarity_scores(palabra) #Se analizan los sentimientos
                        print(analisis["compound"]) #Se le asigna el valor arrojado por el analisis 

                        #se mira que no sea una palabra neeutral o que este en palabras_claves
                        if analisis["compound"] > 0.1 or analisis["compound"] < -0.1 or (i in palabras_clave): 

                            if i in repetidas: #Se guardan las palabras 
                                repetidas[i]+=contando[i]
                            else:
                                repetidas[i]=contando[i]
                print(repetidas)
            else:
                repetidas={}
                #Se miran todas las palabras y se guarda cuantas veces estan repetidas
                for i in lista_comentarios:
                    print(i[0])
                    contando=TextBlob(i[0])
                    contando=contando.word_counts[palabra]
                    print(contando)
                    # repetidas[i]=contando[i]
                # print(repetidas)

                