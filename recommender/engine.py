"""recommender/engine.py — Motor de recomendación de Rosa Oliva."""

import random
from datetime import datetime

import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def get_current_season() -> str:
    """Devuelve la temporada actual basándose en el mes del sistema."""
    month = datetime.now().month
    for season, months in config.SEASON_MAP.items():
        if month in months:
            return season
    return "Continuo"


def recommend(
    cliente_id: int,
    clientes_df: pd.DataFrame,
    productos_df: pd.DataFrame,
    top_n: int = config.DEFAULT_TOP_N,
) -> tuple[pd.DataFrame, str]:
    """
    Genera recomendaciones personalizadas para un cliente.

    Returns:
        Tupla (DataFrame con productos recomendados + columna affinity_pct, texto explicativo).
        En caso de error devuelve (DataFrame vacío, "").
    """
    if clientes_df is None or productos_df is None:
        return pd.DataFrame(), ""

    try:
        cliente = clientes_df.loc[clientes_df["cliente_id"] == cliente_id].iloc[0]
    except IndexError:
        return pd.DataFrame(), ""

    current_season = get_current_season()
    scores = []

    for _, producto in productos_df.iterrows():
        score = 0.0

        # 1. Coincidencia de estilo y material
        if producto["estilo"] == cliente["estilo_preferido"]:
            score += config.SCORE_ESTILO_MATCH
        if producto["material"] == cliente["material_favorito"]:
            score += config.SCORE_MATERIAL_MATCH

        # 2. Relevancia de temporada
        if producto["temporada"] == current_season:
            score += config.SCORE_TEMPORADA_MATCH
        elif producto["temporada"] == "Continuo":
            score += config.SCORE_TEMPORADA_CONTINUO

        # 3. Impulso por oferta del mes
        if producto["oferta_mes"]:
            score += config.SCORE_OFERTA_BOOST

        # 4. Pequeña aleatoriedad para variedad
        score += random.uniform(0, config.SCORE_RANDOM_MAX)

        scores.append(score)

    result_df = productos_df.copy()
    result_df["affinity_score"] = scores

    # Normalizar a porcentaje (0–100)
    result_df["affinity_pct"] = (
        result_df["affinity_score"] / config.MAX_POSSIBLE_SCORE
    ).clip(0, 1)

    recommended_df = result_df.sort_values("affinity_score", ascending=False).head(top_n)

    explanation = (
        f"Basado en tu gusto por el estilo **{cliente['estilo_preferido']}** "
        f"y el material **{cliente['material_favorito']}**, "
        f"considerando la temporada de **{current_season}** y las ofertas actuales."
    )

    return recommended_df, explanation
