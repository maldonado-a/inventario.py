import tkinter as tk
from tkinter import messagebox, ttk
import json
import inventario
import validaciones

ventana = tk.Tk()
ventana.title("Sistema de Gestión de Inventarios")
ventana.geometry("900x600")

vcmd_letras = ventana.register(validaciones.validar_letras)
vcmd_numeros = ventana.register(validaciones.validar_entero)
vcmd_busqueda_letras = ventana.register(validaciones.validar_busqueda_letras)

def mostrar_toast(mensaje, duracion=2000):
    toast = tk.Toplevel(ventana)
    toast.wm_overrideredirect(True)
    x = ventana.winfo_x() + ventana.winfo_width() // 2
    y = ventana.winfo_y() + ventana.winfo_height() // 2
    toast.geometry(f"+{x-100}+{y-50}")
    toast.configure(bg="black")
    tk.Label(toast, text=mensaje, bg="black", fg="white", padx=10, pady=5).pack()
    toast.after(duracion, toast.destroy)

def agregar_producto():
    nombre = nombre_entry.get()
    cantidad = cantidad_entry.get()
    precio = precio_entry.get()

    if not nombre or not cantidad or not precio:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    if not validaciones.validar_letras(nombre):
        messagebox.showerror("Error", "El nombre del producto solo debe contener letras y espacios.")
        return

    if not validaciones.validar_entero(cantidad) or not validaciones.validar_entero(precio):
        messagebox.showerror("Error", "La cantidad y el precio deben ser números enteros.")
        return

    if any(producto[0] == nombre for producto in inventario.inventario):
        messagebox.showerror("Error", "El producto ya existe en el inventario.")
        return

    if messagebox.askyesno("Confirmar", "¿Desea agregar este producto al inventario?"):
        inventario.agregar_producto(nombre, int(cantidad), int(precio))
        actualizar_inventario()
        mostrar_toast("Producto agregado exitosamente")
        nombre_entry.focus()

def eliminar_producto(nombre):
    if messagebox.askyesno("Confirmar", f"¿Desea eliminar el producto '{nombre}' del inventario?"):
        inventario.eliminar_producto(nombre)
        actualizar_inventario()
        mostrar_toast("Producto eliminado exitosamente")

def modificar_producto():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Debe seleccionar un producto para modificarlo.")
        return

    nombre_antiguo = tree.item(selected_item, "values")[0]
    nuevo_nombre = nombre_modificar_entry.get()
    nueva_cantidad = cantidad_modificar_entry.get()
    nuevo_precio = precio_modificar_entry.get()

    if not nuevo_nombre or not nueva_cantidad or not nuevo_precio:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    if not validaciones.validar_letras(nuevo_nombre):
        messagebox.showerror("Error", "El nombre del producto solo debe contener letras y espacios.")
        return

    if not validaciones.validar_entero(nueva_cantidad) or not validaciones.validar_entero(nuevo_precio):
        messagebox.showerror("Error", "La cantidad y el precio deben ser números enteros.")
        return

    if int(nueva_cantidad) < 0:
        messagebox.showerror("Error", "La cantidad no puede ser negativa.")
        return

    # Verificar si el nuevo nombre ya existe en el inventario
    if any(producto[0] != nombre_antiguo and producto[0] == nuevo_nombre for producto in inventario.inventario):
        messagebox.showerror("Error", "El nombre del producto ya existe en el inventario.")
        return

    # Verificar si los nuevos datos ya existen en el inventario
    for producto in inventario.inventario:
        if producto[0] == nuevo_nombre and producto[1] == int(nueva_cantidad) and producto[2] == int(nuevo_precio):
            messagebox.showerror("Error", "El producto con estos datos ya existe en el inventario.")
            return

    if messagebox.askyesno("Confirmar", f"¿Desea modificar el producto '{nombre_antiguo}' con la nueva información?"):
        inventario.modificar_producto(nombre_antiguo, nuevo_nombre, int(nueva_cantidad), int(nuevo_precio))
        actualizar_inventario()
        mostrar_toast("Producto modificado exitosamente")

def calcular_valor_total():
    valor_total = inventario.calcular_valor_total()
    messagebox.showinfo("Valor Total", f"El valor total del inventario es: ${valor_total:.2f}")

def actualizar_inventario():
    for row in tree.get_children():
        tree.delete(row)
    for producto in inventario.inventario:
        tree.insert("", "end", values=(producto[0], producto[1], f"${producto[2]:.2f}", "🗑️"))
    mostrar_total_inventario()

def mostrar_total_inventario():
    valor_total = inventario.calcular_valor_total()
    total_label.config(text=f"Total Inventario: ${valor_total:.2f}")

def on_tree_click(event):
    item = tree.identify('item', event.x, event.y)
    column = tree.identify_column(event.x)
    if item and column == "#4":  # Suponiendo que la columna de eliminar es la cuarta
        nombre = tree.item(item, "values")[0]
        eliminar_producto(nombre)
    elif item:
        producto = tree.item(item, "values")
        nombre_modificar_entry.delete(0, tk.END)
        nombre_modificar_entry.insert(0, producto[0])
        cantidad_modificar_entry.delete(0, tk.END)
        cantidad_modificar_entry.insert(0, producto[1])
        precio_modificar_entry.delete(0, tk.END)
        precio_modificar_entry.insert(0, producto[2].replace('$', ''))

