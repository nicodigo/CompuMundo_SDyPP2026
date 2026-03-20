import socket
import threading
import requests
import json
import sys

D_IP = sys.argv[1]
D_PORT = sys.argv[2]

MI_IP = "127.0.0.1"

# Nodo C: se registra en D, recibe vecinos y les envía un saludo
def servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((MI_IP, 0))   # puerto aleatorio inicial 
    server.listen()

    mi_puerto = server.getsockname()[1] # obtener el puerto asignado

    print("Nodo C escuchando en", MI_IP, mi_puerto) # mostrar el puerto real

    registrar_en_D(mi_puerto)

    while True:
        conn, addr = server.accept() # esperar conexiones de vecinos

        data = conn.recv(1024)
        if data:
            msg = json.loads(data.decode())
            print("Saludo recibido:", msg) # mostrar el saludo recibido

        conn.close()

# Registrar este nodo en D y conectar con vecinos
def registrar_en_D(puerto):

    url = f"http://{D_IP}:{D_PORT}/registro"

    info_nodo = {
        "ip": MI_IP,
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

        saludo = {
            "type": "saludo",
            "from": MI_IP
        }

        s.send(json.dumps(saludo).encode()) # enviar saludo al vecino 
        s.close()

        print("Saludo enviado a", vecino)

    except:
        pass


threading.Thread(target=servidor).start() # iniciar el servidor en un hilo separado