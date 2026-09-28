# Sistema Inteligente de Búsqueda de Rutas

Proyecto académico desarrollado para la asignatura de Inteligencia Artificial.

El sistema utiliza una base de conocimiento representada mediante un grafo, reglas lógicas y el algoritmo de búsqueda heurística A* para determinar una ruta de menor costo entre dos estaciones de un sistema de transporte masivo simplificado.

> **Nota:** las estaciones toman como referencia nombres del sistema de transporte de Bogotá, pero las conexiones, costos y coordenadas utilizadas corresponden a un modelo académico simplificado y no representan rutas, tiempos o distancias reales.

## Objetivo

Desarrollar un sistema inteligente capaz de encontrar una ruta entre un punto de origen y un punto de destino utilizando técnicas de representación del conocimiento, sistemas basados en reglas y búsqueda heurística.

## Componentes

### Base de conocimiento

La base de conocimiento se encuentra en `conocimiento.py`.

El sistema de transporte es representado mediante un grafo:

- Los nodos representan estaciones.
- Las aristas representan conexiones.
- Los valores asociados representan el costo del desplazamiento.
- Las coordenadas permiten calcular la heurística.

### Reglas lógicas

El archivo `reglas.py` contiene reglas para:

- Validar la existencia de una estación.
- Determinar si origen y destino son iguales.
- Verificar conexiones directas.
- Obtener las conexiones disponibles.

### Búsqueda heurística

El archivo `busqueda.py` implementa el algoritmo A*.

A* utiliza:

f(n) = g(n) + h(n)

Donde:

- `g(n)` representa el costo acumulado desde el origen.
- `h(n)` representa la estimación del costo restante hasta el destino.
- `f(n)` representa el costo total estimado.

La heurística se calcula utilizando distancia euclidiana entre las coordenadas simplificadas de las estaciones.

## Estructura del proyecto

```text
SistemaInteligente/
│
├── main.py
├── conocimiento.py
├── reglas.py
├── busqueda.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── tests/
│   └── test_sistema.py
│
└── docs/