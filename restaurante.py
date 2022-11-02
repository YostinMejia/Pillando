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
    
    def __init__(self,id:str) -> None:
        
        self.id=str(id)

        #Se guardan los datos basicos que estan en la tabla restaurante
        cur.execute(f"SELECT * FROM restaurante WHERE id=?",(self.id,))
        datos=cur.fetchall()
        # print(datos)
        self.__nombre=datos[0][1]
        self.__ubicacion=datos[0][2]
        self.__calificacion=datos[0][3]
        self.__horario=datos[0][4]
            

    def mirarUbicacion(self):
        return self.__ubicacion
    
    def mirarHorario(self):
        return self.__horario


    def mirarCalificacion(self):
        return self.__calificacion


    def mirarComentarios(self)-> list:
        
        cur.execute("SELECT comentario,fecha FROM comentarios WHERE id_restaurante=?",(self.id,))
        lista_comentarios=cur.fetchall()

        return lista_comentarios


    #Se mira también la palabra más repetida 

    """Hay que mirar si quiere una cantidad minima de palabras"""
    
                