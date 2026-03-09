"""tests/test_engine.py — Tests unitarios para el motor de recomendación."""

import pandas as pd
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recommender.engine import get_current_season, recommend
import config


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_clientes():
    return pd.DataFrame([
        {
            "cliente_id": 1,
            "nombre": "Ana",
            "edad": 30,
            "estilo_preferido": "Vintage",
            "material_favorito": "Oro",
            "frecuencia_compra": "Mensual",
            "fecha_ultima_compra": "2025-01-01",
            "valor_promedio_compra": 150.0,
        },
        {
            "cliente_id": 2,
            "nombre": "Luis",
            "edad": 45,
            "estilo_preferido": "Moderno",
            "material_favorito": "Acero",
            "frecuencia_compra": "Bimestral",
            "fecha_ultima_compra": "2025-02-01",
            "valor_promedio_compra": 200.0,
        },
    ])


@pytest.fixture
def sample_productos():
    return pd.DataFrame([
        {
            "producto_id": 1,
            "nombre": "Anillo Vintage Oro",
            "categoria": "Anillos",
            "material": "Oro",
            "precio": 200.0,
            "estilo": "Vintage",
            "ocasion": "Diario",
            "temporada": "Continuo",
            "oferta_mes": False,
            "valoracion": 4.5,
            "descripcion": "Anillo vintage en oro",
        },
        {
            "producto_id": 2,
            "nombre": "Collar Moderno Acero",
            "categoria": "Collares",
            "material": "Acero",
            "precio": 80.0,
            "estilo": "Moderno",
            "ocasion": "Trabajo",
            "temporada": "Continuo",
            "oferta_mes": True,
            "valoracion": 3.9,
            "descripcion": "Collar moderno en acero",
        },
        {
            "producto_id": 3,
            "nombre": "Pendiente Clásico Plata",
            "categoria": "Pendientes",
            "material": "Plata",
            "precio": 60.0,
            "estilo": "Clásico",
            "ocasion": "Fiesta",
            "temporada": "Invierno",
            "oferta_mes": False,
            "valoracion": 4.0,
            "descripcion": "Pendiente clásico en plata",
        },
    ])


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_get_current_season_returns_valid():
    season = get_current_season()
    assert season in config.SEASON_MAP.keys()


def test_recommend_returns_top_n(sample_clientes, sample_productos):
    result, explanation = recommend(1, sample_clientes, sample_productos, top_n=2)
    assert len(result) == 2
    assert isinstance(explanation, str)
    assert len(explanation) > 0


def test_recommend_default_top_n(sample_clientes, sample_productos):
    result, _ = recommend(1, sample_clientes, sample_productos)
    assert len(result) <= config.DEFAULT_TOP_N


def test_recommend_prefers_style_and_material_match(sample_clientes, sample_productos):
    """El producto con estilo+material coincidente debe tener mayor puntuación."""
    result, _ = recommend(1, sample_clientes, sample_productos, top_n=1)
    top_product = result.iloc[0]
    # Cliente 1 prefiere Vintage + Oro: el producto 1 debería aparecer primero
    assert top_product["nombre"] == "Anillo Vintage Oro"


def test_recommend_affinity_pct_between_0_and_1(sample_clientes, sample_productos):
    result, _ = recommend(1, sample_clientes, sample_productos, top_n=3)
    assert "affinity_pct" in result.columns
    assert (result["affinity_pct"] >= 0).all()
    assert (result["affinity_pct"] <= 1).all()


def test_recommend_invalid_client_returns_empty(sample_clientes, sample_productos):
    result, explanation = recommend(999, sample_clientes, sample_productos)
    assert result.empty
    assert explanation == ""


def test_recommend_none_data_returns_empty():
    result, explanation = recommend(1, None, None)
    assert result.empty
    assert explanation == ""


def test_recommend_explanation_contains_style(sample_clientes, sample_productos):
    _, explanation = recommend(1, sample_clientes, sample_productos)
    assert "Vintage" in explanation
    assert "Oro" in explanation
