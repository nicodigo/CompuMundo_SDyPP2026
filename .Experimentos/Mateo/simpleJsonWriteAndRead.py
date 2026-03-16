#DEO GLORIA

import json

def escribir_json():

    datos = {
        "empresa": "Tecnología XYZ",
        "empleados": [
        {"id": 1, "nombre": "Carlos"},
        {"id": 2, "nombre": "Laura"}
        ]
    }

    # Escribir en el archivo
    with open('datos.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4) # 'indent' formatea el JSON

def leer_json():
    # 1. Abrir el archivo JSON
    with open('datos.json', 'r', encoding='utf-8') as archivo:
        # 2. Cargar los datos
        datos = json.load(archivo)

    # 3. Acceder a los datos
    print(datos)
    print(datos['empleados'][1]['nombre']) # Acceso a una clave específica

def mostrar_menu():

    print("----- MENU JSON -----")
    print(" ")
    print("1. Cargar JSON    ")
    print("2. Leer JSON      ")
    print()
    print("0. Salir")
    print()

def manejar_menu():

    opcion = 1

    while (opcion != 0):

        mostrar_menu()
        opcion = int(input("Ingrese su elección: "))

        match opcion:
            
            case 0:
                print("El programa ha terminado. Saludos")

            case 1:
                escribir_json()
            
            case 2:
                leer_json()

            case _:
                print("Conque se anda de chistoso usted.")

    

manejar_menu()



"""

#Crear un archivo json (IA)

import json

datos = {
    "empresa": "Tecnología XYZ",
    "empleados": [
        {"id": 1, "nombre": "Carlos"},
        {"id": 2, "nombre": "Laura"}
    ]
}

# Escribir en el archivo
with open('datos.json', 'w', encoding='utf-8') as f:
    json.dump(datos, f, indent=4) # 'indent' formatea el JSON

"""
    

"""

#Leer de json local

import json

# 1. Abrir el archivo JSON
with open('datos.json', 'r', encoding='utf-8') as archivo:
    # 2. Cargar los datos
    datos = json.load(archivo)

# 3. Acceder a los datos
print(datos)
print(datos['nombre']) # Acceso a una clave específica

"""