import sqlite3 as sql
import matplotlib.pyplot as plt
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from restaurante import *
from usuario import *



#Inicia coneccion con la bd
con=sql.connect("database.db")
cur=con.cursor()
        
class AdministradorLocal(Usuario):

    def __init__(self, id: str, apodo: str, nombre: str, id_restaurante:str, comentarios=...) -> None:
        super().__init__(id, apodo, nombre, comentarios)

        self.__id_restaurante:str=id_restaurante
        
        self.__palabras_repetidas:dict={}


    def agregarProducto(self,prod_nombre:str ,prod_precio:int ,prod_descripcion:str ,prod_alias:str)-> None:

        producto=(None,prod_nombre,self.__id_restaurante,prod_precio,prod_descripcion,prod_alias,)
        
        cur.execute("INSERT INTO productos VALUES(?,?,?,?,?,?)",producto)
        con.commit()
        print("Producto Agregado")
        
    
    def actualizarProducto(self,id:str,dato:str,cambio:str)-> None:
        
        cur.execute("SELECT * FROM productos WHERE id=? ",(f"{self.__id_restaurante}",))
        producto=cur.fetchone()

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
            cur.execute("UPDATE restaurante SET nombre=? WHERE id=?",(f"{cambio}",f"{self.__id_restaurante}",))
            con.commit()
        elif dato=="ubicacion":
            cur.execute("UPDATE restaurante SET ubicacion=? WHERE id=?",(f"{cambio}",f"{self.__id_restaurante}",))
            con.commit()
        elif dato=="horario":
            cur.execute("UPDATE restaurante SET horario=? WHERE id=?",(f"{cambio}",f"{self.__id_restaurante}",))
            con.commit()
    
    def mirarCalificacion(self):
        obj_temp=Restaurante(self.__id_restaurante)

        return obj_temp.mirarCalificacion()

    def graficarCalificacion(self):

        cur.execute(f"SELECT comentario,fecha FROM comentarios WHERE id_restaurante=?",(f"{self.__id_restaurante}",))
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
            obj_temp=Restaurante(self.__id_restaurante)
            self.__palabras_repetidas=obj_temp.palabrasRepetidas(lista_palabras)
        
        return self.__palabras_repetidas
    


    def palabrasRepetidas(self,lista_palabras:list) -> dict:
        
        cur.execute("SELECT no_stop_words FROM comentarios WHERE id_restaurante=?",(self.__id_restaurante))
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

                