import imp
import sqlite3 as sql

con=sql.connect("database.db")
cur=con.cursor()

def dbRestaurante(restaurante):   
    #qmark style 
    cur.executemany("INSERT INTO restaurante VALUES(?,?,?,?,?,?,?)",restaurante)
    con.commit()
    con.close()

def dbProductos(productos):
    #qmark style
    cur.executemany("INSERT INTO productos VALUES(?,?,?,?,?,?)",productos)
    con.commit()
    cur.close()

def dbComentarios(comentario):
    #qmark style
    cur.executemany("INSERT INTO comentarios VALUES(?,?,?,?)",comentario)
    con.commit()
    cur.close()

#Ingresan comentarios
# dbComentarios(comentario=[
#     (None,"1","	El menú excelente y barato! 100% recomendable,el servicio rápido la gente amable y la comida exquisita! El secreto está increíble !!!","11/08/2022"),
#     (None,"1","Trato agradable, lo hemos visitado una sola vez y volveremos a repetir en breve, carrillada exquisita. Carta muy apetitosa. Para la próxima probaremos más cosas. Saludos","13/08/2022"),
#     (None,"1","	Estuvimos en este restaurante para celebrar en familia una graduación. Comida exquisita, recomiendo las croquetas de rabo de toro con chocolate y el salmorejo. Lo único malo es que la sala donde estuvimos estaba demasiado llena y estuvimos un poco apretados. Personal muy atento.","14/08/2022"),
#     (None,"1","	Restaurante tradicional y familiar. Alimentos de primera acompañados de un trato excelente. Recomendable las quisquillas de Motril, las mejores que probé nunca. Un acierto seguro.","15/08/2022"),
#     (None,"1","	Iba de chica con mis padres y voy ahora con mi hijo, nos gusta ir y picotear en la barra, los boquerones buenísimos, ni en los restaurantes de pescado de Granada los he probado así de ricos y el trato del personal es buenísimo.","15/08/2022"),
#     (None,"2","Cocina andaluza, Materia prima de calidad, servicio rápido y amable. Tiene menús de todos los precios y para todos los gustos, cabe destacar los menús anticrisis, de unos 30€ y de gran calidad y cantidad. los de degustación, a muy buen precio.","16/08/2022"),
#     (None,"2","	Quisquillas, jamón, boquerones y todos los segundos excepcionales por no hablar del trato recibido. Un diez como la copa de un pino.","22/08/2022"),
#     (None,"2","Fuimos por recomendación a este restaurante, nos habian hablado muy bien de el y las expectativas eran altas y las cumplieron de sobra. Camareros atentos, amables y simpaticos. La comida muy rica toda, sin duda de los mejores sitios de Granada para comer ( en mi caso fue cena ). Ir aqui es acertar seguro.","01/08/2022"),
#     (None,"2","Un buen restaurante con una magnífica cocina y un personal profesional, agradable y atento. Buenísimas las quisquillas de motril, las carnes y un magnífico lomo de bacalao.","09/08/2022"),
#     (None,"2","	La comida es muy buena. Se nota que utilizan productos de calidad. El personal atento y profesional. Yo lo recomiendo.","21/08/2022"),
#     (None,"3","	Me sorprendió porque su materia prima es excelente, el servicio muy bueno, el ambiente clásico. Es un restaurante de siempre donde no sales defraudado.","21/08/2022"),
#     (None,"3","Un sitio perfecto para comer en familia, en pareja o en reuniones. Los vinos excelentes al igual que el trato humano. Una experiencia muy buena. Lo recomiendo sin duda alguna.","15/08/2022"),
#     (None,"3","Fui con mis padres y sus amigos, durante una visita a Granada; todo el mundo lo pasamos de maravilla y una increíble comida! El personal fue muy amable. Recomiendo encarecidamente este lugar.","29/08/2022"),
#     (None,"3","Sólo tuvimos tiempo para un almuerzo, pero me hubiera gustado tener una cena allí también. Cada uno tenía un plato de especialidades que era excelente y el camarero fue muy atento con nosotros para que nos sintiéramos bienvenidos.","11/08/2022"),
#     (None,"4","	Estupendas tapas! Han ganado varios premios para su comida. Hay cartas del Rey Juan Carlos y su padre el antiguo rey en la pared dándoles las gracias por sus comidas. Tapas de berenjena son geniales y hasta sus postres son para morirse aunque puede que no tengan espacio para ellos. Me encanta este lugar!","12/08/2022"),
#     (None,"4","El servicio es excelente y el jamón es muy recomendable. Muy buenos los camareros y el personal del restaurante.","14/08/2022"),
#     (None,"4","	Slow food cocina española en todo su esplendor. El restaurante tiene aspecto clásico. Los camareros saben cómo servir. Este es el lugar para los verdaderos amantes de la comida clásica de la península ibérica.","13/08/2022"),
#     (None,"4","	Teníamos una deliciosa comida de carne, vino tinto y pimienta, queso y ensalada de aguacate Montefrio con paté todo por 62 euros para dos personas. Compartimos el entrante y el plato principal, que era más que suficiente. Nuestro camarero era excelente y atento, y recomendamos encarecidamente una cena aquí, recomendado por el personal de nuestro hotel.","15/08/2022"),
#     (None,"4","	Éramos los únicos ingleses en el lugar. Comimos en el bar ... era genial ... así que regresamos por segunda vez. ","16/08/2022"),
#     (None,"5","No sé cómo sigue abierto este lugar, no sé si los administrados de TripAdvisor o el ayuntamiento de comillas nos ayudará a cerrar este lugar la verdad es que es un asco de lugar ","04/08/2022"),
#     (None,"5","Cada plato del menú de degustación estaba o muy salado, o muy agrio o era muy raro.","05/08/2022"),
#     (None,"5","La atención excelente, tomamos unas tapas y nos atendieron con todo detalle. La calidad y presentación muy recomendables. Vale la pena ir y no es caro para lo que ponen.","02/08/2022"),
#     (None,"5","Todo un referente en Granada. Goza de una clientela fiel y es lugar de visita obligada. Sus paredes están cubiertas de fotos con todo tipo de personajes: artistas, toreros, políticos...","03/08/2022"),
#     (None,"5","Estuve cenando con mi pareja, y la experiencia estuvo a la altura de las expectativas. El servicio fue muy correcto, la chica que nos atendió amabilísima y simpática. La comida fue espectacular, yo tomé pescado que estaba jugosísimo y mi pareja carne, que parecía mantequilla. Un lujazo de cena. Me alegro mucho de haber repetido... lo haremos de nuevo.","06/08/2022"),
#     (None,"5","Cada plato del menú daba para cuatro bocados, lo que estaría bien si la comida supiera genial, pero esta comida en concreto NO lo hacía.","03/08/2022"),
#     (None,"6","Por desgracia, el servicio era deficiente y muy pretencioso.","11/08/2022"),
#     (None,"6","El sitio no es barato, pero la calidad en el servicio y la de la comida es espectacular... un restaurante de los buenos buenos de verdad.","11/08/2022"),
#     (None,"6"," Nosotros no fuimos los únicos reaccionando con expresiones de disgusto al probar los platillos, las personas en las otras mesas se veían decepcionadas y asqueadas con la comida. Mi esposa incluso se enfermó del estómago después de cenar. (...) Nunca pensamos que alguien pudiera preparar tan horrible el foie o el venado. (...) No hay que confundir un estilo novedoso con algo raro y repugnante","11/08/2022"),
#     (None,"6","La comida es tan mala que no merece el esfuerzo de escribir una reseña detallada. Sus trucos son ridículos","11/08/2022"),
#     (None,"6","El departamento más talentoso de este sitio es el departamento de marketing. (...) Cada parte del menú [de 14 platos] tenía una introducción que duraba más que lo que tardabas en comerlo. Nos sirvieron una porción mínima de cerdo (que estaba delicioso) y, cuando preguntamos donde estaba el resto, nos sirvieron una segunda porción hecha por entero con grasa de cerdo. Fue muy insultante","11/08/2022"),
#     ])


