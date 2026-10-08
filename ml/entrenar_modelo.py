import matplotlib
matplotlib.use("Agg")

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

from ml.configuracion import (
    RUTA_DATOS,
    RUTA_GRAFICAS,
    RUTA_MODELOS,
    RUTA_MODELO,
    COLUMNAS_ENTRADA,
    COLUMNA_OBJETIVO,
    CLASES,
    SEMILLA,
    PROPORCION_PRUEBA,
    PROFUNDIDAD_MAXIMA,
)

# --------------------------------------------------
# 1. CARGAR Y VALIDAR LOS DATOS
# --------------------------------------------------

def cargar_datos():
    datos = pd.read_csv(RUTA_DATOS)
    columnas = COLUMNAS_ENTRADA + [COLUMNA_OBJETIVO]

    faltantes = set(columnas) - set(datos.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas: {sorted(faltantes)}")

    if datos[columnas].isnull().any().any():
        raise ValueError("El dataset contiene valores nulos.")

    if not set(datos[COLUMNA_OBJETIVO].unique()).issubset({0, 1}):
        raise ValueError("La etiqueta debe contener únicamente 0 y 1.")

    return datos

# --------------------------------------------------
# 2. ENTRENAMIENTO Y EVALUACIÓN
# --------------------------------------------------

def entrenar_modelo(datos):
    X = datos[COLUMNAS_ENTRADA]
    y = datos[COLUMNA_OBJETIVO]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=PROPORCION_PRUEBA,
        random_state=SEMILLA,
        stratify=y,
    )

    modelo = DecisionTreeClassifier(
        max_depth=PROFUNDIDAD_MAXIMA,
        random_state=SEMILLA,
    )

    modelo.fit(X_train, y_train)

    predicciones = modelo.predict(X_test)
    exactitud = accuracy_score(y_test, predicciones)

    matriz = confusion_matrix(
        y_test,
        predicciones,
        labels=[0, 1],
    )

    print("=" * 60)
    print(" MODELO SUPERVISADO - ÁRBOL DE DECISIÓN")
    print("=" * 60)
    print(f"\nRegistros totales: {len(datos)}")
    print(f"Entrenamiento: {len(X_train)}")
    print(f"Prueba: {len(X_test)}")
    print(f"\nExactitud: {exactitud * 100:.2f}%")
    print("\nMatriz de confusión:")
    print(matriz)

    print("\nReporte de clasificación:")
    print(classification_report(
        y_test,
        predicciones,
        labels=[0, 1],
        target_names=CLASES,
        zero_division=0,
    ))

    return modelo, matriz, exactitud

# --------------------------------------------------
# 3. GENERACIÓN DE GRÁFICAS
# --------------------------------------------------

def generar_graficas(modelo, matriz, datos):
    RUTA_GRAFICAS.mkdir(
        parents=True,
        exist_ok=True
    )

    # Gráfica 1: Árbol de decisión
    fig, ax = plt.subplots(figsize=(20, 11))

    plot_tree(
        modelo,
        feature_names=COLUMNAS_ENTRADA,
        class_names=CLASES,
        filled=True,
        rounded=True,
        fontsize=8,
        ax=ax,
    )

    ax.set_title("Árbol de decisión - Clasificación de rutas")
    fig.tight_layout()
    fig.savefig(
        RUTA_GRAFICAS / "arbol_decision.png",
        dpi=250,
        bbox_inches="tight",
    )
    plt.close(fig)

    # Gráfica 2: Matriz de confusión
    fig, ax = plt.subplots(figsize=(8, 6))

    disp = ConfusionMatrixDisplay(
        confusion_matrix=matriz,
        display_labels=CLASES,
    )

    disp.plot(ax=ax, cmap="Blues")
    ax.set_title("Matriz de confusión")

    fig.tight_layout()
    fig.savefig(
        RUTA_GRAFICAS / "matriz_confusion.png",
        dpi=250,
        bbox_inches="tight",
    )
    plt.close(fig)

    # Gráfica 3: Rutas según hora pico
    resumen = (
        datos.groupby("hora_pico")[COLUMNA_OBJETIVO]
        .value_counts()
        .unstack(fill_value=0)
        .reindex(
            index=[0, 1],
            columns=[0, 1],
            fill_value=0,
        )
    )

    resumen.index = ["Fuera de hora pico", "Hora pico"]
    resumen.columns = CLASES

    ax = resumen.plot(
        kind="bar",
        figsize=(10, 6),
    )

    ax.set_title("Rutas recomendadas según hora pico")
    ax.set_xlabel("Periodo")
    ax.set_ylabel("Cantidad de rutas")
    ax.tick_params(axis="x", rotation=0)
    ax.legend(title="Clasificación")

    fig = ax.figure
    fig.tight_layout()
    fig.savefig(
        RUTA_GRAFICAS / "rutas_hora_pico.png",
        dpi=250,
        bbox_inches="tight",
    )
    plt.close(fig)

    # Gráfica 4: Importancia de características
    importancias = pd.Series(modelo.feature_importances_, index=COLUMNAS_ENTRADA).sort_values()

    fig, ax = plt.subplots(figsize=(11, 6))
    importancias.plot(kind="barh", ax=ax)

    ax.set_title("Importancia de características del modelo")
    ax.set_xlabel("Importancia relativa")
    ax.set_ylabel("Característica")

    fig.tight_layout()
    fig.savefig(
        RUTA_GRAFICAS / "importancia_caracteristicas.png",
        dpi=250,
        bbox_inches="tight",
    )
    plt.close(fig)

    print("\nImportancia de características:")
    print(importancias.sort_values(ascending=False))

    print(f"\nGráficas guardadas en: {RUTA_GRAFICAS}")

# --------------------------------------------------
# 4. EJECUCIÓN PRINCIPAL
# --------------------------------------------------

def main():
    datos = cargar_datos()

    modelo, matriz, exactitud = entrenar_modelo(datos)

    generar_graficas(
        modelo,
        matriz,
        datos,
    )

    # Modelo final: se entrena con todos los datos
    # después de evaluar el modelo de prueba.
    modelo_final = DecisionTreeClassifier(max_depth=PROFUNDIDAD_MAXIMA,  random_state=SEMILLA)

    modelo_final.fit(datos[COLUMNAS_ENTRADA], datos[COLUMNA_OBJETIVO])

    RUTA_MODELOS.mkdir(parents=True, exist_ok=True)

    joblib.dump(
        {
            "modelo": modelo_final,
            "columnas": COLUMNAS_ENTRADA,
        },
        RUTA_MODELO,
    )

    print(f"\nModelo final guardado en: {RUTA_MODELO}")
    print(f"Exactitud de evaluación: {exactitud:.4f}")

if __name__ == "__main__":
    main()