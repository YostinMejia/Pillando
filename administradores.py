import sqlite3 as sql
from restaurante import *
import matplotlib.pyplot as plt
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy

#Cargamos Spacy en español
nlp=spacy.load("es_core_news_lg")

#Inicia coneccion con la bd
con=sql.connect("database.db")
cur=con.cursor()

class Administrador():
    def __init__(self,id:str,nombre:str) -> None:
        self.id=id
        self.nombre=nombre

    def agregarRestaurante(self,nombre:str,ubicacion:str,horario:str)-> None:

        #qmark style 
        restaurante=(None,nombre,ubicacion,0,horario,)
        cur.execute("INSERT INTO restaurante VALUES(?,?,?,?,?)",restaurante)
        print("Restaurante ingresado")
        con.commit()


    def eliminarComentarios(self,comentario:str)-> None:
        cur.execute("DELETE FROM comentarios WHERE id= ?",(f"{comentario}",))
        con.commit()
        print("Comentario eliminado")
        # cur.execute("SELECT * FROM comentarios WHERE id=?",(f"{id_comentario}",))
        # dato=cur.fetchall()
        # print(dato)    

    def actualizarCalificacionRestaurante(self,id_restaurante:str):
        
        cur.execute(f"SELECT calificacion FROM comentarios WHERE id_restaurante=?",(f"{id_restaurante}",))
        comentarios=cur.fetchall()
        calificacion=0

        actualizo_calificacion=0
        for i in range(len(comentarios)):
            #Si el comentario no tiene calificacion se llama otra funcion para que lo califique
            if comentarios[i][0]==None:
                self.actualizarCalificacionComentarios(id_restaurante)
                actualizo_calificacion+=1

        if actualizo_calificacion!=0:
            cur.execute(f"SELECT calificacion FROM comentarios WHERE id_restaurante=?",(f"{id_restaurante}",))
            comentarios=cur.fetchall()

        #Se halla el promedio
        calificacion/=len(comentarios)

        datos=(calificacion,id_restaurante,)
        cur.execute(f"UPDATE restaurante SET calificacion=? WHERE id=? ",datos)
        con.commit()


    #Esta es importante porque a veces se acaba el espacion en memoria para traducir entonces deja de funcionar el analisis de sentiemientos
    #Por lo que se debe de mirar que no arroje el mismo "compound" en todos los comentarios
    
    """Hay que mirar que si se este traduciendo y no se haya agotado la memoria TRY EXCEPT"""

    def actualizarCalificacionComentarios(self, id_restaurante:str):
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
     
        
class AdminLocal:

    def __init__(self,id_admin:str,id_restaurante:str) -> None:

        cur.execute(f"SELECT * FROM restaurante WHERE id=?",(id_restaurante,))
        datos=cur.fetchall()

        self.nombre_restaurante=datos[0][1]
        self.id_admin=id_admin
        self.id_restaurante:str=id_restaurante
        
        self.palabras_repetidas:dict={}

    def agregarProducto(self,prod_nombre:str ,prod_precio:int ,prod_descripcion:str ,prod_alias:str)-> None:

        producto=(None,prod_nombre,self.id_restaurante,prod_precio,prod_descripcion,prod_alias,)
        
        cur.execute("INSERT INTO productos VALUES(?,?,?,?,?,?)",producto)
        con.commit()
        print("Producto Agregado")
        
    
    def actualizarProductos(self,id:str,dato:str,cambio:str)-> None:
        
        cur.execute("SELECT * FROM productos WHERE id=? ",(f"{self.id_restaurante}",))
        producto=cur.fetchall()

        nombre=producto[0][1] #1
        precio=producto[0][3] #2
        descripcion=producto[0][4] #3
        alias=producto[0][5] #4
        
        if dato!="eliminar":

            if dato=="nombre":
                nombre=limpiarStr(nombre)
                nombre=cambio
            elif dato=="precio":
                precio=int(cambio)
            elif dato=="descripcion":
                descripcion=cambio
            elif dato=="alias":
                alias=cambio
            
            else:
                cambio=input("Digite un cambio valido: ")
                self.actualizarProductos(id,cambio)

            #Se aplica el cambio seleccionado
            actualizacion=(nombre,precio,descripcion,alias,id,)
            cur.execute("UPDATE productos SET nombre=? , precio=?, descripcion=?, alias=? WHERE id=? ",actualizacion)
            con.commit()
            print("producto actualizado")
        
        #Eliminar producto por id
        else:
            cur.execute("DELETE FROM productos WHERE id=? ",(f"{id}"),)
            con.commit()
            print("Producto eliminado")
        
    def cambiarInfoRestaurante(self,dato:str,cambio:str):

        if dato=="nombre":
            cur.execute("UPDATE restaurante SET nombre=? WHERE id=?",(f"{cambio}",f"{self.id_restaurante}",))
            con.commit()
        elif dato=="ubicacion":
            cur.execute("UPDATE restaurante SET ubicacion=? WHERE id=?",(f"{cambio}",f"{self.id_restaurante}",))
            con.commit()
        elif dato=="horario":
            cur.execute("UPDATE restaurante SET horario=? WHERE id=?",(f"{cambio}",f"{self.id_restaurante}",))
            con.commit()
    
    def mirarCalificacion(self):
        obj_temp=Restaurante(self.id_restaurante)

        return obj_temp.mirarCalificacion()

    def graficarCalificacion(self):

        cur.execute(f"SELECT comentario,fecha FROM comentarios WHERE id_restaurante=?",(f"{self.id_restaurante}",))
        comentarios=cur.fetchall()

        reseña=[]
        fechas=[]
        for i in range(len(comentarios)):
            
            txt=TextBlob(comentarios[i][0]).translate(from_lang="es", to="en") #Se traduce cada comentario
            analisis=SentimentIntensityAnalyzer().polarity_scores(txt) #Se analizan los sentimientos

            #append para graficar
            fechas.append(comentarios[i][1])
            reseña.append(analisis["compound"])
        
                #Config para graficar
        plt.style.use(['dark_background'])
        plt.plot(fechas,reseña,linestyle="-",color="g",label=F"RESEÑA DE LOS COMENTARIOS DE {self.nombre_restaurante}")
        plt.legend()
        plt.xlabel("FECHA")
        plt.ylabel("CALIFICACIÓN")
        plt.title(f"Calificación comentarios")
        plt.show()
    
    def mirarPalabrasRepetidas(self,actualizar=False,lista_palabras=None):
        
        if actualizar==True:
            obj_temp=Restaurante(self.id_restaurante)
            self.palabras_repetidas=obj_temp.palabrasRepetidas(lista_palabras)
        
        return self.palabras_repetidas
    

    def mirarComentarios(self):
        obj_temp=Restaurante(self.id_restaurante)
        return obj_temp.mirarComentarios()
