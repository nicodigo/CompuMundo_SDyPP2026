from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

nodos = []
tiempo_inicial = time.time()

# Controlador para las solicitudes HTTP
class Controlador(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/health":
            respuesta = {
                "estado": "ok",
                "nodos_registrados": len(nodos),
                "tiempo_activo": int(time.time() - tiempo_inicial)
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

            nodos.append(nodo)

            respuesta = {
                "vecinos": [n for n in nodos if n != nodo]
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(respuesta).encode())


server = HTTPServer(("0.0.0.0", 8000), Controlador)
print("Nodo D escuchando en puerto 8000")
server.serve_forever()