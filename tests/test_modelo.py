import unittest

import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from ml.configuracion import (
    RUTA_DATOS,
    COLUMNAS_ENTRADA,
    COLUMNA_OBJETIVO,
)
from ml.entrenar_modelo import cargar_datos

class TestModeloSupervisado(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.datos = cargar_datos()

    def test_dataset_existe(self):
        self.assertTrue(RUTA_DATOS.is_file())

    def test_cantidad_registros(self):
        self.assertEqual(len(self.datos), 170)

    def test_columnas_obligatorias(self):
        columnas = (
            COLUMNAS_ENTRADA + [COLUMNA_OBJETIVO]
        )
        for columna in columnas:
            self.assertIn(columna, self.datos.columns)

    def test_sin_valores_nulos(self):
        columnas = (
            COLUMNAS_ENTRADA + [COLUMNA_OBJETIVO]
        )
        self.assertFalse(
            self.datos[columnas].isnull().any().any()
        )

    def test_etiquetas_validas(self):
        etiquetas = set(
            self.datos[COLUMNA_OBJETIVO].unique()
        )
        self.assertEqual(etiquetas, {0, 1})

    def test_hora_pico_valida(self):
        valores = set(
            self.datos["hora_pico"].unique()
        )
        self.assertTrue(valores.issubset({0, 1}))

    def test_entrenamiento(self):
        X = self.datos[COLUMNAS_ENTRADA]
        y = self.datos[COLUMNA_OBJETIVO]

        modelo = DecisionTreeClassifier(max_depth=4, random_state=42)

        modelo.fit(X, y)

        self.assertEqual(modelo.n_features_in_, len(COLUMNAS_ENTRADA))

    def test_prediccion_valida(self):
        X = self.datos[COLUMNAS_ENTRADA]
        y = self.datos[COLUMNA_OBJETIVO]

        modelo = DecisionTreeClassifier(max_depth=4, random_state=42)

        modelo.fit(X, y)

        nueva_ruta = pd.DataFrame(
            [{
                "distancia_km": 13,
                "numero_estaciones": 8,
                "numero_transbordos": 1,
                "nivel_congestion": 2,
                "tiempo_estimado_min": 33,
                "costo_estimado": 24,
                "hora_pico": 1,
            }]
        )[COLUMNAS_ENTRADA]

        resultado = int(modelo.predict(nueva_ruta)[0])

        self.assertIn(resultado, [0, 1])

if __name__ == "__main__":
    unittest.main()