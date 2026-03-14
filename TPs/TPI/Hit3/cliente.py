import sys
from TPs.TPI.common.netutils import *
import time


def main():
    if len(sys.argv) != 2:
        print("Comando no valido")
        print("Formato correcto: cliente.py direccion_ip_servidor:puerto_servidor")
        sys.exit(1)

    try:
        host, puerto = parsear_direccion(sys.argv[1])
    except ValueError:
        print("Error: hubo un problema con la direccion ingresada")
        print("Asegurese que tiene la forma: direccion_ip_servidor:puerto_servidor")
        sys.exit(1)

    while True:
        sock_cliente = crear_socket_cliente()
        try: sock_cliente.connect((host, puerto))
        except Exception:
            print(f"{host}:{puerto} no responde")
            print("Verifique su conexion y si el servidor esta corriendo")
            input("Presione <Enter> cuando quiera intentar reconectar")
            sock_cliente.close()
            continue

        enviar_mensaje(sock_cliente, "Hola mundo desde A")
        print("Enviando mensaje...")
        time.sleep(2)

        respuesta = recibir_mensaje(sock_cliente)
        print(f"Respuesta del servidor: {respuesta}")

        sock_cliente.close()


if __name__ == "__main__":
    main()
