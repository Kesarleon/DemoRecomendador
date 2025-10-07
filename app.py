import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import random

# --- Page Configuration ---
st.set_page_config(
    page_title="Rosa Oliva Recommender",
    page_icon="💎",
    layout="wide",
)

# --- Custom CSS for Ambéa Branding ---
st.markdown("""
<style>
    /* New color scheme: Olive, Jade, and Gold */
    .stApp {
        background-color: #FDFDF5; /* Light cream background for contrast */
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #556B2F; /* Olive Green */
    }

    /* Button styling */
    .stButton>button {
        background-color: #00A86B; /* Jade Green */
        color: #FFFFFF;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #007D60; /* Darker Jade */
        color: #FFFFFF;
    }

    /* Text and Titles */
    h1, h2, h3 {
        color: #36454F; /* Charcoal for high contrast */
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Improve contrast for success messages */
    div[data-testid="stNotification"][kind="success"] p {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
@st.cache_data
def load_data():
    """Loads customer and product data from CSV files using robust, absolute paths."""
    try:
        # Get the absolute path of the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        clientes_path = os.path.join(script_dir, "clientes.csv")
        productos_path = os.path.join(script_dir, "productos.csv")

        clientes_df = pd.read_csv(clientes_path)
        productos_df = pd.read_csv(productos_path)
        return clientes_df, productos_df
    except FileNotFoundError as e:
        st.error(f"Error: A data file was not found. Please ensure 'clientes.csv' and 'productos.csv' are in the same directory as the app.\n\nDetails: {e}")
        return None, None

clientes_df, productos_df = load_data()

# --- Recommendation Logic ---
def get_current_season():
    """Determines the current season."""
    month = datetime.now().month
    if month in [3, 4, 5]:
        return 'Primavera'
    elif month in [6, 7, 8]:
        return 'Verano'
    elif month in [9, 10, 11]:
        return 'Otoño'
    else:
        return 'Invierno'

def recommend(cliente_id, clientes_df, productos_df, top_n=3):
    """
    Generates personalized jewelry recommendations for a given customer.
    """
    if clientes_df is None or productos_df is None:
        return pd.DataFrame(), ""

    try:
        cliente = clientes_df.loc[clientes_df['cliente_id'] == cliente_id].iloc[0]
    except IndexError:
        st.warning("Please enter a valid Client ID.")
        return pd.DataFrame(), ""

    scores = []
    current_season = get_current_season()

    for _, producto in productos_df.iterrows():
        score = 0

        # 1. Style and Material Similarity
        if producto['estilo'] == cliente['estilo_preferido']:
            score += 3
        if producto['material'] == cliente['material_favorito']:
            score += 3

        # 2. Season Relevance
        if producto['temporada'] == current_season:
            score += 2
        if producto['temporada'] == 'Continuo':
            score += 1

        # 3. Monthly Offer Boost
        if producto['oferta_mes']:
            score += 4

        # 4. Light Randomization
        score += random.uniform(0, 1)

        scores.append(score)

    productos_df['affinity_score'] = scores

    # Sort and get top recommendations
    recommended_df = productos_df.sort_values(by='affinity_score', ascending=False).head(top_n)

    # Generate explanation
    explanation = f"Basado en tu gusto por el estilo **{cliente['estilo_preferido']}** y el material **{cliente['material_favorito']}**, y considerando la temporada de **{current_season}** y las ofertas actuales."

    return recommended_df, explanation

# --- Streamlit UI ---
st.title("💎 Rosa Oliva: Recomendador de Joyas")
st.write("Una demo interactiva de recomendaciones personalizadas.")

# --- Sidebar ---
st.sidebar.header("Panel de Cliente")
cliente_id_input = st.sidebar.number_input(
    "Introduce tu ID de Cliente (1-10)",
    min_value=1,
    max_value=10,
    step=1,
    value=1
)
get_recs_button = st.sidebar.button("Obtener Recomendaciones")


# --- Main Panel ---
if get_recs_button and clientes_df is not None:
    st.header(f"Hola, {clientes_df.loc[clientes_df['cliente_id'] == cliente_id_input, 'nombre'].values[0]}!")

    # Display Customer Profile
    with st.expander("Ver tu perfil de cliente"):
        cliente_info = clientes_df[clientes_df['cliente_id'] == cliente_id_input].iloc[0]
        st.write(f"**Estilo Preferido:** {cliente_info['estilo_preferido']}")
        st.write(f"**Material Favorito:** {cliente_info['material_favorito']}")
        st.write(f"**Frecuencia de Compra:** {cliente_info['frecuencia_compra']}")
        st.write(f"**Última Compra:** {cliente_info['fecha_ultima_compra']}")

    st.subheader("Tus recomendaciones personalizadas")

    recommended_products, explanation = recommend(cliente_id_input, clientes_df, productos_df)

    if not recommended_products.empty:
        st.info(explanation)

        # Display recommendations in cards
        for _, producto in recommended_products.iterrows():
            st.header("💎")
            st.markdown(f"**{producto['nombre']}**")
            st.write(f"_{producto['categoria']}_ | **Estilo:** {producto['estilo']}")
            st.write(f"**Precio:** ${producto['precio']:.2f}")
            if producto['oferta_mes']:
                st.success("🔥 ¡En oferta este mes!")
            st.markdown("---")
    else:
        st.warning("No se pudieron generar recomendaciones. Verifica los datos.")

else:
    st.info("Introduce un ID de cliente en la barra lateral y haz clic para ver tus recomendaciones.")