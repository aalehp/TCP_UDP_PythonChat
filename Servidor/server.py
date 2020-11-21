from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
from threading import Thread
import json
import time
import sys
import pickle

def aceptarConexionesTCP():
    while True:
        client, client_address = TCPSERVER.accept()
        print("Un nuevo cliente se ha conectado con",client_address)
        salida = 'Inicia sesion o registrate para chatear'
        listaSalida = salida
        client.send(bytes(json.dumps(listaSalida), "utf8"))
        direcciones[client] = client_address
        Thread(target=manejarClienteTCP, args=(client,)).start()


def manejarClienteTCP(client):

    listaEntrada = json.loads(client.recv(Buffer).decode("utf8"))
    name = listaEntrada[1]
    print(name)

    if listaEntrada[0] == 'Login':
        while True:
            if iniciarSesion(listaEntrada[1],listaEntrada[2]) == False:
                salida = 'ERROR: No existe usuario o contraseña incorrecta, intente de nuevo'
                listaSalida = salida
                client.send(bytes(json.dumps(listaSalida), "utf8"))
                listaEntrada = json.loads(client.recv(Buffer).decode("utf8"))
            else:
                break
    if listaEntrada[0] == 'Register':
        while True:
            if registrar(listaEntrada[1]) == True:
                salida = 'ERROR: Ya existe usuario, intente de nuevo'
                listaSalida = salida
                client.send(bytes(json.dumps(listaSalida), "utf8"))
                listaEntrada = json.loads(client.recv(Buffer).decode("utf8"))
            else:
                break
    name = listaEntrada[1]
    usuarios[listaEntrada[1]]=listaEntrada[2]
    puertos[listaEntrada[1]]=listaEntrada[3]
    
    guardarDatos() 
    welcome = 'Selecciona a quien enviar y que método. Bienvenido'
    listaSalida=welcome
    client.send(bytes(json.dumps(listaSalida), "utf8"))

    
    msg = 'Un nuevo usuario se ha conectado, checar abajo'
    listaSalida=msg

    direccionClientes[name] = direcciones[client]
    
    broadcast(listaSalida)
    clientes[client] = name


    while True:
        
        msg = client.recv(Buffer)
        listaEntrada = json.loads(msg)

        if listaEntrada[0] == 'Enviar a':
            enviarTCP(listaEntrada,listaEntrada[1])

        if listaEntrada[0] == '*Salir*':
            listaSalida = 'Un usuario ha dejado el chat, checar abajo'
            del clientes[client]
            del direccionClientes[name]
            broadcast(listaSalida)
            break

def enviarTCP(lista,name):
    for sock in clientes:
        print(clientes[sock])
        if name == clientes[sock]:
            sock.send(bytes(json.dumps(lista), "utf8"))

def broadcast(listaSalida):
    for sock in clientes:
        sock.send(bytes(json.dumps(listaSalida), "utf8"))
        
def conectados():
    i=0
    while True:
        time.sleep(1)
        for sock in clientes:
            sock.send(bytes(json.dumps(direccionClientes), "utf8"))

def registrar(usuario):
    if usuario in usuarios:
        return True
    else:
        return False
def iniciarSesion(usuario, contraseña):
    if usuario in usuarios:
        if usuarios[usuario] == contraseña:
            return True
        else:
            return False
    else:
        return False

def manejarClientesUDP():
    while True:
        data, addr = UDPSERVER.recvfrom(Buffer) 
        listaEntrada = json.loads(data)
        enviarUDP(listaEntrada, listaEntrada[1])

def enviarUDP(listaSalida, name):
    UDPSERVER.sendto( bytes( json.dumps (listaSalida) ,"utf-8"), (direccionClientes[name][0], puertos[name]))
    
    
def cargarDatos():
    with open('usuarios.txt', 'r') as f:
        return json.load(f)
        
def guardarDatos():
    with open('usuarios.txt', 'w') as f:
        json.dump(usuarios, f)
        

def salir():
    sys.exit()


clientes = {}
direcciones = {}
direccionClientes = {}
usuarios = cargarDatos()
puertos = {}

HOST = '192.168.100.106'

TCPPORT = 22222
UDPPORTSERVER = 33333

Buffer = 1024

direccion = (HOST, TCPPORT)
TCPSERVER = socket(AF_INET, SOCK_STREAM)
TCPSERVER.bind(direccion)

direccion = (HOST, UDPPORTSERVER)
UDPSERVER = socket(AF_INET, SOCK_DGRAM)
UDPSERVER.bind(direccion)

if __name__ == "__main__":
    
    TCPSERVER.listen(5)
    
    print("Esperando conexiones")
    
    aceptarTCPHilo = Thread(target=aceptarConexionesTCP)
    conectadosHilo = Thread(target=conectados)
    manejarUDPHilo = Thread(target=manejarClientesUDP)
    
    aceptarTCPHilo.start()
    conectadosHilo.start()
    manejarUDPHilo.start()
    
    aceptarTCPHilo.join()
    
    TCPSERVER.close()
    UDPSERVER.close()
