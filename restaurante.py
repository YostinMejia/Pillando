import sqlite3 as sql
import re

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
    
                