import csv
import random
from pathlib import Path

# --------------------------------------------------
# 1. CONFIGURACIÓN GENERAL
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

ARCHIVO_BASE = BASE_DIR / "rutas_base.csv"
ARCHIVO_SALIDA = BASE_DIR / "rutas_transporte.csv"

SEMILLA = 42
CANTIDAD_NUEVOS = 150

COLUMNAS = [
    "distancia_km",
    "numero_estaciones",
    "numero_transbordos",
    "nivel_congestion",
    "tiempo_estimado_min",
    "costo_estimado",
    "hora",
    "hora_pico",
    "ruta_recomendada",
]


# --------------------------------------------------
# 2. HORAS DE LOS 20 REGISTROS ORIGINALES
# --------------------------------------------------

# Estas horas se conservan del generador original.
# Se asignan en el mismo orden de los 20 registros
# almacenados en rutas_base.csv.

HORAS_ORIGINALES = [
    "07:30",
    "08:15",
    "10:30",
    "17:45",
    "18:20",
    "11:00",
    "14:15",
    "16:30",
    "06:45",
    "12:10",
    "09:20",
    "17:10",
    "19:00",
    "13:40",
    "20:15",
    "07:05",
    "10:50",
    "15:30",
    "18:45",
    "21:00",
]

# --------------------------------------------------
# 3. IDENTIFICAR HORAS PICO
# --------------------------------------------------

def es_hora_pico(hora):
    """
    Determina si una hora corresponde a hora pico.

    Periodos académicos:
    - Mañana: 06:00 a 09:00.
    - Tarde: 16:00 a 19:00.

    Retorna:
        1 = Hora pico.
        0 = Fuera de hora pico.
    """
    hh, mm = map(int, hora.split(":"))

    minutos = hh * 60 + mm

    return int(360 <= minutos <= 540 or 960 <= minutos <= 1140)

# --------------------------------------------------
# 4. CARGAR LOS REGISTROS ORIGINALES
# --------------------------------------------------

def cargar_registros_originales():
    """
    Carga los 20 registros base.

    Se utiliza un archivo independiente para evitar
    que el generador dependa de su propio CSV de salida.
    """

    if not ARCHIVO_BASE.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ARCHIVO_BASE}")

    with open(
        ARCHIVO_BASE,
        newline="",
        encoding="utf-8"
    ) as archivo:
        originales = list(csv.DictReader(archivo))

    if len(originales) != len(HORAS_ORIGINALES):
        raise ValueError("El archivo base debe contener exactamente 20 registros originales.")

    columnas_obligatorias = set(COLUMNAS) - {
        "hora",
        "hora_pico",
    }

    for indice, registro in enumerate(originales):

        faltantes = (columnas_obligatorias - set(registro))

        if faltantes:
            raise ValueError(
                "Faltan columnas en rutas_base.csv: "
                f"{sorted(faltantes)}"
            )

        # Conservamos las horas del script original.
        hora = HORAS_ORIGINALES[indice]

        registro["hora"] = hora
        registro["hora_pico"] = es_hora_pico(hora)

    return originales


# --------------------------------------------------
# 5. GENERAR 150 REGISTROS SINTÉTICOS
# --------------------------------------------------

def generar_registros_nuevos(rng):
    """
    Genera registros sintéticos adicionales.

    Variables:
    - Distancia.
    - Número de estaciones.
    - Número de transbordos.
    - Congestión.
    - Tiempo estimado.
    - Costo estimado.
    - Hora y hora pico.

    Se utiliza una semilla fija para garantizar
    resultados reproducibles.
    """

    nuevos = []

    for _ in range(CANTIDAD_NUEVOS):

        # Distancia simulada de la ruta.
        distancia = round(rng.uniform(5.0, 32.0), 1)

        # Cantidad de estaciones.
        estaciones = max(4, min(20, int(round(distancia * 0.58 + rng.uniform(-1.5, 2.0)))))

        # Cantidad de transbordos.
        transbordos = max(0, min(5, int(round((estaciones - 5) / 4 + rng.uniform(-1, 1)))))

        # Hora simulada del recorrido.
        hora = rng.randint(5, 22)

        minuto = rng.choice([0, 10, 15, 20, 30, 40, 45, 50])

        hora_texto = f"{hora:02d}:{minuto:02d}"
        hora_pico = es_hora_pico(hora_texto)

        # Se supone mayor congestión en hora pico.
        congestion = max(1, min(5, int(round(rng.gauss(2.4 + 1.0 * hora_pico, 0.9)))))

        # Tiempo estimado del recorrido.
        tiempo = max(12, round(
            distancia * 2.2 +
            estaciones * 0.65 +
            transbordos * 4 +
            congestion * 2.2 +
            rng.uniform(-3.5, 3.5)
        ))

        # Costo académico estimado.
        # No representa el valor real del pasaje.
        costo = round(
            7 +
            distancia * 1.75 +
            transbordos * 2.8 +
            rng.uniform(-2.5, 2.5),
            1
        )

        nuevos.append({
            "distancia_km": distancia,
            "numero_estaciones": estaciones,
            "numero_transbordos": transbordos,
            "nivel_congestion": congestion,
            "tiempo_estimado_min": tiempo,
            "costo_estimado": costo,
            "hora": hora_texto,
            "hora_pico": hora_pico,
        })

    return nuevos

