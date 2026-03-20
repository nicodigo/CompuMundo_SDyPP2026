from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, Tuple, List, Any
import json
import threading
import sys
import time


ACTIVOS: List[Tuple[str, int]] = []
PROXIMOS: List[Tuple[str, int]] = []

FILE_EJECUCION = "registro_ejecucion.json"


class Manejador(BaseHTTPRequestHandler):
    def _set_headers(self,
                     status: int = 200,
                     content_type: str = "application/json"
                     ) -> None:
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def _read_json(self) -> Dict:
        content_length: int = int(self.headers.get("Content-Length", 0))
        cuerpo: bytes = self.rfile.read(content_length)
        return json.loads(cuerpo.decode("utf-8"))

    def do_GET(self) -> None:
        if self.path == "/health":
            self._handle_health()
        elif self.path == "/activos":
            self._handle_get_activos()
        else:
            self._set_headers(404)
            self.wfile.write(b'{"error": "Not Found"}')

    def do_POST(self) -> None:
        if self.path == "/registro":
            self._handle_registro()
        else:
            self._set_headers(404)
            self.wfile.write(b'{"error": "Not Found"}')

    def _handle_registro(self) -> None:
        try:
            data: Dict = self._read_json()
            ip: str = data["ip"]
            puerto: int = int(data["puerto"])

            nodo: Tuple[str, int] = (ip, puerto)

            if nodo not in PROXIMOS:
                PROXIMOS.append(nodo)

            self._set_headers(200)
            respuesta: Dict = {
                    "estado": "registrado",
                    "nodos-activos": [
                        {"ip": ip, "puerto": puerto}
                        for ip, puerto in ACTIVOS
                        ]
                    }
            self.wfile.write(json.dumps(respuesta).encode("utf-8"))

            registrar_evento("registro-nodo", data)

        except (KeyError, ValueError, json.JSONDecodeError):
            self._set_headers(404)
            self.wfile.write(b'{"error": "Not Found"}')

    def _handle_health(self) -> None:
        self._set_headers(200)
        respuesta: Dict = {
                "estado": "ok",
                "cant_conectados": len(ACTIVOS)
                }
        self.wfile.write(json.dumps(respuesta).encode("utf-8"))

    def _handle_get_activos(self) -> None:
        self._set_headers(200)
        respuesta: Dict = {
                "nodos": [
                    {"ip": ip, "puerto": puerto}
                    for ip, puerto in ACTIVOS
                    ]
                }
        self.wfile.write(json.dumps(respuesta).encode("utf-8"))


def run(server_class: type[HTTPServer] = HTTPServer,
        handler_class: type[BaseHTTPRequestHandler] = Manejador,
        ip: str = "localhost",
        puerto: int = 8080) -> None:

    server_addr: Tuple[str, int] = (ip, puerto)
    httpd: HTTPServer = server_class(server_addr, handler_class)

    print(f"Servidor corriendo en {ip}:{puerto}")
    httpd.serve_forever()


def manejar_ventana():
    global ACTIVOS, PROXIMOS

    while True:
        print("Cambio de ventana")
        datos_evento: Dict[str, Any] = {
                "activos": ACTIVOS,
                "proximos": PROXIMOS,
                }
        registrar_evento("cambio-ventana", datos_evento)
        ACTIVOS = PROXIMOS.copy()
        PROXIMOS.clear()
        time.sleep(60)


def registrar_evento(evento: str, datos: Dict[str, Any]) -> None:
    registro: Dict[str, Any] = {
            "evento": evento,
            "timestamp": time.time(),
            "datos": datos,
            }
    with open(FILE_EJECUCION, "a") as jfile:
        json.dump(registro, jfile, indent=4)


def main():

    with open(FILE_EJECUCION, "w"):
        pass

    servidor_http = threading.Thread(
            target=run,
            daemon=True,
            )
    servidor_http.start()
    manejador_ventana = threading.Thread(
            target=manejar_ventana,
            daemon=True
            )

    manejador_ventana.start()
    manejador_ventana.join()


if __name__ == "__main__":
    main()
