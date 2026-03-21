# Sistema de Comunicación TCP (Cliente-Servidor)

## Descripción
Implementación de una arquitectura cliente-servidor basada en sockets TCP para el intercambio de mensajes de texto. El sistema gestiona la persistencia del servidor ante desconexiones del cliente y la capacidad de reconexión automática del cliente ante caídas del servidor.

## Estructura del Proyecto
* **netutils.py**: Biblioteca de utilidades para la abstracción de creación de sockets, codificación/decodificación UTF-8 y procesamiento de direcciones IP/Puerto.
* **servidor.py**: Proceso B. Escucha conexiones entrantes, procesa saludos del cliente y mantiene el ciclo de ejecución tras la finalización de sesiones individuales.
* **cliente.py**: Proceso A. Establece conexión con el proceso B, envía un saludo y gestiona excepciones de red mediante un bucle de reintento de conexión.

## Requisitos
* Python 3.x instalado.

## Ejecución

### 1. Servidor (Proceso B)
Debe iniciarse primero para habilitar el puerto de escucha.
```bash
python servidor.py <direccion_ip>:<puerto>
```

### 2. Cliente (Proceso A)
```bash
python cliente.py <direccion_ip_servidor>:<puerto_servidor>
```
