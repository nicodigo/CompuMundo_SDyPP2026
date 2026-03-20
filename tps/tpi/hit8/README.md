# Nodo gRPC Bidireccional (Programa C)

Implementación de un nodo único que integra un servidor y un cliente gRPC para establecer comunicación recíproca entre dos instancias independientes.

## Requisitos
Instalación de dependencias mediante pip:
```bash
pip install -r requisitos.txt
```
O en el caso que el se requiera un entorno virtual para no interferir con los paquetes globales (en linux):
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requisitos.txt
```


## Estructura del Proyecto
* `C.py`: Lógica principal del nodo (Servidor y Cliente).
* `nodo.proto`: Definición del servicio y mensajes.
* `nodo_pb2.py` / `nodo_pb2_grpc.py`: Código generado por el compilador de Protocol Buffers.

## Ejecución
El programa requiere la IP y el puerto local para el servidor, y la IP y el puerto remoto para el cliente.

```bash
python C.py <ip_local> <puerto_local> <ip_remoto> <puerto_remoto>
```

### Ejemplo de uso (Local)
Para comunicar dos instancias en la misma máquina:

**Terminal 1:**
```bash
python C.py 127.0.0.1 50051 127.0.0.1 50052
```

**Terminal 2:**
```bash
python C.py 127.0.0.1 50052 127.0.0.1 50051
```

## Lógica de Operación
1.  **Paralelismo:** El programa inicia dos hilos (`threading.Thread`). Uno ejecuta el servidor gRPC y el otro el cliente.
2.  **Servidor:** Implementa `NodoServicer` y escucha peticiones de saludo en el puerto local definido.
3.  **Cliente:** Intenta contactar recursivamente al nodo remoto. Al establecer conexión, envía un `SaludoRequest` y procesa la respuesta.
