"""
Pruebas unitarias para métricas y visualización.
Usar: pytest -v
"""

import sys
import os
import pytest

# Asegurar que src esté en el path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils_metricas import calcular_costo
from src.visualizador import ComparadorRuns


def test_calcular_costo():
    """Verifica cálculo de costos"""
    costo = calcular_costo("gpt-4o", 1000, 500)
    assert costo > 0
    # gpt-4o: (1000/1M * 2.5) + (500/1M * 10) = 0.0075
    assert round(costo, 4) == 0.0075 or pytest.approx(costo, rel=1e-3)


def test_comparador():
    """Verifica comparador funciona"""
    run1 = {"tokens_totales": 100, "costo_total": 0.001}
    run2 = {"tokens_totales": 50, "costo_total": 0.0005}

    comp = ComparadorRuns(run1, run2)

    try:
        comp.mostrar_comparacion()
    except Exception as e:
        pytest.fail(f"ComparadorRuns lanzó una excepción inesperada: {e}")
