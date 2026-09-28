# reglas.py

"""
Reglas lógicas utilizadas por el sistema inteligente.
"""


def estacion_existe(estacion, grafo):
    """
    Regla 1:
    SI la estación pertenece a la base de conocimiento
    ENTONCES la estación es válida.
    """
    return estacion in grafo


def mismo_origen_destino(origen, destino):
    """
    Regla 2:
    SI origen y destino son iguales
    ENTONCES no es necesario realizar recorrido.
    """
    return origen == destino


def estaciones_conectadas(origen, destino, grafo):
    """
    Regla 3:
    SI destino pertenece a los vecinos del origen
    ENTONCES existe una conexión directa.
    """
    return destino in grafo.get(origen, {})


def obtener_conexiones(estacion, grafo):
    """
    Regla 4:
    SI una estación existe
    ENTONCES se pueden consultar sus conexiones.
    """
    return grafo.get(estacion, {})