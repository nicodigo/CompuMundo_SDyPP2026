#DEO GLORIA

import socket

def obtener_puerto():

    puerto = int(input("Ingrese el numero de puerto a utilizar (2000 < puerto < 65000): "))

    while (puerto <= 2000 or puerto >= 65000):

        puerto = int(input("Ingrese el numero de puerto a utilizar (2000 < puerto < 65000): "))

    return puerto

def proceso_servidor(puerto):

    # Crear socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enlazar el socket a la dirección y puerto
    server_address = ('localhost', puerto)
    server_socket.bind(server_address)

    # Escuchar conexiones entrantes
    server_socket.listen(1)
    print("Esperando conexión...")

    # Aceptar conexión
    connection, client_address = server_socket.accept()
    try:
        print(f"Conexión recibida de {client_address}")
        # Recibir datos
        data = connection.recv(1024)
        print(f"Recibido: {data.decode()}")
    finally:
        connection.close()


puerto = obtener_puerto()

proceso_servidor(puerto)