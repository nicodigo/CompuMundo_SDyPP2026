# TP I HIT 3 README


## Requisitos

1. Python Version 3.12
2. Dos terminales que permitan ejecutar phyton o IDE que permita múltiples terminales

## Instrucciones de Ejecución

1. Posicionado en la carpeta raiz del proyecto ejecute los siguientes comandos
2. Servidor: en la terminal servidor ejecute "python -m TPs.TPI.Hit3.servidor direccion_ip_servidor:puerto_servidor"
3. Cliente: en la terminal cliente ejecute "python -m TPs.TPI.Hit3.cliente direccion_ip_servidor:puerto_servidor"

Ejemplo en linux con python3:

servidor > python -m TPs.TPI.Hit3.servidor localhost:18080

cliente > python -m TPs.TPI.Hit3.cliente localhost:18080

**La direccion y puerto puede ser cualquiera siempre y cuando sea consistente en ambos

## Decisiones de diseño

Mínimas requeridas por consigna, un cliente saluda a un servidor.
Si el cliente termina su proceso el servidor sigue escuchando peticiones, por lo que podria reconectarse, y si el servidor termina el cliente en lugar de fallar le informa al usuario el cual puede intentar reconectar.
