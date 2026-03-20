from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import sys


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



def main():
    if (len(sys.argv) != 2):
        print("Error: Formato incorrecto")
        print("Se espera: D.py <puerto para D>")
        sys.exit(1)

    try:
        d_port = int(sys.argv[1])
    except ValueError:
        print("Error: asegurese de que los puertos sean numeros enteros validos")
        sys.exit(1)

    server = HTTPServer(("0.0.0.0", d_port), Controlador)
    print("Nodo D escuchando en puerto " + d_port)
    server.serve_forever()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
