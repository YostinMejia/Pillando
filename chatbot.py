import sqlite3 as sql
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import date
from textblob import TextBlob
import re
from unicodedata import normalize
import matplotlib.pyplot as mtp

con=sql.connect("database.db")
cur=con.cursor()

#Limpia el str antes de hacer un select a la bd
def limpiarStr(palabra):
    # -> NFD y eliminar diacríticos
    palabra = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", palabra), 0, re.I)
    palabra=re.sub("[^\w\s]","",palabra)
    palabra=re.sub("[0-9_]","",palabra)
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
        productos=cur.fetchall()
        self.productos=productos
            
        #Se guardan los comentarios
        comentarios=cur.fetchall()
        self.comentarios=comentarios

        #Luego cuando el usuario quiera ver la calificacion se otorga la calificacion
        self.calificacion=calificacion


    def mirarProductos(self,eleccion=None):
        eleccion=limpiarStr(eleccion)
    
        cur.execute("SELECT * FROM productos")
        productos=cur.fetchall()
        
        #hay que mirar si el restarurante está abierto---------

        #Se mira si el usuario escogio algun producto para buscar 
        if eleccion==None:
            for i in range(len(productos)):
                if productos[i][4]!=None:
                    if productos[i][5]!=None:
                        print(f"{productos[i][5]} cuesta {productos[i][3]}. \n descripción: {productos[i][4]} ")
                    else:
                        print(f"{productos[i][1]} cuesta {productos[i][3]}. \n descripción: {productos[i][4]}")
                else:
                    print(f"{productos[i][1]} cuesta {productos[i][3]}.")
        else:
            cur.execute("SELECT * FROM productos WHERE id_restaurante= ? and (nombre LIKE ? OR alias LIKE ?)",(f"{self.id}",f"{eleccion}%",f"{eleccion}%",))
            productos=cur.fetchall()
            
            if len(productos)!=0:
                for i in range(len(productos)):
                    if productos[i][4]!=None:
                        if productos[i][5]!=None:
                            print(f"{productos[i][5]} cuesta {productos[i][3]}. \n descripción: {productos[i][4]} ")
                        else:
                            print(f"{productos[i][1]} cuesta {productos[i][3]}. \n descripción: {productos[i][4]}")
                    else:
                        print(f"{productos[i][1]} cuesta {productos[i][3]}.")
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
        print(f" {self.nombre} queda en el {ubicacion[0]}")
    
    def mirarHorario(self):
        cur.execute("SELECT horario FROM restaurante")
        horario=cur.fetchall()
        print(f"{self.nombre} tiene un horario de {horario[0]}")

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
        if calificacion>=0.4:
            if calificacion<=0.6:
                calificacion="★ ★ ★"
            elif calificacion>0.6 and calificacion>0.6:
                calificacion="★ ★ ★ ★"
            else:
                calificacion="★ ★ ★ ★ ★"
        elif calificacion <=-0.2:
            calificacion="☆"
        else:
            calificacion="★ ★ ☆"
        
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

class Usuario:
    def __init__(self,id,apodo) -> None:
        self.id=id
        self.apodo=apodo
    
    def enviarComentario(self,restaurante:str,comentario:str):
        # date(año,mes,dia)
        pass

    def infoRestaurante(self,restaurante:Restaurante):
        pass
    
    