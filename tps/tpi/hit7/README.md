# Sistema de Inscripciones Distribuido

## Descripción General

Implementación de un sistema distribuido basado en nodos C (clientes) y un nodo D (coordinador).

- Ventanas de tiempo fijas de 60 segundos (en código actual: 30s)
- Los nodos C se registran en D
- El registro es diferido: aplica a la próxima ventana
- D mantiene:
  - ACTIVOS: nodos en ventana actual
  - PROXIMOS: nodos para la siguiente ventana
- Cada intervalo:
  - PROXIMOS → ACTIVOS
  - PROXIMOS se limpia

---

## Arquitectura

### Nodo D (d.py)

Responsabilidades:
- Servidor HTTP
- Gestión de ventanas
- Persistencia en JSON

Endpoints:
- POST /registro
- GET /health
- GET /activos

---

### Nodo C (c.py)

Responsabilidades:
- Registro en D
- Consulta de nodos activos
- Comunicación P2P vía TCP
- Escucha de mensajes

---

## Flujo

1. Nodo C inicia
2. Abre socket TCP en puerto dinámico
3. Se registra en D
4. D lo agrega a PROXIMOS
5. Cambio de ventana:
   - PROXIMOS → ACTIVOS
6. C consulta /activos
7. C se comunica con nodos activos

---

## Endpoints

### POST /registro

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

{
  "estado": "ok",
  "cant_conectados": N
}

---

### GET /activos

{
  "nodos": [
    {"ip": "...", "puerto": ...}
  ]
}

---

## Comunicación entre nodos

Protocolo: TCP

Mensaje:
{
  "from": "ip:puerto",
  "texto": "Hola vecino!"
}

---

## Persistencia

Archivo: registro_ejecucion.json

Eventos:
- registro-nodo
- cambio-ventana

Formato:
{
  "evento": "...",
  "timestamp": ...,
  "datos": {...}
}

---

## Concurrencia

Nodo D:
- Hilo HTTP
- Hilo de ventanas

Nodo C:
- Hilo escucha TCP
- Hilo envío mensajes
- Hilo health

---

## Ejecución

Nodo D:
python3 d.py

Nodo C:
python3 c.py <ip_D> <puerto_D> <ip_local>

Ejemplo:
python3 c.py localhost 8080 localhost

---

## Limitaciones

- JSON no estructurado (append inválido)
- Locks incorrectos (no compartidos)
- No thread-safe real
- Intervalo inconsistente (30s vs 60s)
- HTTPServer secuencial
- Sin manejo robusto de errores

---

## Estado

Funcional a nivel conceptual:
- Registro diferido: OK
- Consulta activos: OK
- Comunicación entre nodos: OK
- Persistencia: parcial

Problemas en sincronización y robustez.
