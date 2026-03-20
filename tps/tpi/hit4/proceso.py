import sys
from netutils import *
import threading
import socket


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
        while True:
            msj = recibir_mensaje(c)
            if not msj: break
            print(f"({a[0]}:{a[1]}): {msj}")
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