#Se ingresan restaurantes
# dbRestaurante(restaurante=[
#     #id nombre productos ubicacion calificacion horario comentarios  
#     (None,"Don Beto","","bloque 12",0,"6am a 8pm",""),
#     (None,"La Panaderia Miguel","","bloque 4",0,"7am a 9pm",""),
#     (None,"Pregunte por lo que no vea","","bloque 4",0,"6am a 8pm",""),
#     (None,"Abarrotes Don José","","bloque 4",0,"6am a 8pm",""),
#     (None,"La Providencia","","bloque 12",0,"8am a 3pm",""),
#     (None,"La Esquina","","bloque 4",0,"6am a 2pm",""),

# ])

#Se ingresan productos
# dbProductos(productos=[
#     #id nombre id_restaurante precio descripcion(opcional) alias(si tiene algun nombre propio del local)
#     (None,"salchipapa","1",12000,None,None),
#     (None,"salchipapa con pollo","2",13000,"vienen con pollo molido y caviar",None),
#     (None,"salchipapa con chicharron","5",8000,"traen chicharron y pan","pepa"),
#     (None,"perro","6",17000,"trae arroz cubano","jbalvin"),
#     (None,"perro","1",13123,None,None),
#     (None,"hamburguesa","3",13123,None,None),
#     (None,"hamburguesa","4",13123,"trae carne de bufalo","buffalo soldier")

