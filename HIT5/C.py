import socket
import threading
import time
import json
import sys

MI_IP = sys.argv[1]
MI_PUERTO = int(sys.argv[2])

OTRO_IP = sys.argv[3]
OTRO_PUERTO = int(sys.argv[4])


def servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((MI_IP, MI_PUERTO))
    server.listen()

    print("Escuchando en", MI_IP, MI_PUERTO)

    while True:
        conn, addr = server.accept()
        print("Conexion entrante:", addr)

        try:
            data = conn.recv(1024)

            if not data:
                continue

            mensaje = json.loads(data.decode())
            print("Mensaje recibido:", mensaje)

            respuesta = {
                "tipo": "saludo_respuesta",
                "origen": MI_PUERTO,
                "mensaje": "Hola desde servidor"
            }

            json_respuesta = json.dumps(respuesta)
            conn.send(json_respuesta.encode())

        finally:
            conn.close()


def cliente():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((OTRO_IP, OTRO_PUERTO))

            saludo = {
                "tipo": "saludo",
                "origen": MI_PUERTO,
                "mensaje": "Hola nodo vecino"
            }

            json_saludo = json.dumps(saludo)
            s.send(json_saludo.encode())

            data = s.recv(1024)

            if data:
                respuesta = json.loads(data.decode())
                print("Respuesta recibida:", respuesta)

            s.close()
            break

        except ConnectionRefusedError:
            time.sleep(2)


threading.Thread(target=servidor, daemon=True).start()
threading.Thread(target=cliente).start()

while True:
    time.sleep(1)