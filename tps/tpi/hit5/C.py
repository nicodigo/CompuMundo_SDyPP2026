import socket
import threading
import time
import json
import sys


def servidor(ip_local: str, puerto_local: int) -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip_local, puerto_local))
    server.listen()

    print("Escuchando en", ip_local, puerto_local)

    while True:
        conn, addr = server.accept()
        print("Conexion entrante:", addr)

        try:
            data = conn.recv(1024)

            if not data:
                continue

            mensaje = json.loads(data.decode())
            print(f"Servidor: Mensaje recibido: {mensaje}\n")

            respuesta = {
                "tipo": "saludo_respuesta",
                "origen": puerto_local,
                "mensaje": "Hola desde servidor"
            }

            json_respuesta = json.dumps(respuesta)
            conn.send(json_respuesta.encode())

        finally:
            conn.close()


def cliente(ip_remoto: str, puerto_remoto: int) -> None:
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip_remoto, puerto_remoto))
            ip_cliente, puerto_cliente = s.getsockname()

            saludo = {
                "tipo": "saludo",
                "ip origen": ip_cliente,
                "puerto origen": puerto_cliente,
                "mensaje": "Hola nodo vecino"
            }

            json_saludo = json.dumps(saludo)
            s.send(json_saludo.encode())

            data = s.recv(1024)

            if data:
                respuesta = json.loads(data.decode())
                print(f"Cliente: Respuesta recibida: {respuesta}\n")

            s.close()
            break

        except ConnectionRefusedError:
            print("No se pudo conectar al servidor")
            print("Reintentando...")
            s.close()
            time.sleep(2)


def main():
    if (len(sys.argv) != 5):
        print("Error: Formato incorrecto")
        print("Se espera: C.py <ip local> <puerto local> <ip remoto> <puerto remoto>")
        sys.exit(1)

    try:
        ip_local = sys.argv[1]
        puerto_local = int(sys.argv[2])

        ip_remoto = sys.argv[3]
        puerto_remoto = int(sys.argv[4])
    except ValueError:
        print("Error: asegurese de que los puertos sean numeros enteros validos")
        sys.exit(1)

    proceso_servidor = threading.Thread(
            target=servidor,
            args=(ip_local, puerto_local),
            daemon=True,
            )

    proceso_cliente = threading.Thread(
            target=cliente,
            args=(ip_remoto, puerto_remoto),
            daemon=True,
            )

    proceso_servidor.start()
    proceso_cliente.start()

    proceso_cliente.join()
    proceso_servidor.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
