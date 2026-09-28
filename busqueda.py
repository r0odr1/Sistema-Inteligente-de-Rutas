import heapq
import math

from reglas import obtener_conexiones


def calcular_heuristica(estacion, destino, coordenadas):
    """
    Calcula la distancia euclidiana entre la estación actual
    y la estación destino.

    Esta distancia funciona como heurística h(n) para A*.
    """

    x1, y1 = coordenadas[estacion]
    x2, y2 = coordenadas[destino]

    distancia = math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )

    return distancia


def buscar_mejor_ruta(
    grafo,
    origen,
    destino,
    coordenadas,
    mostrar_proceso=False
):
    """
    Algoritmo de búsqueda heurística A*.

    f(n) = g(n) + h(n)

    g(n): costo real acumulado desde el origen.
    h(n): estimación desde el nodo actual hasta el destino.
    f(n): costo total estimado.
    """

    cola_prioridad = []

    heuristica_inicial = calcular_heuristica(
        origen,
        destino,
        coordenadas
    )

    # Elementos de la cola:
    # (f, g, estacion, ruta)

    heapq.heappush(
        cola_prioridad,
        (
            heuristica_inicial,
            0,
            origen,
            [origen]
        )
    )

    mejor_costo = {
        origen: 0
    }

    while cola_prioridad:

        (
            f_actual,
            costo_actual,
            estacion_actual,
            ruta
        ) = heapq.heappop(cola_prioridad)

        # Ignorar una entrada antigua si ya conocemos
        # una forma más económica de llegar a la estación.
        if costo_actual > mejor_costo.get(
            estacion_actual,
            float("inf")
        ):
            continue

        if mostrar_proceso:
            h_actual = calcular_heuristica(
                estacion_actual,
                destino,
                coordenadas
            )

            print("\n----------------------------------------")
            print(f"Analizando: {estacion_actual}")
            print(f"g(n) = {costo_actual:.2f}")
            print(f"h(n) = {h_actual:.2f}")
            print(f"f(n) = {f_actual:.2f}")

        # Regla de objetivo
        if estacion_actual == destino:

            if mostrar_proceso:
                print("\nDestino alcanzado.")

            return ruta, costo_actual

        conexiones = obtener_conexiones(
            estacion_actual,
            grafo
        )

        for vecino, costo_movimiento in conexiones.items():

            nuevo_costo = (
                costo_actual +
                costo_movimiento
            )

            costo_anterior = mejor_costo.get(
                vecino,
                float("inf")
            )

            # Solo consideramos la nueva ruta si mejora
            # el costo conocido para llegar al vecino.
            if nuevo_costo < costo_anterior:

                mejor_costo[vecino] = nuevo_costo

                h = calcular_heuristica(
                    vecino,
                    destino,
                    coordenadas
                )

                f = nuevo_costo + h

                nueva_ruta = ruta + [vecino]

                heapq.heappush(
                    cola_prioridad,
                    (
                        f,
                        nuevo_costo,
                        vecino,
                        nueva_ruta
                    )
                )

                if mostrar_proceso:
                    print(f"\n  Posible movimiento → {vecino}")
                    print(
                        f"  Costo del movimiento: "
                        f"{costo_movimiento}"
                    )
                    print(
                        f"  g(n) acumulado: "
                        f"{nuevo_costo:.2f}"
                    )
                    print(
                        f"  h(n) estimado: "
                        f"{h:.2f}"
                    )
                    print(
                        f"  f(n) = g(n) + h(n): "
                        f"{f:.2f}"
                    )

    return None, None