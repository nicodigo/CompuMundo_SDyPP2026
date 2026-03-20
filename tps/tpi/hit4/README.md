# TP I HIT 4 README


## Requisitos

1. Python Version 3.12
2. Dos terminales que permitan ejecutar phyton o IDE que permita múltiples terminales

## Instrucciones de Ejecución

1. Posicionado en la carpeta raiz del proyecto ejecute los siguientes comandos

2. Proceso1: en la terminal ejecute "python -m TPs.TPI.Hit3.proceso <ip y puerto de escucha> <ip y puerto proceso2>

3. Proceso2: en la terminal ejecute "python -m TPs.TPI.Hit3.proceso <ip y puerto de escucha> <ip y puerto proceso1>

4. Luego en le Proceso1 deberemos ingresar "r" para intentar reconectar, esto es porqu al iniciarlo el servidor del Proceso2 todavia no estaba en ejecucion, por lo tanto falla la conexion y debemos reintentarla antes de enviar un mensaje.

Ejemplo en linux con python3:

proceso1 > python -m TPs.TPI.Hit4.proceso localhost:18080 localhost:18081

proceso2 > python -m TPs.TPI.Hit4.proceso localhost:18081 localhost:18080

**La direccion y puerto puede ser cualquiera siempre y cuando sea consistente en ambos

## Decisiones de diseño

Mínimas requeridas por consigna, un cliente saluda a un servidor.
Si el cliente termina su proceso el servidor sigue escuchando peticiones, por lo que podria reconectarse, y si el servidor termina el cliente en lugar de fallar le informa al usuario el cual puede intentar reconectar.

# Cuestiones a mejorar
La funcionalidad de la reconexion (paso 4) funciona, pero debe haber una mejor manera de impalementarla para que no sea responsabilidad del usuario, sino del mismo proceso.
