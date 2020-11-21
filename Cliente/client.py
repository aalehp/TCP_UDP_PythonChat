from socket import AF_INET, socket, SOCK_STREAM,SOCK_DGRAM
from threading import Thread 
import tkinter as tk
import tkinter
from tkinter import font
import tkinter.font as tkFont
from tkinter.constants import END, FALSE
import tkinter.ttk
import json
import time
import random
import sys
from tkinter.ttk import Label


def center(toplevel): 
    toplevel.update_idletasks() 
    w = toplevel.winfo_screenwidth() 
    h = toplevel.winfo_screenheight() 
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x')) 
    x = w/2 - size[0]/2 
    y = h/2 - size[1]/2 
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y))) 


def ocultar():
    botonIN.place_forget()
    botonRG.place_forget()
    usrtxt.place_forget()
    contratxt.place_forget()
    l1.place_forget()
    l2.place_forget()
    botonSal.pack_forget()

def iniciado():
    l3 =tk.Label(ventana, text="Protocolo: ",font=fontStyle ,bg="blue", fg="white")
    l3.place(x=40, y=20)
    RBTCP.place(x=150, y=25)
    RBTCP.configure(bg="blue", fg="black")
    RBUDP.place(x=220, y=25)
    RBUDP.configure(bg="blue", fg="black")

    l4 =tk.Label(ventana, text="Usuarios: ",font=fontStyle ,bg="blue", fg="white")
    l4.place(x=360, y=20)
    
    l5 =tk.Label(ventana, text='Bienvenido ' + usr.get() + " Puerto:" + str(UDPPORTCLIENTE) + " IP:" + MIIP ,font=fontStyle ,bg="blue", fg="white")
    l5.place(x=40, y=50)

    listaUsr.place(x=450, y=25, width=250)
    botonSal.place(x=750, y=20, width=200)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    listaMsgs.pack(fill=tk.X)
    ventMsg.place(x=10, y=80, height=500,width=980)

    textoMsg.place(x=10, y=600, width=800, height=50)
    botonEN.place(x=830, y=600, width=150, height=50)
    botonEN.configure(bg="Green", fg="white")
    ventana.resizable(0,0)

def recibirTCP():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            chat = json.loads(msg)
            if type(chat) is dict:
                conectados = chat.copy()
                listaUsr['values'] = list(conectados.keys())
            else:
                if 'Selecciona a quien enviar y que método. Bienvenido' == chat:
                    ocultar()
                    iniciado()
                    ventana.geometry("1000x700")
                    center(ventana)

                    chat = 'Selecciona a quien enviar y que método. Bienvenido ' + usr.get()+"."
                    listaMsgs.insert(tkinter.END, chat)
                if 'Inicia sesion o registrate para chatear' == chat:
                    listaMsgs.insert(tkinter.END, chat)
                if 'ERROR: Ya existe usuario, intente de nuevo' == chat:
                    listaMsgs.insert(tkinter.END, chat)
                if 'ERROR: No existe usuario o contraseña incorrecta, intente de nuevo' == chat:
                    listaMsgs.insert(tkinter.END, chat)
                if chat == 'Un nuevo usuario se ha conectado, checar abajo':
                    listaMsgs.insert(tkinter.END, chat)
                if chat == 'Un usuario ha dejado el chat, checar abajo':
                    listaMsgs.insert(tkinter.END, chat)
                if chat[0] == 'Enviar a':
                    string = chat[2] +" : "+chat[3]
                    listaMsgs.insert(tkinter.END, string)
        except OSError: 
            break

def recibirUDP():
    while True:
        data, direccion = UDPSERVER.recvfrom(BUFSIZ)
        chat = json.loads(data)
        string = chat[2] +" : "+chat[3]
        listaMsgs.insert(tkinter.END, string)


#Funciones de Botones

def enviar(event=None):
    msg = msgToEnviar.get()
    listaMsgs.insert(tkinter.END, usr.get()+"(YO) : "+msg)
    listaSalida = ['Enviar a',listaUsr.get(),usr.get(),msg]
    msgToEnviar.set("")
    if protocolos.get() == 1:
        client_socket.send(bytes(json.dumps(listaSalida), "utf8"))
    else:
        UDPSERVER.sendto( bytes( json.dumps (listaSalida) ,"utf-8"), (HOST, UDPPORTSERVER))
        
