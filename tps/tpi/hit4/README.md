# Nodo de Comunicación Bidireccional (Programa C)

Implementación de un nodo único que integra funciones de cliente y servidor para la comunicación simultánea entre dos instancias mediante hilos.

## Descripción
El sistema permite que dos procesos se conecten entre sí de forma recíproca. Cada instancia levanta un hilo de servidor para recibir mensajes y un hilo de cliente para enviarlos, resolviendo la necesidad de programas cliente-servidor independientes.

## Requisitos
* Python 3.x
* `netutils.py` (Módulo de utilidades de red)
* `proceso.py` (Script principal)

## Ejecución
El programa requiere dos argumentos posicionales con el formato `ip:puerto`.

```bash
python proceso.py <direccion_local>:<puerto_local> <direccion_remota>:<puerto_remota>
```

### Ejemplo de configuración para dos instancias (Localhost):
**Instancia 1:**
```bash
python proceso.py 127.0.0.1:8000 127.0.0.1:8001
```
**Instancia 2:**
```bash
python proceso.py 127.0.0.1:8001 127.0.0.1:8000
```

## Estructura y Lógica
1.  **Hilos (Threading):** El servidor se ejecuta como un demonio para permitir la escucha constante sin bloquear la entrada de teclado del cliente.
2.  **Sockets:** Utiliza TCP (`SOCK_STREAM`) para garantizar la entrega de mensajes.
3.  **Gestión de Errores:** Implementa lógica de reconexión manual en el cliente y manejo de excepciones en la recepción de datos.

## Interacción
* **Envío:** Escriba cualquier texto y presione `Enter`.
* **Recepción:** Los mensajes remotos se muestran automáticamente indicando origen y puerto.
* **Cierre:** La entrada de la letra `s` finaliza el proceso de cliente.
