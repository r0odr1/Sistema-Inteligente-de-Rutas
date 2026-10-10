import pandas as pd

from ml.agrupar_rutas import (
    COLUMNAS_AGRUPAMIENTO,
    cargar_datos,
    preparar_datos,
    evaluar_k,
    entrenar_agrupamiento,
)


def test_dataset_tiene_170_registros():
    datos = cargar_datos()

    assert len(datos) == 170

def test_existen_columnas_de_agrupamiento():
    datos = cargar_datos()

    for columna in COLUMNAS_AGRUPAMIENTO:
        assert columna in datos.columns

def test_no_hay_valores_nulos():
    datos = cargar_datos()

    assert not datos[COLUMNAS_AGRUPAMIENTO].isnull().any().any()

def test_datos_estandarizados_tienen_dimensiones_correctas():
    datos = cargar_datos()

    datos_estandarizados, _ = preparar_datos(datos)

    assert datos_estandarizados.shape == (170, 7)

def test_se_evaluan_los_valores_de_k():
    datos = cargar_datos()

    datos_estandarizados, _ = preparar_datos(datos)

    resultados = evaluar_k(datos_estandarizados)

    valores_k = [resultado["k"] for resultado in resultados]

    assert valores_k == [2, 3, 4, 5, 6]

def test_kmeans_genera_170_etiquetas():
    datos = cargar_datos()

    datos_estandarizados, _ = preparar_datos(datos)

    modelo, etiquetas = entrenar_agrupamiento(
        datos_estandarizados
    )

    assert modelo.n_clusters == 2
    assert len(etiquetas) == 170

def test_silueta_en_rango_valido():
    datos = cargar_datos()

    datos_estandarizados, _ = preparar_datos(datos)

    resultados = evaluar_k(datos_estandarizados)

    for resultado in resultados:
        assert -1 <= resultado["silueta"] <= 1

def test_no_se_usa_ruta_recomendada():
    assert "ruta_recomendada" not in COLUMNAS_AGRUPAMIENTO
    