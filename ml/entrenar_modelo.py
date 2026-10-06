import os

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


# --------------------------------------------------
# 1. CARGAR LOS DATOS
# --------------------------------------------------

datos = pd.read_csv(
    "datos/rutas_transporte.csv"
)

print("=" * 60)
print(" MODELO SUPERVISADO - ÁRBOL DE DECISIÓN")
print("=" * 60)

print("\nCantidad total de registros:", len(datos))


# --------------------------------------------------
# 2. DEFINIR VARIABLES DE ENTRADA Y SALIDA
# --------------------------------------------------

columnas_entrada = [
    "distancia_km",
    "numero_estaciones",
    "numero_transbordos",
    "nivel_congestion",
    "tiempo_estimado_min",
    "costo_estimado"
]

X = datos[columnas_entrada]

# Variable objetivo
y = datos["ruta_recomendada"]


# --------------------------------------------------
# 3. DIVIDIR DATOS
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

print("\nDatos de entrenamiento:", len(X_train))
print("Datos de prueba:", len(X_test))


# --------------------------------------------------
# 4. CREAR Y ENTRENAR EL MODELO
# --------------------------------------------------

modelo = DecisionTreeClassifier(
    max_depth=4,
    random_state=42
)

modelo.fit(
    X_train,
    y_train
)


# --------------------------------------------------
# 5. REALIZAR PREDICCIONES
# --------------------------------------------------

predicciones = modelo.predict(
    X_test
)


# --------------------------------------------------
# 6. EVALUAR EL MODELO
# --------------------------------------------------

precision = accuracy_score(
    y_test,
    predicciones
)

matriz = confusion_matrix(
    y_test,
    predicciones
)

print("\n" + "=" * 60)
print(" RESULTADOS")
print("=" * 60)

print(
    f"\nPrecisión del modelo: "
    f"{precision * 100:.2f}%"
)

print("\nMatriz de confusión:")
print(matriz)

print("\nReporte de clasificación:")

print(
    classification_report(
        y_test,
        predicciones,
        target_names=[
            "No recomendada",
            "Recomendada"
        ]
    )
)


# --------------------------------------------------
# 7. CREAR CARPETA PARA GRÁFICAS
# --------------------------------------------------

os.makedirs(
    "graficas",
    exist_ok=True
)


# --------------------------------------------------
# 8. GRÁFICA DEL ÁRBOL DE DECISIÓN
# --------------------------------------------------

plt.figure(
    figsize=(18, 10)
)

plot_tree(
    modelo,
    feature_names=columnas_entrada,
    class_names=[
        "No recomendada",
        "Recomendada"
    ],
    filled=True,
    rounded=True,
    fontsize=9
)

plt.title(
    "Árbol de decisión - Clasificación de rutas"
)

plt.tight_layout()

plt.savefig(
    "graficas/arbol_decision.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# --------------------------------------------------
# 9. MATRIZ DE CONFUSIÓN
# --------------------------------------------------

disp = ConfusionMatrixDisplay(
    confusion_matrix=matriz,
    display_labels=[
        "No recomendada",
        "Recomendada"
    ]
)

disp.plot(
    cmap="Blues"
)

plt.title(
    "Matriz de confusión"
)

plt.tight_layout()

plt.savefig(
    "graficas/matriz_confusion.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()