import pandas as pd

from sklearn.tree import DecisionTreeClassifier


datos = pd.read_csv(
    "datos/rutas_transporte.csv"
)


X = datos[
    [
        "distancia_km",
        "numero_estaciones",
        "numero_transbordos",
        "nivel_congestion",
        "tiempo_estimado_min",
        "costo_estimado"
    ]
]

y = datos["ruta_recomendada"]


modelo = DecisionTreeClassifier(
    max_depth=4,
    random_state=42
)

modelo.fit(X, y)


nueva_ruta = pd.DataFrame(
    [
        {
            "distancia_km": 13,
            "numero_estaciones": 8,
            "numero_transbordos": 1,
            "nivel_congestion": 2,
            "tiempo_estimado_min": 33,
            "costo_estimado": 24
        }
    ]
)


prediccion = modelo.predict(
    nueva_ruta
)


print("=" * 50)
print(" PREDICCIÓN DE NUEVA RUTA")
print("=" * 50)

print("\nDatos de la ruta:")
print(nueva_ruta)

if prediccion[0] == 1:
    print(
        "\nResultado: RUTA RECOMENDADA"
    )
else:
    print(
        "\nResultado: RUTA NO RECOMENDADA"
    )