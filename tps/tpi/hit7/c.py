import threading
from typing import Dict, Any, Tuple
import http.client
import json
import sys
import time
import socket


class NodoCliente:
    def __init__(self, server_ip: str, server_puerto: int) -> None:
        self.server_ip: str = server_ip
        self.server_puerto: int = server_puerto

    def _request(
            self,
            method: str,
            path: str,
            body: Dict[str, Any] | None = None
            ) -> Tuple[int, Dict[str, Any]]:
        conn: http.client.HTTPConnection = http.client.HTTPConnection(
                self.server_ip,
                self.server_puerto,
                timeout=5
                )

        headers: Dict[str, str] = {
                "Content-Type": "application/json"
                }

        payload: str | None = None
        if body is not None:
            payload = json.dumps(body)

        conn.request(method, path, body=payload, headers=headers)

        respuesta: http.client.HTTPResponse = conn.getresponse()
        estado: int = respuesta.status

        datos_crudos: bytes = respuesta.read()
        conn.close()

        if not datos_crudos:
            return estado, {}

        try:
            datos: Dict[str, Any] = json.loads(datos_crudos.decode("utf-8"))
        except json.JSONDecodeError:
            datos = {}

        return estado, datos

    def registrar(self, ip: str, puerto: int) -> Tuple[int, Dict[str, Any]]:
        body: Dict[str, Any] = {
                "ip": ip,
                "puerto": puerto
                }
        return self._request("POST", "/registro", body)

    def get_health(self) -> Tuple[int, Dict[str, Any]]:
        return self._request("GET", "/health")

    def get_activos(self) -> Tuple[int, Dict[str, Any]]:
        return self._request("GET", "/activos")


def run_ping(c: NodoCliente) -> None:
    estado, datos = c.get_health()
    while (datos["estado"] == "ok"):
        print (f"\n\ncheckhealth: {estado}\n{datos}\n\n")
        time.sleep(55)


def saludar_vecinos(cliente: NodoCliente, ip_local: str, puerto_local: int) -> None:
    mensaje: Dict[str, Any] = {
            "from": f"{ip_local}:{puerto_local}",
            "texto": "Hola vecino!"
            }
    mensaje_json = json.dumps(mensaje)
    while True:
        estado, datos = cliente.get_activos()
        if estado != 200: continue
        for nodo in datos["nodos"]:
            ip = nodo["ip"]
            puerto = nodo["puerto"]
            if (ip == ip_local) and (puerto == puerto_local):
                continue
            try:
                soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                soc.connect((nodo["ip"], nodo["puerto"]))
                soc.sendall(mensaje_json.encode("utf-8"))
            except Exception:
                print(f"Error al saludar a {ip}:{puerto}")

        time.sleep(30)


def escuchar_saludos(s_escucha: socket.socket) -> None:
    ip_local, puerto_local = s_escucha.getsockname()
    print(f"{ip_local}")

    while True:
        conn, addr= s_escucha.accept()
        datos = conn.recv(1024).decode("utf-8")
        print("mensaje nuevo")
        print(f"{addr[0]}:{addr[1]}: {datos} \n")
        conn.close()


def main():
    if (len(sys.argv) != 4):
        print("Error: Formato incorrecto")
        print("Se espera: c.py <ip D> <puerto D> <ip C>")
        sys.exit(1)

    try:
        d_ip = sys.argv[1]
        d_port = int(sys.argv[2])

        ip_local = sys.argv[3]
    except ValueError:
        print("Error: asegurese de que los puertos sean numeros enteros validos")
        sys.exit(1)

    cliente: NodoCliente = NodoCliente(d_ip, d_port)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_local, 0))  # puerto aleatorio inicial
    server.listen()
    puerto_local = server.getsockname()[1]  # obtener el puerto asignado

    estado_reg, datos_reg = cliente.registrar(ip_local, puerto_local)
    if estado_reg != 200:
        print(f"Error al registrar\n{estado_reg}\n{datos_reg}")
        sys.exit(1)
    print("registrado con exito")

    escuchar = threading.Thread(
            target=escuchar_saludos,
            args=(server,),
            daemon=True,
            )

    checkhealth = threading.Thread(
            target=run_ping,
            args=(cliente,),
            daemon=True,
            )

    saludar = threading.Thread(
            target=saludar_vecinos,
            args=(cliente, ip_local, puerto_local),
            daemon=True,
            )

    checkhealth.start()
    saludar.start()
    escuchar.start()

    while True:
        opt = input("para anotarse para la proxima ventana presione <Enter>")
        if opt == "s": break
        estado_reg, datos_reg = cliente.registrar(ip_local, puerto_local)
        if estado_reg != 200:
            print(f"Error al registrar\n{estado_reg}\n{datos_reg}")
            break
        print("Registrado con exito")

    checkhealth.join()
    saludar.join()
    escuchar.join()


if __name__ == "__main__":
    main()
