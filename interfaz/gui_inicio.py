# import sys
# from traceback import print_tb

# sys.path.insert(1,"C:\GitHub\Pillando\codigo")

# import administradores
# import usuario
# import restaurante

from tkinter import *
from PIL import ImageTk,Image
import pyglet

pyglet.font.add_file('interfaz\letra\GermaniaOneRegular.ttf')  

root=Tk()
root.title("  Usuario")
root.iconbitmap("interfaz\img\searching.ico")
root.geometry("1440x1024")
root["bg"]="white"

lbl_iniciar=Label(root,text="Iniciar Sesión", font=("Germania One",96), fg="#4C3572", bg="#FFFFFF")

img = ImageTk.PhotoImage(Image.open("interfaz\img\pillando.png"))
lbl_imagen=Label(root, image=img, bg="#FFFFFF")

lbl_usuario=Label(root,text="Usuario", font=("Germania One",48), fg="#4C3572", bg="#FFFFFF")
entry_usuario=Entry(root)

lbl_contrasena=Label(root,text="Contraseña", font=("Germania One",48), fg="#4C3572", bg="#FFFFFF")
entry_contrasena=Entry(root, width=50, bg="#D8D8D8")

# btn_confirmar=RoundedButton(root, width=30, height=15, cornerradius=40, fg="#4C3572", bg="#D8D8D8")

#btn_confirmar=Button(root, text="Enviar",  font=("Germania One",16), fg="#4C3572", bg="#FFFFFF")


lbl_olvcontrasena=Label(root, text="¿Has olvidado la contraseña?",font=("Germania One",20), fg="#000000", bg="#FFFFFF")
lbl_olvcontrasena2=Label(root, text="click aquí para recuperarla",font=("Germania One",20), fg="#000000", bg="#FFFFFF")

lbl_registrarse=Label(root, text="¿No tienes usuario?",font=("Germania One",20), fg="#000000", bg="#FFFFFF")
lbl_registrarse2=Label(root, text="click aquí para Registrarte",font=("Germania One",20), fg="#000000", bg="#FFFFFF")

# ---------------------- GRID -------------------------

lbl_iniciar.place(x=639, y=46)

lbl_imagen.place(x=178, y=300)

lbl_usuario.place(x=783, y=252)
entry_usuario.place(x=783, y=335)
entry_usuario.insert(0,"Ingrese su usuario")

lbl_contrasena.place(x=783, y=476)
entry_contrasena.place(x=783, y=556)
entry_contrasena.insert(0,"Ingrese su usuario")

# btn_confirmar.place(x=893 , y=600)

lbl_olvcontrasena.place(x=783 ,y=691)
lbl_olvcontrasena2.place(x=783 ,y=727)

lbl_registrarse.place(x=150 ,y=691)
lbl_registrarse2.place(x=139 ,y=727)


# entry=Entry(root, width=50, borderwidth=2 )
# entry.insert(0,"escriba")

# def mostrar():
#     print(entry.get())



# btn1=Button(root, text="pulse", command= lambda: mostrar(), padx=60, fg="white", bg="green" )
# btnCerrar(root, text="Close", command=root.quit)


root.mainloop()
