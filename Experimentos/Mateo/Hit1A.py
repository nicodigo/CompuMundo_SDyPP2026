#DEO GLORIA

'''La letra b delante de un string en Python (b"texto") define un literal de bytes (bytes literal), 
creando un objeto bytes en lugar de una cadena Unicode (str) normal. 
Esto se utiliza para manipular datos binarios de bajo nivel (valores del 0 al 255), como archivos binarios o redes.'''

#Hecho con IA a fiens de prueba

import socket

def obtener_puerto():

    puerto = int(input("Ingrese el numero de puerto del servidor (2000 < puerto < 65000): "))

    while (puerto <= 2000 or puerto >= 65000):

        puerto = int(input("Ingrese el numero de puerto del servidor (2000 < puerto < 65000): "))

    return puerto

def proceso_cliente(puerto):

    # Crear socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectar al servidor
    server_address = ('localhost', puerto)
    client_socket.connect(server_address)

    try:
        # Enviar datos
        message = b"Hola CompuMundo, el cliente os saluda."
        client_socket.sendall(message)
        print("Mensaje enviado")
    finally:
        client_socket.close()

puerto = obtener_puerto()

proceso_cliente(puerto)