def buscar_producto():
    busqueda = busqueda_entry.get().lower()
    productos_encontrados = False
    for item in tree.get_children():
        tree.delete(item)
    for producto in inventario.inventario:
        if busqueda in producto[0].lower():
            tree.insert("", "end", values=(producto[0], producto[1], f"${producto[2]:.2f}", "🗑️"))
            productos_encontrados = True
    if not productos_encontrados:
        messagebox.showinfo("Búsqueda", "No se encontraron productos con ese nombre.")

frame_titulo = tk.Frame(ventana, pady=10)
frame_titulo.place(relx=0.5, rely=0.05, anchor=tk.N)
titulo_label = tk.Label(frame_titulo, text="Gestión de Inventario", font=("Arial", 14, "bold"))
titulo_label.pack()

frame_busqueda = tk.Frame(ventana, padx=5, pady=5)
frame_busqueda.place(relx=0.5, rely=0.1, anchor=tk.N)
tk.Label(frame_busqueda, text="Buscar producto:").pack(side=tk.LEFT, padx=5)
busqueda_entry = tk.Entry(frame_busqueda, validate="key", validatecommand=(vcmd_busqueda_letras, '%S'), width=20)
busqueda_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
buscar_btn = tk.Button(frame_busqueda, text="Buscar", command=buscar_producto, bg="orange", fg="white")
buscar_btn.pack(side=tk.LEFT, padx=5)

frame_agregar = tk.Frame(ventana, padx=5, pady=5)
frame_agregar.place(relx=0.5, rely=0.2, anchor=tk.N)
tk.Label(frame_agregar, text="Nombre del producto:").pack(side=tk.LEFT, padx=5)
nombre_entry = tk.Entry(frame_agregar, validate="key", validatecommand=(vcmd_letras, '%S'), width=20)
nombre_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

tk.Label(frame_agregar, text="Cantidad:").pack(side=tk.LEFT, padx=5)
cantidad_entry = tk.Entry(frame_agregar, validate="key", validatecommand=(vcmd_numeros, '%S'), width=10)
cantidad_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

tk.Label(frame_agregar, text="Precio:").pack(side=tk.LEFT, padx=5)
precio_entry = tk.Entry(frame_agregar, validate="key", validatecommand=(vcmd_numeros, '%S'), width=10)
precio_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

agregar_btn = tk.Button(frame_agregar, text="Agregar Producto", command=agregar_producto, bg="green", fg="white")
agregar_btn.pack(side=tk.LEFT, padx=5)

frame_inventario = tk.Frame(ventana, padx=5, pady=5)
frame_inventario.place(relx=0.5, rely=0.4, anchor=tk.N)
columns = ("Nombre", "Cantidad", "Precio", "Eliminar")
tree = ttk.Treeview(frame_inventario, columns=columns, show="headings", selectmode="browse")
tree.heading("Nombre", text="Nombre", anchor=tk.CENTER)
tree.heading("Cantidad", text="Cantidad", anchor=tk.CENTER)
tree.heading("Precio", text="Precio", anchor=tk.CENTER)
tree.heading("Eliminar", text="Eliminar", anchor=tk.CENTER)
tree.column("Nombre", anchor=tk.CENTER, width=300)
tree.column("Cantidad", anchor=tk.CENTER, width=300)
tree.column("Precio", anchor=tk.CENTER, width=300)
tree.column("Eliminar", anchor=tk.CENTER, width=300)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
tree.bind("<Button-1>", on_tree_click)

scroll_y = tk.Scrollbar(frame_inventario, orient=tk.VERTICAL, command=tree.yview)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scroll_y.set)

frame_acciones = tk.Frame(ventana, padx=5, pady=5)
frame_acciones.place(relx=0.5, rely=0.7, anchor=tk.N)
tk.Label(frame_acciones, text="Modificar nombre:").pack(side=tk.LEFT, padx=5)
nombre_modificar_entry = tk.Entry(frame_acciones, validate="key", validatecommand=(vcmd_letras, '%S'), width=20)
nombre_modificar_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

tk.Label(frame_acciones, text="Modificar cantidad:").pack(side=tk.LEFT, padx=5)
cantidad_modificar_entry = tk.Entry(frame_acciones, validate="key", validatecommand=(vcmd_numeros, '%S'), width=10)
cantidad_modificar_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

tk.Label(frame_acciones, text="Modificar precio:").pack(side=tk.LEFT, padx=5)
precio_modificar_entry = tk.Entry(frame_acciones, validate="key", validatecommand=(vcmd_numeros, '%S'), width=10)
precio_modificar_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

modificar_btn = tk.Button(frame_acciones, text="Modificar Producto", command=modificar_producto, bg="blue", fg="white")
modificar_btn.pack(side=tk.LEFT, padx=5)

calcular_btn = tk.Button(frame_acciones, text="Calcular Valor Total", command=calcular_valor_total, bg="purple", fg="white")
calcular_btn.pack(side=tk.LEFT, padx=5)

total_label = tk.Label(ventana, text="Total Inventario: $0.00", font=("Arial", 12))
total_label.place(relx=0.5, rely=0.85, anchor=tk.N)

inventario.cargar_inventario()
actualizar_inventario()

ventana.mainloop()


