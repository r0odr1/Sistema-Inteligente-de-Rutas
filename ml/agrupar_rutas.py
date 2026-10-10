import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

from ml.configuracion import RUTA_DATOS


COLUMNAS_AGRUPAMIENTO = [
    "distancia_km",
    "numero_estaciones",
    "numero_transbordos",
    "nivel_congestion",
    "tiempo_estimado_min",
    "costo_estimado",
    "hora_pico",
]

RANGO_K = range(2, 7)

K_SELECCIONADO = 2


def cargar_datos():
    """Carga y valida el dataset utilizado para K-Means."""

    datos = pd.read_csv(RUTA_DATOS)

    faltantes = set(COLUMNAS_AGRUPAMIENTO) - set(datos.columns)

    if faltantes:
        raise ValueError(
            f"Faltan columnas para agrupamiento: {sorted(faltantes)}"
        )

    if datos[COLUMNAS_AGRUPAMIENTO].isnull().any().any():
        raise ValueError(
            "El dataset contiene valores nulos en las variables de agrupamiento."
        )

    return datos


def preparar_datos(datos):
    """Estandariza las variables utilizadas por K-Means."""

    escalador = StandardScaler()

    datos_estandarizados = escalador.fit_transform(
        datos[COLUMNAS_AGRUPAMIENTO]
    )

    return datos_estandarizados, escalador


def evaluar_k(datos_estandarizados):
    """Evalúa diferentes cantidades de clusters."""

    resultados = []

    for k in RANGO_K:
        modelo = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=20
        )

        etiquetas = modelo.fit_predict(datos_estandarizados)

        silueta = silhouette_score(
            datos_estandarizados,
            etiquetas
        )

        resultados.append({
            "k": k,
            "inercia": modelo.inertia_,
            "silueta": silueta
        })

    return resultados


def generar_grafica_codo(resultados):
    """Genera la gráfica del método del codo."""

    valores_k = [resultado["k"] for resultado in resultados]
    inercias = [resultado["inercia"] for resultado in resultados]

    plt.figure(figsize=(8, 5))

    plt.plot(
        valores_k,
        inercias,
        marker="o"
    )

    plt.title("Método del codo - K-Means")
    plt.xlabel("Número de clusters (K)")
    plt.ylabel("Inercia")

    plt.xticks(valores_k)
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "graficas/metodo_codo.png",
        dpi=300
    )

    plt.show()

    plt.close()


def generar_grafica_silueta(resultados):
    """Genera la gráfica del coeficiente de Silhouette."""

    valores_k = [resultado["k"] for resultado in resultados]
    valores_silueta = [
        resultado["silueta"]
        for resultado in resultados
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        valores_k,
        valores_silueta,
        marker="o"
    )

    plt.title("Coeficiente de Silhouette - K-Means")
    plt.xlabel("Número de clusters (K)")
    plt.ylabel("Coeficiente de Silhouette")

    plt.xticks(valores_k)
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "graficas/silhouette_clusters.png",
        dpi=300
    )

    plt.show()

    plt.close()


def crear_perfil_clusters(datos, etiquetas):
    """Calcula el perfil medio de cada cluster."""

    datos_perfil = datos[COLUMNAS_AGRUPAMIENTO].copy()

    datos_perfil["cluster"] = etiquetas

    perfil = (
        datos_perfil
        .groupby("cluster")
        .mean()
        .round(2)
    )

    return perfil


def guardar_resultados(datos, etiquetas):
    """Guarda el dataset original junto con el cluster asignado."""

    datos_resultado = datos.copy()

    datos_resultado["cluster"] = etiquetas

    datos_resultado.to_csv(
        "datos/rutas_agrupadas.csv",
        index=False
    )


def generar_grafica_clusters(datos_estandarizados, etiquetas):
    """Reduce las variables a dos componentes y visualiza los clusters."""

    pca = PCA(n_components=2)

    datos_pca = pca.fit_transform(
        datos_estandarizados
    )

    plt.figure(figsize=(8, 5))

    plt.scatter(
        datos_pca[:, 0],
        datos_pca[:, 1],
        c=etiquetas,
        cmap="viridis",
        alpha=0.7
    )

    plt.title("Visualización de clusters mediante PCA")
    plt.xlabel("Componente principal 1")
    plt.ylabel("Componente principal 2")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "graficas/clusters_rutas.png",
        dpi=300
    )

    plt.show()

    plt.close()


def entrenar_agrupamiento(datos_estandarizados):
    """Entrena el modelo K-Means con el número de clusters seleccionado."""

    modelo = KMeans(
        n_clusters=K_SELECCIONADO,
        random_state=42,
        n_init=20
    )

    etiquetas = modelo.fit_predict(
        datos_estandarizados
    )

    return modelo, etiquetas


if __name__ == "__main__":
    datos = cargar_datos()

    datos_estandarizados, escalador = preparar_datos(
        datos
    )

    resultados = evaluar_k(
        datos_estandarizados
    )

    generar_grafica_codo(
        resultados
    )

    generar_grafica_silueta(
        resultados
    )

    modelo, etiquetas = entrenar_agrupamiento(
        datos_estandarizados
    )

    guardar_resultados(
        datos,
        etiquetas
    )

    generar_grafica_clusters(
        datos_estandarizados,
        etiquetas
    )

    perfil_clusters = crear_perfil_clusters(
        datos,
        etiquetas
    )

    print("=" * 60)
    print(" APRENDIZAJE NO SUPERVISADO - K-MEANS")
    print("=" * 60)

    print(
        f"\nRegistros cargados: {len(datos)}"
    )

    print(
        f"Variables utilizadas: "
        f"{len(COLUMNAS_AGRUPAMIENTO)}"
    )

    print("\nColumnas utilizadas:")

    for columna in COLUMNAS_AGRUPAMIENTO:
        print(f" - {columna}")

    print("\nDimensiones de los datos estandarizados:")

    print(
        datos_estandarizados.shape
    )

    print("\nPrimeras 5 filas estandarizadas:")

    print(
        datos_estandarizados[:5]
    )

    print(
        "\nEvaluación de diferentes "
        "cantidades de clusters:"
    )

    for resultado in resultados:
        print(
            f"K={resultado['k']} | "
            f"Inercia={resultado['inercia']:.2f} | "
            f"Silueta={resultado['silueta']:.4f}"
        )

    print("\nPerfil medio de los clusters:")

    print(
        perfil_clusters.to_string()
    )

    print("\nResultados del agrupamiento:")

    print(
        f"Clusters seleccionados: "
        f"{modelo.n_clusters}"
    )

    print("\nCantidad de rutas por cluster:")

    print(
        pd.Series(etiquetas)
        .value_counts()
        .sort_index()
    )

    print(
        "\nDatos preparados y agrupados correctamente."
    )
