# conocimiento.py

"""
Base de conocimiento del sistema inteligente de transporte.

Cada estación representa un nodo del grafo.
Las conexiones representan las posibles rutas entre estaciones.
El valor asociado representa el costo estimado del recorrido.
"""

GRAFO = {
    "Portal Norte": {
        "Calle 127": 4
    },

    "Calle 127": {
        "Portal Norte": 4,
        "Calle 100": 3
    },

    "Calle 100": {
        "Calle 127": 3,
        "Calle 72": 4,
        "Suba Calle 100": 5
    },

    "Calle 72": {
        "Calle 100": 4,
        "Calle 63": 2
    },

    "Calle 63": {
        "Calle 72": 2,
        "Calle 45": 3
    },

    "Calle 45": {
        "Calle 63": 3,
        "Calle 26": 4
    },

    "Calle 26": {
        "Calle 45": 4,
        "Avenida Jimenez": 3
    },

    "Avenida Jimenez": {
        "Calle 26": 3,
        "Tercer Milenio": 3,
        "Ricaurte": 4
    },

    "Tercer Milenio": {
        "Avenida Jimenez": 3,
        "NQS Calle 30 Sur": 5
    },

    "NQS Calle 30 Sur": {
        "Tercer Milenio": 5,
        "Portal Sur": 6
    },

    "Portal Sur": {
        "NQS Calle 30 Sur": 6
    },

    "Suba Calle 100": {
        "Calle 100": 5,
        "Portal Suba": 6
    },

    "Portal Suba": {
        "Suba Calle 100": 6
    },

    "Ricaurte": {
        "Avenida Jimenez": 4,
        "Portal Americas": 8
    },

    "Portal Americas": {
        "Ricaurte": 8
    }
}


# Coordenadas simplificadas de las estaciones.
# Se utilizan para calcular dinámicamente la heurística de A*.
#
# IMPORTANTE:
# Estas coordenadas representan posiciones relativas dentro
# del modelo académico y no coordenadas geográficas reales.

COORDENADAS = {
    "Portal Norte": (5, 30),
    "Calle 127": (5, 27),
    "Calle 100": (5, 24),
    "Calle 72": (5, 20),
    "Calle 63": (5, 18),
    "Calle 45": (5, 15),
    "Calle 26": (5, 12),
    "Avenida Jimenez": (5, 9),
    "Tercer Milenio": (5, 7),
    "NQS Calle 30 Sur": (5, 4),
    "Portal Sur": (5, 0),

    # Ramal hacia Suba
    "Suba Calle 100": (1, 24),
    "Portal Suba": (-4, 25),

    # Ramal hacia Americas
    "Ricaurte": (2, 9),
    "Portal Americas": (-5, 7)
}