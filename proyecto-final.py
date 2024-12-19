import sqlite3
from colorama import init, Fore, Style

# Inicializa colorama
init(autoreset=True)

# Funciones
def crear_tabla():
    conn = sqlite3.connect("bdproyecto.db")
    cursor = conn.cursor()
    inst = '''CREATE TABLE IF NOT EXISTS productos(
                id integer primary key autoincrement,
                producto text,
                stock integer,
                precio float)'''
    cursor.execute(inst)
    conn.commit()
    conn.close()


def agregar_productos(producto, stock, precio):
    try:
        conn = sqlite3.connect("bdproyecto.db")
        cursor = conn.cursor()
        inst = "INSERT INTO productos (producto, stock, precio) VALUES (?, ?, ?)"
        parametros = (producto, stock, precio)
        cursor.execute(inst, parametros)
        conn.commit()
        print(Fore.GREEN + f"Producto '{producto}' agregado correctamente.")
    except sqlite3.Error as e:
        print(Fore.RED + f"Error al agregar el producto: {e}")
    finally:
        conn.close()


def leer_productos():
    conn = sqlite3.connect("bdproyecto.db")
    cursor = conn.cursor()
    inst = "SELECT * FROM productos"
    cursor.execute(inst)
    datos = cursor.fetchall()
    conn.close()
    if datos:
        print(Fore.CYAN + "Lista de productos:")
        for producto in datos:
            print(Fore.YELLOW + f"ID: {producto[0]}, Producto: {producto[1]}, Stock: {producto[2]}, Precio: {producto[3]:.2f}")
    else:
        print(Fore.RED + "No hay productos registrados.")


def reporte_bajo_stock(umbral=5):
    conn = sqlite3.connect("bdproyecto.db")
    cursor = conn.cursor()
    inst = "SELECT * FROM productos WHERE stock < ?"
    cursor.execute(inst, (umbral,))
    productos_bajo_stock = cursor.fetchall()
    conn.close()
    if productos_bajo_stock:
        print(Fore.CYAN + f"Productos con stock menor a {umbral}:")
        for producto in productos_bajo_stock:
            print(Fore.YELLOW + f"ID: {producto[0]}, Producto: {producto[1]}, Stock: {producto[2]}, Precio: {producto[3]:.2f}")
    else:
        print(Fore.GREEN + f"No hay productos con stock menor a {umbral}.")


def actualizar_producto():
    conn = sqlite3.connect("bdproyecto.db")
    cursor = conn.cursor()
    nuevo_producto = input(Fore.BLUE + "¿Qué producto deseas modificar? ").capitalize()
    nuevo_stock = int(input(Fore.BLUE + "¿Cuál es el stock correcto? "))
    nuevo_precio = float(input(Fore.BLUE + "¿Cuál es el nuevo precio? "))
    inst = f"UPDATE productos SET precio={nuevo_precio}, stock={nuevo_stock} WHERE producto LIKE '{nuevo_producto}'"
    cursor.execute(inst)
    conn.commit()
    conn.close()
    print(Fore.GREEN + f"Producto '{nuevo_producto}' actualizado correctamente.")


def eliminar():
    conn = sqlite3.connect("bdproyecto.db")
    cursor = conn.cursor()
    producto = input(Fore.BLUE + "Introduce el nombre del producto que deseas eliminar: ").capitalize()
    inst = f"DELETE FROM productos WHERE producto LIKE '{producto}'"
    cursor.execute(inst)
    conn.commit()
    conn.close()
    print(Fore.GREEN + f"Producto '{producto}' eliminado correctamente, si existía.")


# Menú principal
while True:
    print(Fore.MAGENTA + Style.BRIGHT + "                 * Bienvenido al Sistema de Gestión de Productos *")
    inicio = input(Fore.CYAN + '''
        ------------------------------------------------------------------------
        ¿Qué tarea desea realizar? Selecciona la opción introduciendo el número: 
        ------------------------------------------------------------------------
        1. Agregar producto
        2. Modificar producto
        3. Consultar productos
        4. Eliminar producto
        5. Reporte de bajo stock
        6. Salir
    ''' + Fore.WHITE)

    if inicio == "1":
        producto = input(Fore.BLUE + "Introduce el nombre del producto que deseas agregar: ").capitalize()
        stock = int(input(Fore.BLUE + f"Introduce el stock de {producto}: "))
        precio = float(input(Fore.BLUE + f"Introduce el precio de {producto}: "))
        agregar_productos(producto, stock, precio)
    elif inicio == "2":
        actualizar_producto()
    elif inicio == "3":
        leer_productos()
    elif inicio == "4":
        eliminar()
    elif inicio == "5":
        umbral = int(input(Fore.BLUE + "Introduce el umbral de bajo stock (por defecto es 5): ") or 5)
        reporte_bajo_stock(umbral)
    elif inicio == "6":
        print(Fore.GREEN + "¡Adiós! Gracias por usar el sistema.")
        break
    else:
        print(Fore.RED + "Opción no válida. Intente de nuevo.")