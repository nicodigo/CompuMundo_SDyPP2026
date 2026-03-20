# DEO GLORIA

import sys
from netutils import parsear_direccion, crear_socket_servidor, recibir_mensaje, enviar_mensaje


def main():
    if len(sys.argv) != 2:
        print("Comando no valido")
        print("Formato correcto: servidor.py direccion_ip_servidor:puerto_servidor")
        sys.exit(1)

    host, puerto = parsear_direccion(sys.argv[1])

    servidor = crear_socket_servidor(host, puerto)

    while True:

        cliente, addr = servidor.accept()

        msj = recibir_mensaje(cliente)
        print(f"({addr[0]}:{addr[1]}): {msj}")

        enviar_mensaje(cliente, "Hola mundo desde B")

        cliente.close()


if __name__ == "__main__":
    main()
