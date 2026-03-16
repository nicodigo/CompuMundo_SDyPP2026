#DEO GLORIA

import sys
import threading
import socket
from typing import Tuple

def parsear_direccion(addr: str) -> Tuple[str, int]:
    """
    Puede ocasionar una excepcion 
    ValueError
    si la cadena no es la esperada, por ejemplo si el puerto no puede convertirse a entero
    """
    host, puerto = addr.split(":")
    return host, int(puerto)


def crear_socket_servidor(host: str, puerto: int) -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, puerto))
    s.listen()
    return s

def crear_socket_cliente() -> socket.socket:
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def enviar_mensaje(sock: socket.socket, msj: str) -> None:
    sock.sendall(msj.encode("utf-8"))


def recibir_mensaje(sock: socket.socket, size=1024) -> str:
    datos = sock.recv(size)
    return datos.decode("utf-8")

#---------------------------------------------------------------------------


def servicio_cliente(host_remoto: str, puerto_remoto: int) -> None:
    while True:
        s_cliente= crear_socket_cliente()
        try:
            s_cliente.connect((host_remoto, puerto_remoto))
        except Exception:
            print(f"{host_remoto}:{puerto_remoto} no responde")
            print("Verifique su conexion y si el servidor esta corriendo")

            opcion = ""
            while (opcion != "r") and (opcion != "s"):
                opcion = input("Ingrese r para reconectar o s para salir\n").strip()

            match opcion:
                case "r":
                    s_cliente = crear_socket_cliente()
                    continue
                case "s":
                    break

        try:
            while True:
                msj = input("").strip()
                if msj == "s":
                    s_cliente.close()
                    print("conexion con el servidor cerrada")
                    return
                if msj:
                    enviar_mensaje(s_cliente, msj)
                else: continue
        except: print("Fallo al enviar el mensaje, intentando reconexion...")
        finally: s_cliente.close()


def escuchar(c: socket.socket, a: Tuple[str, int]) -> None:
    try:
        msj = recibir_mensaje(c)
        while msj:
            print(f"({a[0]}:{a[1]}): {msj}")
            msj = recibir_mensaje(c)
    finally:
        c.close()


def servicio_servidor(s_servidor: socket.socket) -> None:
    while True:
        cliente, addr = s_servidor.accept()
        print(f"{addr[0]}:{addr[1]} se ha conectado")
        escuchador = threading.Thread(
                target=escuchar,
                args=(cliente, addr),
                daemon=True,
                )
        escuchador.start()
        escuchador.join()



def main():
    if len(sys.argv) != 3:
        print("Comando no valido")
        print("Formato correcto: cliente ip_local:puerto_local  ip_remoto:puerto_remoto")
        sys.exit(1)

    try:
        host_local, puerto_local = parsear_direccion(sys.argv[1])
        host_remoto, puerto_remoto = parsear_direccion(sys.argv[2])
    except ValueError:
        print("Error: hubo un problema con la direccion ingresada")
        print("Asegurese que tiene la forma: direccion_ip:puerto")
        sys.exit(1)

    soc_local = crear_socket_servidor(host_local, puerto_local)
    print(f"Escuchando en: {host_local}:{puerto_local}")

    hilo_servidor = threading.Thread(
            target=servicio_servidor,
            args=(soc_local,),
            daemon=True,
            )
    hilo_servidor.start()
    
    hilo_cliente = threading.Thread(
            target=servicio_cliente,
            args=(host_remoto, puerto_remoto),
            daemon=True,
            )

    hilo_cliente.start()
    hilo_cliente.join()

    soc_local.close()


if __name__ == "__main__":
    main()

"""
#Enviar archivo JSON como cliente (IA)

import socket

def enviar_archivo():
    host = 'localhost'  # IP del servidor
    port = 6190
    filename = "archivo_a_enviar.txt"
    
    # Crear socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Conectado a {host}:{port}")
        
        # Enviar archivo
        with open(filename, "rb") as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                s.sendall(data)
        print("Archivo enviado.")

#Recibo de archivo mediante proceso servidor (IA)

import socket

def recibir_archivo():
    # Configuración del servidor
    host = '0.0.0.0'  # Escuchar en todas las interfaces
    port = 6190
    
    # Crear socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        print(f"Escuchando en {host}:{port}...")
        
        conn, addr = s.accept()
        with conn:
            print(f"Conectado por {addr}")
            
            # Recibir el archivo
            with open("archivo_recibido.txt", "wb") as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
            print("Archivo recibido y guardado.")

"""