# --------------------------------------------------
# 6. CLASIFICAR LAS RUTAS SINTÉTICAS
# --------------------------------------------------

def clasificar_rutas(registros, rng):
    """
    Asigna la variable objetivo ruta_recomendada.

    El puntaje considera:
    - Tiempo estimado.
    - Costo estimado.
    - Transbordos.
    - Congestión.
    - Hora pico.

    Un menor puntaje favorece la recomendación.
    Se añade una pequeña variación aleatoria.

    Esta clasificación es sintética y académica.
    """

    puntajes = []

    for registro in registros:

        puntaje = (
            registro["tiempo_estimado_min"] +
            registro["costo_estimado"] * 0.45 +
            registro["numero_transbordos"] * 4 +
            registro["nivel_congestion"] * 4 +
            registro["hora_pico"] * 6
        )

        # Guardar el puntaje del registro.
        registro["_puntaje"] = puntaje

        # Añadirlo a la lista para calcular el umbral.
        puntajes.append(puntaje)

    puntajes.sort()

    # Umbral central de los 150 registros nuevos.
    umbral = (puntajes[74] + puntajes[75]) / 2

    for registro in registros:

        puntaje = registro.pop("_puntaje")

        registro["ruta_recomendada"] = int(puntaje + rng.uniform(-5, 5) <= umbral)

    return registros

# --------------------------------------------------
# 7. CONSTRUIR EL DATASET COMPLETO
# --------------------------------------------------

def generar_dataset():
    """
    Construye el dataset definitivo.

    Pasos:
    1. Cargar 20 registros originales.
    2. Generar 150 registros nuevos.
    3. Clasificar las rutas sintéticas.
    4. Unir todos los registros.
    5. Guardar el archivo CSV.
    6. Mostrar el resumen.
    """

    rng = random.Random(SEMILLA)
    originales = cargar_registros_originales()
    nuevos = generar_registros_nuevos(rng)

    nuevos = clasificar_rutas(
        nuevos,
        rng
    )

    registros = originales + nuevos

    # ------------------------------------------
    # 7.1 GUARDAR EL ARCHIVO CSV
    # ------------------------------------------

    with open(
        ARCHIVO_SALIDA,
        "w",
        newline="",
        encoding="utf-8"
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=COLUMNAS
        )

        escritor.writeheader()
        escritor.writerows(registros)

    # ------------------------------------------
    # 7.2 MOSTRAR RESULTADOS
    # ------------------------------------------

    recomendadas = sum(
        int(registro["ruta_recomendada"]) == 1
        for registro in registros
    )

    no_recomendadas = (len(registros) - recomendadas)

    print("=" * 60)
    print(" GENERACIÓN DEL DATASET DE TRANSPORTE")
    print("=" * 60)

    print(f"\nRegistros originales: {len(originales)}")
    print(f"Registros nuevos: {len(nuevos)}")
    print(f"Total de registros: {len(registros)}")
    print(f"Columnas: {len(COLUMNAS)}")

    print(f"\nRutas recomendadas: {recomendadas}")
    print(f"Rutas no recomendadas: {no_recomendadas}")

    print(f"\nArchivo generado: {ARCHIVO_SALIDA}")

    print("\nClasificación:")
    print("0 = Ruta no recomendada")
    print("1 = Ruta recomendada")

    return registros


# --------------------------------------------------
# 8. PUNTO DE ENTRADA
# --------------------------------------------------

if __name__ == "__main__":
    generar_dataset()
