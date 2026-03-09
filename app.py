"""app.py — Punto de entrada de Rosa Oliva Recomendador de Joyas."""

import streamlit as st

import config
from data.loader import load_data
from recommender.engine import recommend
from ui.styles import CSS_STYLES
from ui import components

# --- Configuración de página ---
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout="wide",
)

st.markdown(CSS_STYLES, unsafe_allow_html=True)

# --- Carga de datos ---
clientes_df, productos_df = load_data()

# --- Cabecera principal ---
st.title(f"{config.PAGE_ICON} Rosa Oliva — Recomendador de Joyas")
st.write("Una demo interactiva de recomendaciones personalizadas.")
components.render_metric_header(clientes_df, productos_df)
st.markdown("---")

# --- Pestañas principales ---
tab1, tab2, tab3 = st.tabs(["💎 Recomendaciones", "🛍️ Catálogo", "📊 Análisis"])

# ── Pestaña 1: Recomendaciones ────────────────────────────────────────────────
with tab1:
    st.sidebar.header("Panel de Cliente")

    num_clientes = len(clientes_df) if clientes_df is not None else 10
    cliente_id_input = st.sidebar.number_input(
        f"ID de Cliente (1–{num_clientes})",
        min_value=1,
        max_value=num_clientes,
        step=1,
        value=1,
    )
    top_n = st.sidebar.slider(
        "Número de recomendaciones",
        min_value=1,
        max_value=config.MAX_TOP_N,
        value=config.DEFAULT_TOP_N,
    )
    get_recs_button = st.sidebar.button("Obtener Recomendaciones", use_container_width=True)

    if get_recs_button and clientes_df is not None:
        nombre = clientes_df.loc[
            clientes_df["cliente_id"] == cliente_id_input, "nombre"
        ].values[0]
        st.header(f"¡Hola, {nombre}!")

        cliente_info = clientes_df[clientes_df["cliente_id"] == cliente_id_input].iloc[0]
        components.render_customer_profile(cliente_info)

        st.subheader("Tus recomendaciones personalizadas")
        recommended_products, explanation = recommend(
            cliente_id_input, clientes_df, productos_df, top_n=top_n
        )

        if not recommended_products.empty:
            st.info(explanation)
            for _, producto in recommended_products.iterrows():
                components.render_product_card(producto, show_affinity=True)
        else:
            st.warning("No se pudieron generar recomendaciones. Verifica los datos.")
    else:
        st.info(
            "Introduce un ID de cliente en la barra lateral y haz clic en "
            "**Obtener Recomendaciones** para ver tus sugerencias personalizadas."
        )

# ── Pestaña 2: Catálogo ───────────────────────────────────────────────────────
with tab2:
    if productos_df is not None:
        components.render_catalog_tab(productos_df)
    else:
        st.error("No se pudieron cargar los datos del catálogo.")

# ── Pestaña 3: Análisis ───────────────────────────────────────────────────────
with tab3:
    if productos_df is not None:
        components.render_analysis_tab(productos_df)
    else:
        st.error("No se pudieron cargar los datos para el análisis.")
