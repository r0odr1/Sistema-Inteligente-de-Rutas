
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

RUTA_DATOS = RAIZ / "datos" / "rutas_transporte.csv"
RUTA_GRAFICAS = RAIZ / "graficas"
RUTA_MODELOS = RAIZ / "modelos"
RUTA_MODELO = RUTA_MODELOS / "modelo_rutas.joblib"

COLUMNAS_ENTRADA = [
    "distancia_km",
    "numero_estaciones",
    "numero_transbordos",
    "nivel_congestion",
    "tiempo_estimado_min",
    "costo_estimado",
    "hora_pico",
]

COLUMNA_OBJETIVO = "ruta_recomendada"

CLASES = [
    "No recomendada",
    "Recomendada",
]

SEMILLA = 42
PROPORCION_PRUEBA = 0.30
PROFUNDIDAD_MAXIMA = 4
