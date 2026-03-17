import socket
import threading
import requests
import json
import time

D_IP = "127.0.0.1"
D_PORT = 8000

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


    print("Registrado para próxima ventana")

    consultar_vecinos()
    
def consultar_vecinos():
    url = f"http://{D_IP}:{D_PORT}/vecinos"

    while True:
        try:
            r = requests.get(url)
            data = r.json()
            vecinos = data["vecinos"]

            print("Vecinos actuales:", vecinos)

            for vecino in vecinos:
                conectar_vecino(vecino)

        except Exception as e:
            print("Error al consultar vecinos:", e)

        time.sleep(10) # consultar cada 10 segundos

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