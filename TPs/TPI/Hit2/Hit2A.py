#DEO GLORIA

import socket

def obtener_puerto():

    puerto = int(input("Ingrese el numero de puerto del servidor (2000 < puerto < 65000): "))

    while (puerto <= 2000 or puerto >= 65000):

        puerto = int(input("Ingrese el numero de puerto del servidor (2000 < puerto < 65000): "))

    return puerto

def decidir_reconexion(client_socket):
    
    client_socket.close()

    conectar = input("La conexion termino ¿Quiere intertar reconectarse? (s/n): ")

    while((conectar != 's') and (conectar != 'n')):
        print("Ingrese valores válidos.")
        conectar = input("La conexion termino ¿Quiere intertar reconectarse? (s/n): ")

    if(conectar == 's'):
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
    
    #Este es el except requerido para cumplir por lo pedido en el HIT 2
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






''' Idea de la IA
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 5000))
        print("Conectado al servidor")

        while True:
            # Intentar recibir datos
            data = client_socket.recv(1024)
            
            if not data:
                # Si recv devuelve 0 bytes, el servidor cerró la conexión
                print("El servidor ha cerrado la conexión (EOF).")
                break
            
            print(f"Recibido: {data.decode('utf-8')}")

    except ConnectionResetError:
        print("Error: Conexión forzada por el servidor (se cayó).")
    except ConnectionAbortedError:
        print("Error: Conexión abortada por el software en el equipo host.")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        client_socket.close()
        print("Socket cerrado.")


# Modificación propia

    intentos = 10

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while(intentos > 0):
    
        try:
            server_address = ('localhost', puerto)
            client_socket.connect(server_address)
            print("Conectado al servidor")

            message = b"Hola CompuMundo, el cliente os saluda."
            client_socket.sendall(message)

            
            data = client_socket.recv(1024)
            
            if not data:
                # Si recv devuelve 0 bytes, el servidor cerró la conexión
                print("El servidor ha cerrado la conexión (EOF).")
            
            print(f"Recibido: {data.decode('utf-8')}")
            


        #Este es el except requerido para cumplir por lo pedido en el HIT 2
        except BrokenPipeError:
            print("Error: El servidor no mantuvo la conexión.")    

        except ConnectionRefusedError:
            print("Error: El servidor rechazó la conexión.")
        
        except ConnectionResetError:
            print("Error: El servidor reseteó la conexión.")

        except ConnectionAbortedError:
            print("Error: El software del equipo host destruyó la conexión.")

        except Exception as e:
            print(f"Error inesperado: {e}")

        finally:
            client_socket.close()
            print("Socket cerrado.")



'''