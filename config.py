# config.py — Configuración central de Rosa Oliva Recomendador

# --- Branding ---
PAGE_TITLE = "Rosa Oliva | Recomendador de Joyas"
PAGE_ICON = "💎"

BRAND_COLORS = {
    "olive": "#556B2F",
    "jade": "#00A86B",
    "jade_dark": "#007D60",
    "cream": "#FDFDF5",
    "charcoal": "#36454F",
    "gold": "#C9A84C",
}

# --- Rutas de datos ---
DATA_DIR = "data"
CLIENTES_FILE = "clientes.csv"
PRODUCTOS_FILE = "productos.csv"

# --- Pesos del motor de recomendación ---
SCORE_ESTILO_MATCH = 3
SCORE_MATERIAL_MATCH = 3
SCORE_TEMPORADA_MATCH = 2
SCORE_TEMPORADA_CONTINUO = 1
SCORE_OFERTA_BOOST = 4
SCORE_RANDOM_MAX = 1.0

# Puntuación máxima posible (sin aleatoriedad) para normalización
MAX_POSSIBLE_SCORE = (
    SCORE_ESTILO_MATCH
    + SCORE_MATERIAL_MATCH
    + SCORE_TEMPORADA_MATCH
    + SCORE_OFERTA_BOOST
    + SCORE_RANDOM_MAX
)

# --- Temporadas ---
SEASON_MAP = {
    "Primavera": [3, 4, 5],
    "Verano": [6, 7, 8],
    "Otoño": [9, 10, 11],
    "Invierno": [12, 1, 2],
}

# --- Iconos por categoría ---
CATEGORY_ICONS = {
    "Anillos": "💍",
    "Collares": "📿",
    "Pendientes": "✨",
    "Pulseras": "⚜️",
    "Broches": "🌿",
}

# --- Configuración de recomendaciones ---
DEFAULT_TOP_N = 3
MAX_TOP_N = 8

# --- Estrellas de valoración ---
STAR_FULL = "★"
STAR_EMPTY = "☆"
