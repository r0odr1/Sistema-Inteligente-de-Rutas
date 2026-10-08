import joblib
import pandas as pd

from ml.configuracion import (
    RUTA_MODELO,
    COLUMNAS_ENTRADA,
)


def predecir_ruta(datos_ruta):
    """
    Clasifica una ruta utilizando el modelo entrenado.

    Devuelve:
        0 = No recomendada
        1 = Recomendada
    """
    if not RUTA_MODELO.exists():
        raise FileNotFoundError("No existe el modelo entrenado. Ejecuta primero: py -m ml.entrenar_modelo")

    paquete = joblib.load(RUTA_MODELO)
    modelo = paquete["modelo"]
    columnas = paquete["columnas"]

    if columnas != COLUMNAS_ENTRADA:
        raise ValueError("Las columnas del modelo no coinciden.")

    ruta = pd.DataFrame([datos_ruta], columns=COLUMNAS_ENTRADA)

    if ruta.isnull().any().any():
        raise ValueError("Faltan características de la ruta.")

    return int(modelo.predict(ruta)[0])


def main():
    nueva_ruta = {
        "distancia_km": 13,
        "numero_estaciones": 8,
        "numero_transbordos": 1,
        "nivel_congestion": 2,
        "tiempo_estimado_min": 33,
        "costo_estimado": 24,
        "hora_pico": 1,
    }

    resultado = predecir_ruta(nueva_ruta)

    print("=" * 50)
    print(" PREDICCIÓN DE NUEVA RUTA")
    print("=" * 50)

    print("\nDatos de la ruta:")
    for clave, valor in nueva_ruta.items():
        print(f"{clave}: {valor}")

    if resultado == 1:
        print("\nResultado: RUTA RECOMENDADA")
    else:
        print("\nResultado: RUTA NO RECOMENDADA")

if __name__ == "__main__":
    main()