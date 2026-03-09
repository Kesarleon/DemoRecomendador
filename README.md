# Rosa Oliva — Recomendador de Joyas

Demo interactiva de un sistema de recomendación de joyas para la marca **Rosa Oliva**, construida con Streamlit.

## Estructura del proyecto

```
DemoRecomendador/
├── app.py                 # Punto de entrada (thin entry point)
├── config.py              # Constantes y configuración central
├── requirements.txt       # Dependencias Python
│
├── data/
│   ├── loader.py          # Carga y validación de datos
│   ├── clientes.csv       # 25 perfiles de clientes
│   └── productos.csv      # 40 productos del catálogo
│
├── recommender/
│   └── engine.py          # Motor de recomendación (scoring + temporada)
│
├── ui/
│   ├── styles.py          # CSS de branding Rosa Oliva
│   └── components.py      # Componentes reutilizables (tarjetas, gráficos)
│
└── tests/
    ├── test_engine.py     # Tests del motor de recomendación
    └── test_loader.py     # Tests de carga de datos
```

## Características

- **Dashboard con 3 pestañas**: Recomendaciones, Catálogo y Análisis
- **Recomendaciones personalizadas**: basadas en estilo, material, temporada y ofertas activas
- **Puntuación de afinidad**: visible como barra de progreso en cada producto
- **Catálogo filtrable**: por categoría, material, estilo y rango de precio
- **Análisis visual**: gráficos Plotly de distribución de categorías, precios, materiales y valoraciones
- **Valoraciones y descripciones**: cada producto incluye puntuación (★) y descripción corta
- **Tests unitarios**: cobertura del motor de recomendación y carga de datos

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```

## Tests

```bash
pytest tests/ -v
```

## Cómo funciona el motor de recomendación

El sistema usa **filtrado basado en contenido** calculando un *affinity_score* para cada producto:

| Factor | Puntos |
|---|---|
| Coincidencia de estilo con preferencia del cliente | +3 |
| Coincidencia de material favorito | +3 |
| Temporada actual del producto | +2 |
| Producto de temporada "Continuo" | +1 |
| Oferta activa del mes | +4 |
| Factor de aleatoriedad (variedad) | 0–1 |

La puntuación se normaliza a porcentaje (0–100 %) para mostrarla visualmente.
