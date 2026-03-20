# DEO GLORIA

import socket


def obtener_puerto():

    puerto = int(input("Ingrese el numero de puerto del servidor (2000 < puerto < 65000): "))

    while (puerto <= 2000 or puerto >= 65000):

        puerto = int(input("Ingrese el numero de puerto del servidor (2000 < puerto < 65000): "))

    return puerto


def decidir_reconexion(client_socket):
    client_socket.close()

    conectar = input("La conexion termino ¿Quiere intertar reconectarse? (s/n): ")

    while ((conectar != 's') and (conectar != 'n')):
        print("Ingrese valores válidos.")
        conectar = input("La conexion termino ¿Quiere intertar reconectarse? (s/n): ")

    if (conectar == 's'):
        proceso_cliente(obtener_puerto())
    else:
        print("El programa termino, saludos.")


def proceso_cliente(puerto):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_address = ('localhost', puerto)
        client_socket.connect(server_address)
        print("Conectado al servidor")

        message = b"Hola CompuMundo, el cliente os saluda."
        client_socket.sendall(message)

    except BrokenPipeError:
        print("Error: El servidor no mantuvo la conexión.")

    # Este es el except requerido para cumplir por lo pedido en el HIT 2
    except ConnectionRefusedError:
        print("Error: El servidor rechazó la conexión.")

    except ConnectionResetError:
        print("Error: El servidor reseteó la conexión.")

    except ConnectionAbortedError:
        print("Error: El software del equipo host destruyó la conexión.")

    except Exception as e:
        print(f"Error inesperado: {e}")

    finally:
        decidir_reconexion(client_socket)


puerto = obtener_puerto()


proceso_cliente(puerto)
