import sys
from concurrent import futures
import time
import threading
import grpc
import nodo_pb2
import nodo_pb2_grpc


class Nodo(nodo_pb2_grpc.NodoServicer):
    def Saludo(self, request, context):
        return nodo_pb2.SaludoResponse(mensaje=f"Hola, {request.name}!")


def servir(ip_local: str, puerto_local: int) -> None:
    server: grpc.Server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=3)
            )

    nodo_pb2_grpc.add_NodoServicer_to_server(
            Nodo(),
            server,
           )

    server.add_insecure_port(f"{ip_local}:{puerto_local}")
    server.start()

    print(f"Servidor gRPC escuchando en {ip_local}:{puerto_local}")

    server.wait_for_termination()


def cliente(ip_remoto: str, puerto_remoto: int) -> None:
    while True:
        try:
            print("Intentando saludar a Nodo vecino...")
            with grpc.insecure_channel(f"{ip_remoto}:{puerto_remoto}") as channel:
                stub: nodo_pb2_grpc.NodoStub = nodo_pb2_grpc.NodoStub(channel)

                request: nodo_pb2.SaludoRequest = nodo_pb2.SaludoRequest(
                        name="Nodo"
                        )

                response: nodo_pb2.SaludoResponse = stub.Saludo(request)

                print("Cliente recibio: ", response.mensaje)
                break

        except grpc.RpcError as e:
            print(f"Error RPC: {e}\n")
            print("Reintentando...\n\n")
            time.sleep(2)


def main():
    if (len(sys.argv) != 5):
        print("Error: Formato incorrecto")
        print("Se espera: C.py <ip local> <puerto local> <ip remoto> <puerto remoto>")
        sys.exit(1)

    try:
        ip_local = sys.argv[1]
        puerto_local = int(sys.argv[2])

        ip_remoto = sys.argv[3]
        puerto_remoto = int(sys.argv[4])
    except ValueError:
        print("Error: asegurese de que los puertos sean numeros enteros validos")
        sys.exit(1)

    proceso_servidor = threading.Thread(
            target=servir,
            args=(ip_local, puerto_local),
            daemon=True,
            )

    proceso_cliente = threading.Thread(
            target=cliente,
            args=(ip_remoto, puerto_remoto),
            daemon=True,
            )

    proceso_servidor.start()
    proceso_cliente.start()

    proceso_cliente.join()
    proceso_servidor.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
