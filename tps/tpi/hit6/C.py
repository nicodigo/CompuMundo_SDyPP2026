import socket
import threading
import requests
import json
import sys

"""
D_IP = sys.argv[1]
D_PORT = sys.argv[2]

MI_IP = "127.0.0.1"
"""


# Nodo C: se registra en D, recibe vecinos y les envía un saludo
def servidor(d_ip, d_port, ip_local):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_local, 0))   # puerto aleatorio inicial 
    server.listen()

    mi_puerto = server.getsockname()[1] # obtener el puerto asignado

    print("Nodo C escuchando en", ip_local, mi_puerto) # mostrar el puerto real

    registrar_en_D(d_ip, d_port, ip_local, mi_puerto)

    while True:
        conn, addr = server.accept() # esperar conexiones de vecinos

        data = conn.recv(1024)
        if data:
            msg = json.loads(data.decode())
            print("Saludo recibido:", msg) # mostrar el saludo recibido

        conn.close()


# Registrar este nodo en D y conectar con vecinos
def registrar_en_D(d_ip, d_port, ip_local, puerto):

    url = f"http://{d_ip}:{d_port}/registro"

    info_nodo = {
        "ip": ip_local,
        "port": puerto
    }

    r = requests.post(url, json=info_nodo)

    vecinos = r.json()["vecinos"]

    for v in vecinos:
        conectar_vecino(v)


# Enviar un saludo a un vecino
def conectar_vecino(vecino):

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((vecino["ip"], vecino["port"]))
        mi_ip = s.getsockname()[0]

        saludo = {
            "type": "saludo",
            "from": mi_ip
        }

        s.send(json.dumps(saludo).encode()) # enviar saludo al vecino 
        s.close()

        print("Saludo enviado a", vecino)

    except:
        pass


def main():
    if (len(sys.argv) != 4):
        print("Error: Formato incorrecto")
        print("Se espera: C.py <ip D> <puerto D> <ip C>")
        sys.exit(1)

    try:
        d_ip = sys.argv[1]
        d_port = int(sys.argv[2])

        ip_local = sys.argv[3]
    except ValueError:
        print("Error: asegurese de que los puertos sean numeros enteros validos")
        sys.exit(1)

    proceso_servidor = threading.Thread(
            target=servidor,
            args=(d_ip, d_port, ip_local),
            daemon=True,
            )


    proceso_servidor.start()
    
    proceso_servidor.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)