def iniciar():
    miNombre=usr.get()
    listaSalida = ['Login',usr.get(), contra.get(),UDPPORTCLIENTE]
    client_socket.send(bytes(json.dumps(listaSalida), "utf8"))
    listaMsgs.delete(0,END)
    
def registrar():
    miNombre=usr.get()
    listaSalida = ['Register',usr.get(), contra.get(),UDPPORTCLIENTE]
    client_socket.send(bytes(json.dumps(listaSalida), "utf8"))
    listaMsgs.delete(0,END)
    
def salir(event=None):
    listaSalida = ['*Salir*',usr.get()]
    client_socket.send(bytes(json.dumps(listaSalida), "utf8"))
    ventana.destroy()
    

ventana = tkinter.Tk()
ventana.title("Actividad 11 S.O. I")
ventana.configure(background="blue")
ventana.geometry("250x375")

ventMsg = tkinter.Frame(ventana)
msgToEnviar = tkinter.StringVar()
msgToEnviar.set("")
usr = tkinter.StringVar()
usr.set("aw")
contra = tkinter.StringVar()  
contra.set("1234")

scrollbar = tkinter.Scrollbar(ventMsg)
listaMsgs = tkinter.Listbox(ventMsg, height=30, width=80, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
listaMsgs.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
listaMsgs.pack(side="right")
ventMsg.pack(side="right",padx=10, pady=10)

scrollbar.pack_forget()
listaMsgs.pack_forget()
ventMsg.pack_forget()

fontStyle = tkFont.Font(family="Arial", size=15)

l1 =tk.Label(ventana, text="Nombre Ususario",font=fontStyle ,bg="blue", fg="white")
l1.place(x=40, y=80)

usrtxt = tkinter.Entry(ventana, textvariable=usr)
usrtxt.bind("<Return>", iniciar, registrar)
usrtxt.pack()
usrtxt.place(x=40, y=110)

l2 =tk.Label(ventana, text="Contraseña",font=fontStyle, bg="blue", fg="white")
l2.place(x=70, y=150)

contratxt = tkinter.Entry(ventana, textvariable=contra)
contratxt.bind("<Return>", iniciar, registrar)
contratxt.pack()
contratxt.place(x=40, y=180)

botonIN = tkinter.Button(ventana, text="Login", command=iniciar)
botonIN.pack(padx=10, pady=10)
botonIN.place(x=40, y=250)

botonRG = tkinter.Button(ventana, text="Register", command=registrar)
botonRG.pack(padx=0, pady=10)
botonRG.place(x=120, y=250)

botonSal = tkinter.Button(ventana, text="Salir", command=salir, bg="Red", fg="white")
botonSal.pack(padx=10, pady=10, side=tkinter.BOTTOM, fill=tk.X)



textoMsg = tkinter.Entry(ventana, textvariable=msgToEnviar)
textoMsg.bind("<Return>", enviar)

botonEN = tkinter.Button(ventana, text="Enviar", command=enviar)

listaUsr = tkinter.ttk.Combobox(ventana)

protocolos = tkinter.IntVar(value=1)

RBTCP = tkinter.Radiobutton(ventana, text="TCP", state="normal", value="1", variable=protocolos)
RBUDP = tkinter.Radiobutton(ventana, text="UDP", state="normal",value="2", variable=protocolos)


ventana.protocol("WM_DELETE_WINDOW", salir)

HOST = '192.168.100.106'
MIIP = '192.168.100.106'
TCPPORT = 22222
UDPPORTSERVER = 33333

UDPPORTCLIENTE = random.randint(10000,60000)

BUFSIZ = 1024

ADDR = (HOST, TCPPORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

ADDR = (MIIP, UDPPORTCLIENTE)
UDPSERVER = socket(AF_INET, SOCK_DGRAM)
UDPSERVER.bind(ADDR)

conectados = {}

recibirTCPHilo = Thread(target=recibirTCP)
recibirUDPHilo = Thread(target=recibirUDP)

recibirTCPHilo.start()
recibirUDPHilo.start()

tkinter.mainloop()  