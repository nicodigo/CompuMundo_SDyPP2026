from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import threading

nodos_corriendo = []
nodos_proximos = []

FILE = "estado_nodo.json"


def guardar_estado():
    data = {
        "corriendo": nodos_corriendo,
        "proximos": nodos_proximos
    }
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def rotar_ventana():
    global nodos_corriendo, nodos_proximos

    while True:
        ahora = time.time()
        descanso = 60 - (int(ahora) % 60)
        time.sleep(descanso)

        nodos_corriendo = nodos_proximos
        nodos_proximos = []

        print("Nueva ventana iniciada")
        guardar_estado()

# Controlador para las solicitudes HTTP
class Controlador(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/vecinos":   
            respuesta = {
                "vecinos": nodos_corriendo
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(respuesta).encode())
        elif self.path == "/health":
            respuesta = {
                "estado": "ok",
                "nodos_corriendo": len(nodos_corriendo),
                "nodos_proximos": len(nodos_proximos)
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(respuesta).encode())

    def do_POST(self):
        if self.path == "/registro":

            length = int(self.headers["Content-Length"])
            data = self.rfile.read(length)
            nodo = json.loads(data.decode())

            nodos_proximos.append(nodo)

            guardar_estado()

            respuesta = {
                "mensaje" : "Nodo registrado para la próxima ventana"
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(respuesta).encode())


threading.Thread(target=rotar_ventana, daemon=True).start()

server = HTTPServer(("0.0.0.0", 8000), Controlador)
print("Nodo D escuchando en puerto 8000")
server.serve_forever()