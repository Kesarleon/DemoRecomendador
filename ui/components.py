"""ui/components.py — Componentes reutilizables de la interfaz de Rosa Oliva."""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def _stars(rating: float) -> str:
    """Devuelve una cadena de estrellas para una valoración 1–5."""
    full = int(round(rating))
    return config.STAR_FULL * full + config.STAR_EMPTY * (5 - full)


def render_metric_header(clientes_df: pd.DataFrame, productos_df: pd.DataFrame) -> None:
    """Muestra tres métricas clave en la parte superior del dashboard."""
    if clientes_df is None or productos_df is None:
        return
    total_clientes = len(clientes_df)
    total_productos = len(productos_df)
    ofertas_activas = int(productos_df["oferta_mes"].sum())

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Clientes registrados", total_clientes)
    col2.metric("💎 Productos en catálogo", total_productos)
    col3.metric("🔥 Ofertas activas", ofertas_activas)


def render_product_card(producto: pd.Series, show_affinity: bool = False) -> None:
    """Renderiza una tarjeta visual para un producto."""
    icon = config.CATEGORY_ICONS.get(producto["categoria"], "💎")
    oferta_badge = (
        '<span class="badge-oferta">🔥 Oferta del mes</span>'
        if producto["oferta_mes"]
        else ""
    )
    material_badge = f'<span class="badge-material">{producto["material"]}</span>'

    # Valoración (columna opcional)
    rating_str = ""
    if "valoracion" in producto.index and pd.notna(producto["valoracion"]):
        rating_str = f"&nbsp;{_stars(float(producto['valoracion']))} ({producto['valoracion']:.1f})"

    # Descripción (columna opcional)
    desc_str = ""
    if "descripcion" in producto.index and pd.notna(producto["descripcion"]):
        desc_str = f"<p style='color:#666;font-size:0.88em;margin:4px 0 0 0;'>{producto['descripcion']}</p>"

    st.markdown(
        f"""
        <div class="product-card">
            <h4 style="margin:0 0 4px 0;">{icon} {producto['nombre']}</h4>
            <p style="margin:0 0 4px 0;">
                {material_badge}
                <span style="font-size:0.85em;color:#666;">{producto['categoria']} · {producto['estilo']} · {producto['ocasion']}</span>
            </p>
            {desc_str}
            <p style="margin:6px 0 2px 0;font-size:1.05em;">
                <strong style="color:#C9A84C;">${producto['precio']:.2f}</strong>
                {rating_str}
            </p>
            {oferta_badge}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if show_affinity and "affinity_pct" in producto.index:
        pct = float(producto["affinity_pct"])
        st.progress(pct, text=f"Afinidad: {pct*100:.0f}%")


def render_customer_profile(cliente: pd.Series) -> None:
    """Muestra el perfil del cliente en un expander."""
    with st.expander("Ver tu perfil de cliente"):
        col1, col2 = st.columns(2)
        col1.write(f"**Estilo preferido:** {cliente['estilo_preferido']}")
        col1.write(f"**Material favorito:** {cliente['material_favorito']}")
        col2.write(f"**Frecuencia de compra:** {cliente['frecuencia_compra']}")
        col2.write(f"**Última compra:** {cliente['fecha_ultima_compra']}")
        st.write(f"**Valor medio de compra:** ${float(cliente['valor_promedio_compra']):.2f}")


def render_catalog_tab(productos_df: pd.DataFrame) -> None:
    """Pestaña de catálogo con filtros interactivos."""
    st.subheader("🛍️ Catálogo completo")

    with st.expander("Filtros", expanded=True):
        col1, col2, col3 = st.columns(3)
        categorias = ["Todas"] + sorted(productos_df["categoria"].unique().tolist())
        materiales = ["Todos"] + sorted(productos_df["material"].unique().tolist())
        estilos = ["Todos"] + sorted(productos_df["estilo"].unique().tolist())

        cat_sel = col1.selectbox("Categoría", categorias)
        mat_sel = col2.selectbox("Material", materiales)
        est_sel = col3.selectbox("Estilo", estilos)

        precio_min = float(productos_df["precio"].min())
        precio_max = float(productos_df["precio"].max())
        rango_precio = st.slider(
            "Rango de precio ($)",
            min_value=precio_min,
            max_value=precio_max,
            value=(precio_min, precio_max),
            step=10.0,
        )
        solo_oferta = st.checkbox("Solo ofertas activas")

    filtrado = productos_df.copy()
    if cat_sel != "Todas":
        filtrado = filtrado[filtrado["categoria"] == cat_sel]
    if mat_sel != "Todos":
        filtrado = filtrado[filtrado["material"] == mat_sel]
    if est_sel != "Todos":
        filtrado = filtrado[filtrado["estilo"] == est_sel]
    filtrado = filtrado[
        (filtrado["precio"] >= rango_precio[0]) & (filtrado["precio"] <= rango_precio[1])
    ]
    if solo_oferta:
        filtrado = filtrado[filtrado["oferta_mes"]]

    st.write(f"**{len(filtrado)} productos** encontrados")

    display_cols = ["nombre", "categoria", "material", "precio", "estilo", "ocasion", "temporada", "oferta_mes"]
    if "valoracion" in filtrado.columns:
        display_cols.append("valoracion")

    st.dataframe(
        filtrado[display_cols].reset_index(drop=True),
        use_container_width=True,
        column_config={
            "precio": st.column_config.NumberColumn("Precio ($)", format="$%.2f"),
            "valoracion": st.column_config.NumberColumn("Valoración ★", format="%.1f"),
            "oferta_mes": st.column_config.CheckboxColumn("Oferta"),
        },
    )


def render_analysis_tab(productos_df: pd.DataFrame) -> None:
    """Pestaña de análisis con gráficos Plotly."""
    st.subheader("📊 Análisis del catálogo")

    col1, col2 = st.columns(2)

    # Gráfico 1: productos por categoría
    with col1:
        cat_counts = (
            productos_df.groupby("categoria")
            .size()
            .reset_index(name="cantidad")
            .sort_values("cantidad", ascending=True)
        )
        fig_cat = px.bar(
            cat_counts,
            x="cantidad",
            y="categoria",
            orientation="h",
            title="Productos por categoría",
            color="cantidad",
            color_continuous_scale=[[0, "#C9A84C"], [1, "#00A86B"]],
            labels={"cantidad": "Cantidad", "categoria": "Categoría"},
        )
        fig_cat.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_cat, use_container_width=True)

    # Gráfico 2: distribución de precios
    with col2:
        fig_price = px.histogram(
            productos_df,
            x="precio",
            nbins=15,
            title="Distribución de precios",
            color_discrete_sequence=["#556B2F"],
            labels={"precio": "Precio ($)", "count": "Productos"},
        )
        fig_price.update_layout(bargap=0.1)
        st.plotly_chart(fig_price, use_container_width=True)

    col3, col4 = st.columns(2)

    # Gráfico 3: productos por material
    with col3:
        mat_counts = productos_df["material"].value_counts().reset_index()
        mat_counts.columns = ["material", "cantidad"]
        fig_mat = px.pie(
            mat_counts,
            names="material",
            values="cantidad",
            title="Distribución por material",
            color_discrete_sequence=px.colors.sequential.Greens_r,
        )
        st.plotly_chart(fig_mat, use_container_width=True)

    # Gráfico 4: valoración media por categoría (si existe la columna)
    with col4:
        if "valoracion" in productos_df.columns:
            val_cat = (
                productos_df.groupby("categoria")["valoracion"]
                .mean()
                .reset_index()
                .rename(columns={"valoracion": "valoracion_media"})
                .sort_values("valoracion_media", ascending=False)
            )
            fig_val = px.bar(
                val_cat,
                x="categoria",
                y="valoracion_media",
                title="Valoración media por categoría",
                color="valoracion_media",
                color_continuous_scale=[[0, "#C9A84C"], [1, "#00A86B"]],
                labels={"valoracion_media": "Valoración media", "categoria": "Categoría"},
            )
            fig_val.update_layout(coloraxis_showscale=False, yaxis_range=[0, 5])
            st.plotly_chart(fig_val, use_container_width=True)
        else:
            st.info("Columna 'valoracion' no disponible para este gráfico.")
