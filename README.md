# Sistema de Gestión de Inventarios

Este es un sistema de gestión de inventarios desarrollado en Python utilizando Tkinter para la interfaz gráfica. Permite agregar, eliminar y modificar productos, así como calcular el valor total del inventario.

## Características

- **Agregar Productos**: Añade nuevos productos al inventario con nombre, cantidad y precio.
- **Eliminar Productos**: Elimina productos del inventario.
- **Modificar Productos**: Actualiza la información de productos existentes.
- **Buscar Productos**: Encuentra productos por nombre.
- **Calcular Valor Total**: Calcula el valor total del inventario en base a los productos actuales.
- **Visualización**: Muestra el inventario en una tabla con opciones para eliminar productos.


*Estructura del Código*
**main.py**: Contiene la lógica principal de la aplicación y gestiona eventos como agregar, eliminar y modificar productos.
**interfaz.py**: Configura la interfaz gráfica, incluyendo la creación de ventanas, botones, entradas y la tabla de inventario.
**validaciones.py**: Proporciona funciones de validación para asegurarse de que los datos ingresados sean correctos (letras para nombres y números para cantidades y precios).
**inventario.py**: Maneja la lógica relacionada con el inventario, incluyendo agregar, eliminar, modificar productos y calcular el valor total del inventario.
