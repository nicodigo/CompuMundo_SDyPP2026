# Sistema de Inscripciones Distribuido

## Descripción

Implementación de un sistema distribuido con nodos C (clientes) y un nodo D (coordinador) que administra inscripciones en ventanas de tiempo discretas.

El sistema cumple con:

- Ventanas de tiempo fijas de 60 segundos
- Registro diferido: todo nodo se inscribe para la próxima ventana
- Separación entre nodos activos y nodos futuros
- Persistencia de eventos en formato JSON

---

## Modelo de Ventanas

El sistema opera en ciclos temporales:

- Un nodo que se registra en tiempo T queda activo en T+1
- Al iniciar una nueva ventana:
  - PROXIMOS → ACTIVOS
  - PROXIMOS se vacía

Ejemplo:

- Registro a las 11:28:34 → activo en 11:29
- Registros posteriores a 11:29 → pasan a 11:30

Los nodos solo pueden observar los nodos activos de la ventana actual.

---

## Arquitectura

### Nodo D (Coordinador)

Archivo: d.py

Responsabilidades:

- Exponer API HTTP
- Gestionar ventanas temporales
- Mantener estado:
  - ACTIVOS
  - PROXIMOS
- Persistir eventos en archivo JSON

---

### Nodo C (Cliente)

Archivo: c.py

Responsabilidades:

- Registrarse en D
- Consultar nodos activos
- Comunicarse con otros nodos mediante TCP
- Escuchar conexiones entrantes

---

## Endpoints HTTP

### POST /registro

Registra un nodo para la próxima ventana.

Request:
{
  "ip": "127.0.0.1",
  "puerto": 5000
}

Response:
{
  "estado": "registrado",
  "nodos-activos": [...]
}

---

### GET /health

Devuelve estado del sistema.

{
  "estado": "ok",
  "cant_conectados": N
}

---

### GET /activos

Devuelve nodos activos en la ventana actual.

{
  "nodos": [
    {"ip": "...", "puerto": ...}
  ]
}

---

## Comunicación entre Nodos C

- Protocolo: TCP
- Cada nodo:
  - Escucha conexiones entrantes
  - Envía mensajes a otros nodos activos

Formato del mensaje:

{
  "from": "ip:puerto",
  "texto": "Hola vecino!"
}

---

## Persistencia

Archivo: registro_ejecucion.json

Eventos registrados:

- registro-nodo
- cambio-ventana

Formato:

{
  "evento": "...",
  "timestamp": ...,
  "datos": {...}
}

Nota: el archivo se escribe en modo append sin estructura de arreglo JSON válida.

---

## Concurrencia

Nodo D:

- Hilo HTTP (manejo de requests)
- Hilo de manejo de ventanas

Nodo C:

- Hilo de escucha TCP
- Hilo de envío de mensajes
- Hilo de chequeo de estado

---

## Ejecución

### Nodo D

python3 d.py

Por defecto el Servidor escucha en:
localhost:8080

---

### Nodo C

python3 c.py <ip_D> <puerto_D> <ip_local>

Ejemplo:

python3 c.py localhost 8080 localhost

---

## Flujo de Ejecución

1. Nodo C inicia
2. Abre socket TCP en puerto dinámico
3. Se registra en D
4. D agrega nodo a PROXIMOS
5. Cambio de ventana:
   - PROXIMOS → ACTIVOS
6. C consulta nodos activos
7. C envía mensajes a otros nodos

---

## Limitaciones

- No thread-safe (acceso concurrente sin sincronización)
- Sin validación de duplicados robusta
- Sin manejo de fallos de red
- Sin control de desconexión de nodos
- No se puede elegir el puerto o ip de escucha del Servidor sin cambiar el código

---

## Estado del Sistema

Implementa correctamente:

- Registro diferido por ventanas
- Separación entre nodos activos y futuros
- Consulta de nodos activos
- Comunicación entre nodos
- Registro de eventos

Limitaciones presentes en sincronización, persistencia y robustez.
