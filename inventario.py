import json

archivo_inventario = 'inventario.json'

def cargar_inventario():
    global inventario
    try:
        with open(archivo_inventario, 'r') as file:
            inventario = json.load(file)
    except FileNotFoundError:
        inventario = []
    except json.JSONDecodeError:
        inventario = []

def guardar_inventario():
    with open(archivo_inventario, 'w') as file:
        json.dump(inventario, file, indent=4)

def agregar_producto(nombre, cantidad, precio):
    inventario.append([nombre, cantidad, precio])
    guardar_inventario()

def eliminar_producto(nombre):
    global inventario
    inventario = [p for p in inventario if p[0] != nombre]
    guardar_inventario()

def modificar_producto(nombre_antiguo, nuevo_nombre, nueva_cantidad, nuevo_precio):
    for producto in inventario:
        if producto[0] == nombre_antiguo:
            producto[0] = nuevo_nombre
            producto[1] = nueva_cantidad
            producto[2] = nuevo_precio
    guardar_inventario()

def calcular_valor_total():
    return sum(p[1] * p[2] for p in inventario)
