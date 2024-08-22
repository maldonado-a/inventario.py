# validaciones.py

import re

def validar_letras(valor):
    """Permite letras y espacios"""
    return bool(re.match(r"^[A-Za-z\s]+$", valor))

def validar_entero(valor):
    """Permite números enteros positivos"""
    return valor.isdigit()
    
def validar_busqueda_letras(valor):
    """Permite letras y espacios para búsqueda"""
    return bool(re.match(r"^[A-Za-z\s]*$", valor))

