import unittest

from conocimiento import GRAFO, COORDENADAS
from reglas import (
    estacion_existe,
    mismo_origen_destino,
    estaciones_conectadas
)
from busqueda import (
    buscar_mejor_ruta,
    calcular_heuristica
)


class TestSistemaInteligente(unittest.TestCase):

    def test_estacion_existente(self):
        """
        Verifica que una estación registrada
        sea reconocida por la base de conocimiento.
        """
        resultado = estacion_existe(
            "Portal Norte",
            GRAFO
        )

        self.assertTrue(resultado)

    def test_estacion_inexistente(self):
        """
        Verifica que una estación desconocida
        sea rechazada.
        """
        resultado = estacion_existe(
            "Estacion Inexistente",
            GRAFO
        )

        self.assertFalse(resultado)

    def test_mismo_origen_destino(self):
        """
        Comprueba la regla que determina si
        origen y destino son iguales.
        """
        resultado = mismo_origen_destino(
            "Portal Norte",
            "Portal Norte"
        )

        self.assertTrue(resultado)

    def test_conexion_directa(self):
        """
        Verifica una relación almacenada
        en la base de conocimiento.
        """
        resultado = estaciones_conectadas(
            "Portal Norte",
            "Calle 127",
            GRAFO
        )

        self.assertTrue(resultado)

    def test_heuristica_destino(self):
        """
        La heurística de una estación respecto
        a ella misma debe ser cero.
        """
        resultado = calcular_heuristica(
            "Portal Sur",
            "Portal Sur",
            COORDENADAS
        )

        self.assertEqual(resultado, 0)

    def test_ruta_portal_sur_portal_norte(self):
        """
        Verifica la búsqueda A* entre
        Portal Sur y Portal Norte.
        """
        ruta, costo = buscar_mejor_ruta(
            GRAFO,
            "Portal Sur",
            "Portal Norte",
            COORDENADAS
        )

        self.assertEqual(
            ruta[0],
            "Portal Sur"
        )

        self.assertEqual(
            ruta[-1],
            "Portal Norte"
        )

        self.assertEqual(
            costo,
            37
        )

    def test_ruta_suba_americas(self):
        """
        Verifica la ruta utilizada en nuestro
        segundo caso de prueba.
        """
        ruta, costo = buscar_mejor_ruta(
            GRAFO,
            "Portal Suba",
            "Portal Americas",
            COORDENADAS
        )

        self.assertEqual(
            ruta[0],
            "Portal Suba"
        )

        self.assertEqual(
            ruta[-1],
            "Portal Americas"
        )

        self.assertEqual(
            costo,
            39
        )


if __name__ == "__main__":
    unittest.main()