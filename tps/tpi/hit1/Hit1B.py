# DEO GLORIA

import socket
import sys


MAX_PORT = 65000
MIN_PORT = 2000


def obtener_puerto():
    puerto = int(input("Ingrese el numero de puerto a utilizar (2000 < puerto < 65000): "))

    while (puerto <= 2000 or puerto >= 65000):

        puerto = int(input("Ingrese el numero de puerto a utilizar (2000 < puerto < 65000): "))

    return puerto


def puerto_valido(puerto: int) -> bool:
    if (puerto <= MIN_PORT or puerto >= MAX_PORT):
        return False

    return True


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


def main():
    argc = len(sys.argv)
    if (argc != 2):
        print("Error: El comando esperado contiene numero de puerto ")
        print("Ejemplo: 55555 ")
        sys.exit(1)

    try:
        puerto = int(sys.argv[1])
    except ValueError:
        print("Error: El puerto debe ser un entero")
        sys.exit(1)

    if not (puerto_valido(puerto)):
        print("Error: Rango de puertos permitidos = ", MIN_PORT, " - ", MAX_PORT)
        sys.exit(1)

    proceso_servidor(puerto)


main()