# ])


from textblob import TextBlob
import re
from unicodedata import normalize
import matplotlib.pyplot as mtp

#Limpia el str antes de hacer un select a la bd
def limpiarStr(palabra):
    # -> NFD y eliminar diacríticos
    palabra = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", palabra), 0, re.I)
    palabra=re.sub("[^\w\s]","",palabra)
    palabra=re.sub("[0-9_]","",palabra)
    # -> NFC
    palabra= normalize( 'NFC', palabra)
    return palabra

#Se busca el producto
def buscarProducto(producto):

    producto=limpiarStr(producto)

#hay que mirar si el restarurante está abierto---------

    if len(producto)>=3:

        cur.execute("SELECT * FROM productos WHERE nombre LIKE ?",(f"{producto}%",))
        lista_productos=cur.fetchall()

        if len(lista_productos)==0:

            print(f"{producto} no se encuntra disponible")
            print("Ingrese un producto valido")
            #Llamamos la misma funcion
            producto=limpiarStr(input("-> "))
            buscarProducto(producto)
            
        else:
            temp=producto[0:len(producto)//2]
            cur.execute("SELECT * FROM productos WHERE nombre LIKE ?",(f"{temp}%",))
            productos=cur.fetchall()
            print(productos)

    else:
        print(f"{producto} no se encuntra disponible")
        print("Ingrese un producto valido")
        #Llamamos la misma funcion
        producto=limpiarStr(input("-> "))
        buscarProducto(producto)

#El usuario puede crear un objeto restaurante y este se puede almacenar en un json para no repetirlo
class Restaurante:

    def __init__(self,id:str) -> None:
        self.id=str(id)

        #Se guardan los datos basicos que estan en la tabla restaurante
        cur.execute(f"SELECT * FROM restaurante WHERE id=?",(f"{self.id}",))
        datos=cur.fetchall()
        # if datos==[]:
        #     print("El nombre no es válido \n Ingrese uno valido")
        #     self.id=input("->: ")
        #     don_beto=Restaurante(self.id)
        
        self.nombre=datos[0][1]
        self.ubicacion=datos[0][3]
        self.horario=datos[0][4]

        #Se guardan los productos de la tabla productos
        cur.execute(f"SELECT * FROM productos WHERE id_restaurante=?",(f"{self.id}",))
        productos=cur.fetchall()
        self.productos=productos
            
        #Se guardan los comentarios
        cur.execute(f"SELECT comentario,fecha FROM comentarios WHERE id_restaurante=?",(f"{self.id}",))
        comentarios=cur.fetchall()
        self.comentarios=comentarios

        #Luego cuando el usuario quiera ver la calificacion se otorga la calificacion
        self.calificacion=0
        
    def buscarProducto(self):
        pass

    def mirarUbicacion(self):
        cur.execute("SELECT ubicacion FROM restaurante")
        ubicacion=cur.fetchone()
        print(f" {self.nombre} queda en el {ubicacion[0]}")
    
    def mirarHorario(self):
        cur.execute("SELECT horario FROM restaurante")
        horario=cur.fetchone()
        print(f"{self.nombre} tiene un horario de {horario[0]}")

    def mirarCalificacion(self):
        
        cur.execute(f"SELECT comentario,fecha FROM comentarios WHERE id_restaurante=?",(f"{self.id}",))
        comentarios=cur.fetchall()
        self.comentarios=comentarios
        
        #Graficar la calificacion por medio de fechas
        #utilizar el analisis de sentimientos

    def mirarComentarios(self):
        
        cur.execute("SELECT comentario,fecha FROM comentarios WHERE id_restaurante=?",(f"{self.id}",))
        lista_comentarios=cur.fetchall()

        if lista_comentarios==[]:
            print("No hay comentarios")
        else:
            self.comentarios=lista_comentarios
            for i in lista_comentarios:
                print(i[0],f"Publicado el {i[1]}\n")

        
don_beto=Restaurante("1")


class Usuario:
    def __init__(self,id,apodo) -> None:
        self.id=id
        self.apodo=apodo
    
    def enviarComentario(self,restaurante:str,comentario:str):
        pass

    def infoRestaurante(self,restaurante:Restaurante):
        pass
    
    

#mejor guardar las palabar en plurar para evitar errores en la busqueda



# class Usuario:
#     def __init__(self,id:str,apodo:str,) -> None:
#         self.id=id
#         self.apodo=apodo
    
