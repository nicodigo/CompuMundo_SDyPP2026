#DEO GLORIA

'''La letra b delante de un string en Python (b"texto") define un literal de bytes (bytes literal), 
creando un objeto bytes en lugar de una cadena Unicode (str) normal. 
Esto se utiliza para manipular datos binarios de bajo nivel (valores del 0 al 255), como archivos binarios o redes.'''


import socket
import sys


MAX_PORT = 65000
MIN_PORT = 2000


def obtener_puerto():
    puerto = 0

    while (puerto <= 2000 or puerto >= 65000):
        try:
            puerto = int(input("Ingrese el numero de puerto del servidor (2000 < puerto < 65000): "))
        except ValueError:
            print("Advertencia: el puerto debe ser un numero entero")

    return puerto


def puerto_valido(puerto: int) -> bool:
    if (puerto <= MIN_PORT or puerto >= MAX_PORT):
        return False

    return True



def enviar_mensaje(puerto: int, mensaje: str):
    # Crear socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conectar al servidor
        server_address = ('localhost', puerto)
        client_socket.connect(server_address)

        # Enviar datos
        client_socket.sendall(mensaje.encode("utf-8"))

    except ConnectionRefusedError:
        print("Hubo un error al conectar al servidor, asegurate que este corriendo")
        sys.exit(1)

    finally:
        client_socket.close()


def main():
    argc = len(sys.argv)
    if (argc != 3):
        print("Error: El comando esperado contiene numero de puerto y mensaje")
        print("Ejemplo: 55555 \"Hola mundo\"")
        sys.exit(1)

    try:
        puerto = int(sys.argv[1])
    except ValueError:
        print("Error: El puerto debe ser un entero")
        sys.exit(1)

    if not (puerto_valido(puerto)):
        print("Error: Rango de puertos permitidos = ", MIN_PORT, " - ", MAX_PORT)
        sys.exit(1)

    mensaje = sys.argv[2].strip()
    if not mensaje:
        print("Error: El mensaje no puede estar vacio")
        sys.exit(1)

    enviar_mensaje(puerto, mensaje)
    print("Mensaje enviado")
    sys.exit(0)


main()
