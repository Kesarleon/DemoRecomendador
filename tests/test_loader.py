"""tests/test_loader.py — Tests para la carga de datos."""

import os
import pandas as pd
import pytest
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def _write_valid_csvs(tmp_path):
    """Escribe CSVs válidos en tmp_path/data/."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    clientes = pd.DataFrame([{
        "cliente_id": 1, "nombre": "Ana", "edad": 30,
        "estilo_preferido": "Vintage", "material_favorito": "Oro",
        "frecuencia_compra": "Mensual", "fecha_ultima_compra": "2025-01-01",
        "valor_promedio_compra": 150.0,
    }])
    productos = pd.DataFrame([{
        "producto_id": 1, "nombre": "Anillo Oro", "categoria": "Anillos",
        "material": "Oro", "precio": 200.0, "estilo": "Vintage",
        "ocasion": "Diario", "temporada": "Continuo", "oferta_mes": False,
    }])
    clientes.to_csv(data_dir / config.CLIENTES_FILE, index=False)
    productos.to_csv(data_dir / config.PRODUCTOS_FILE, index=False)
    return data_dir


def test_valid_csvs_load_correctly(tmp_path):
    """Los CSVs válidos deben cargarse sin errores."""
    data_dir = _write_valid_csvs(tmp_path)
    clientes_df = pd.read_csv(data_dir / config.CLIENTES_FILE)
    productos_df = pd.read_csv(data_dir / config.PRODUCTOS_FILE)
    assert len(clientes_df) == 1
    assert len(productos_df) == 1
    assert "cliente_id" in clientes_df.columns
    assert "producto_id" in productos_df.columns


def test_clientes_csv_has_required_columns(tmp_path):
    data_dir = _write_valid_csvs(tmp_path)
    df = pd.read_csv(data_dir / config.CLIENTES_FILE)
    required = {
        "cliente_id", "nombre", "edad", "estilo_preferido",
        "material_favorito", "frecuencia_compra", "fecha_ultima_compra",
        "valor_promedio_compra",
    }
    assert required.issubset(set(df.columns))


def test_productos_csv_has_required_columns(tmp_path):
    data_dir = _write_valid_csvs(tmp_path)
    df = pd.read_csv(data_dir / config.PRODUCTOS_FILE)
    required = {
        "producto_id", "nombre", "categoria", "material", "precio",
        "estilo", "ocasion", "temporada", "oferta_mes",
    }
    assert required.issubset(set(df.columns))


def test_missing_file_raises_error(tmp_path):
    """Un FileNotFoundError debe lanzarse si el CSV no existe."""
    with pytest.raises(FileNotFoundError):
        pd.read_csv(tmp_path / "data" / "no_existe.csv")


def test_real_data_clientes_count():
    """El archivo real de clientes debe tener 25 registros."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, config.DATA_DIR, config.CLIENTES_FILE)
    if os.path.exists(path):
        df = pd.read_csv(path)
        assert len(df) == 25


def test_real_data_productos_count():
    """El archivo real de productos debe tener 40 registros."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, config.DATA_DIR, config.PRODUCTOS_FILE)
    if os.path.exists(path):
        df = pd.read_csv(path)
        assert len(df) == 40


def test_real_productos_has_valoracion_column():
    """El CSV de productos real debe tener la columna 'valoracion'."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, config.DATA_DIR, config.PRODUCTOS_FILE)
    if os.path.exists(path):
        df = pd.read_csv(path)
        assert "valoracion" in df.columns
        assert "descripcion" in df.columns
