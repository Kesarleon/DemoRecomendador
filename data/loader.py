"""data/loader.py — Carga y validación de datos de Rosa Oliva."""

import os
import streamlit as st
import pandas as pd
import sys

# Añadir raíz del proyecto al path para importar config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

REQUIRED_CLIENTES_COLS = {
    "cliente_id", "nombre", "edad", "estilo_preferido",
    "material_favorito", "frecuencia_compra", "fecha_ultima_compra",
    "valor_promedio_compra",
}
REQUIRED_PRODUCTOS_COLS = {
    "producto_id", "nombre", "categoria", "material", "precio",
    "estilo", "ocasion", "temporada", "oferta_mes",
}


@st.cache_data
def load_data() -> tuple[pd.DataFrame | None, pd.DataFrame | None]:
    """Carga clientes y productos desde los CSVs del directorio data/."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, config.DATA_DIR)
    clientes_path = os.path.join(data_dir, config.CLIENTES_FILE)
    productos_path = os.path.join(data_dir, config.PRODUCTOS_FILE)

    try:
        clientes_df = pd.read_csv(clientes_path)
        productos_df = pd.read_csv(productos_path)
    except FileNotFoundError as e:
        st.error(
            f"Error: No se encontró un archivo de datos. "
            f"Asegúrate de que '{config.CLIENTES_FILE}' y '{config.PRODUCTOS_FILE}' "
            f"están en la carpeta '{config.DATA_DIR}/'.\n\nDetalle: {e}"
        )
        return None, None

    missing_c = REQUIRED_CLIENTES_COLS - set(clientes_df.columns)
    missing_p = REQUIRED_PRODUCTOS_COLS - set(productos_df.columns)
    if missing_c or missing_p:
        st.error(
            f"Columnas faltantes — clientes: {missing_c}, productos: {missing_p}"
        )
        return None, None

    return clientes_df, productos_df
