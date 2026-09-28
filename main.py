# main.py

from conocimiento import GRAFO, COORDENADAS
from reglas import estacion_existe, mismo_origen_destino
from busqueda import buscar_mejor_ruta


def mostrar_estaciones():
    print("\nESTACIONES DISPONIBLES")
    print("-" * 40)

    for numero, estacion in enumerate(GRAFO.keys(), start=1):
        print(f"{numero}. {estacion}")


def seleccionar_estacion(mensaje):

    estaciones = list(GRAFO.keys())

    while True:

        try:

            opcion = int(input(mensaje))

            if 1 <= opcion <= len(estaciones):
                return estaciones[opcion - 1]

            print("Opción fuera de rango.")

        except ValueError:
            print("Debe ingresar un número válido.")


def main():

    print("=" * 55)
    print(" SISTEMA INTELIGENTE DE BÚSQUEDA DE RUTAS")
    print("=" * 55)

    mostrar_estaciones()

    origen = seleccionar_estacion(
        "\nSeleccione el número de la estación de origen: "
    )

    destino = seleccionar_estacion(
        "Seleccione el número de la estación de destino: "
    )

    print("\nOrigen:", origen)
    print("Destino:", destino)

    # Aplicación de reglas lógicas

    if not estacion_existe(origen, GRAFO):
        print("La estación de origen no existe.")
        return

    if not estacion_existe(destino, GRAFO):
        print("La estación de destino no existe.")
        return

    if mismo_origen_destino(origen, destino):
        print("\nYa se encuentra en la estación de destino.")
        return

    print("\nBuscando la mejor ruta mediante A*...")

    ruta, costo = buscar_mejor_ruta(
      GRAFO,
      origen,
      destino,
      COORDENADAS,
      mostrar_proceso=True
    )

    if ruta:

        print("\n" + "=" * 55)
        print(" MEJOR RUTA ENCONTRADA")
        print("=" * 55)

        for i, estacion in enumerate(ruta, start=1):
            print(f"{i}. {estacion}")

        print("\nNúmero de estaciones:", len(ruta))
        print("Número de tramos:", len(ruta) - 1)
        print("Costo total estimado:", costo)

    else:
        print("\nNo fue posible encontrar una ruta.")


if __name__ == "__main__":
    main()