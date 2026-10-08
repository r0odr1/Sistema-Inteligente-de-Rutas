import csv
import random

ARCHIVO_SALIDA = "datos/rutas_transporte.csv"

# Este script genera 150 registros sintéticos adicionales y conserva los 20 originales.
# Semilla fija para poder reproducir el mismo dataset.
random.seed(42)

def es_hora_pico(hora):
    hh, mm = map(int, hora.split(":"))
    minutos = hh * 60 + mm
    return int(360 <= minutos <= 540 or 960 <= minutos <= 1140)

# Los 20 registros originales se conservan y se les asigna una hora para completar las nuevas variables.
horas_originales = [
    "07:30", "08:15", "10:30", "17:45", "18:20", "11:00", "14:15", "16:30",
    "06:45", "12:10", "09:20", "17:10", "19:00", "13:40", "20:15", "07:05",
    "10:50", "15:30", "18:45", "21:00"
]

with open(ARCHIVO_SALIDA, newline="", encoding="utf-8") as archivo:
    originales = list(csv.DictReader(archivo))[:20]

for registro, hora in zip(originales, horas_originales):
    registro["hora"] = hora
    registro["hora_pico"] = es_hora_pico(hora)

# Generar 150 registros nuevos.
nuevos = []
for _ in range(150):
    distancia = round(random.uniform(5.0, 32.0), 1)
    estaciones = max(4, min(20, int(round(distancia * 0.58 + random.uniform(-1.5, 2.0)))))
    transbordos = max(0, min(5, int(round((estaciones - 5) / 4 + random.uniform(-1, 1)))))

    hora = random.randint(5, 22)
    minuto = random.choice([0, 10, 15, 20, 30, 40, 45, 50])
    hora_texto = f"{hora:02d}:{minuto:02d}"
    hora_pico = es_hora_pico(hora_texto)

    congestion = max(1, min(5, int(round(random.gauss(2.4 + 1.0 * hora_pico, 0.9)))))
    tiempo = max(12, round(distancia * 2.2 + estaciones * 0.65 + transbordos * 4 + congestion * 2.2 + random.uniform(-3.5, 3.5)))
    costo = round(7 + distancia * 1.75 + transbordos * 2.8 + random.uniform(-2.5, 2.5), 1)

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

# La etiqueta se obtiene de una regla académica sintética: menor tiempo/costo/congestión
# implica mayor probabilidad de recomendación.
scores = []
for r in nuevos:
    score = (r["tiempo_estimado_min"] + r["costo_estimado"] * 0.45 +
             r["numero_transbordos"] * 4 + r["nivel_congestion"] * 4 + r["hora_pico"] * 6)
    r["_score"] = score
    scores.append(score)

scores.sort()
umbral = (scores[74] + scores[75]) / 2

for r in nuevos:
    score = r.pop("_score")
    r["ruta_recomendada"] = int(score + random.uniform(-5, 5) <= umbral)

registros = originales + nuevos
columnas = [
    "distancia_km", "numero_estaciones", "numero_transbordos",
    "nivel_congestion", "tiempo_estimado_min", "costo_estimado",
    "hora", "hora_pico", "ruta_recomendada"
]

with open(ARCHIVO_SALIDA, "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=columnas)
    escritor.writeheader()
    escritor.writerows(registros)

print(f"Dataset generado correctamente: {len(registros)} registros")
print("Columnas añadidas: hora, hora_pico")
