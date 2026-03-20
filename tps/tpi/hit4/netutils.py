import socket
from typing import Tuple


def parsear_direccion(addr: str) -> Tuple[str, int]:
    """
    Puede ocasionar una excepcion 
    ValueError
    si la cadena no es la esperada, por ejemplo si el puerto no puede convertirse a entero
    """
    host, puerto = addr.split(":")
    return host, int(puerto)


def crear_socket_servidor(host: str, puerto: int) -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, puerto))
    s.listen()
    return s

def crear_socket_cliente() -> socket.socket:
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def enviar_mensaje(sock: socket.socket, msj: str) -> None:
    sock.sendall(msj.encode("utf-8"))


def recibir_mensaje(sock: socket.socket, size=1024) -> str:
    datos = sock.recv(size)
    return datos.decode("utf-8")
