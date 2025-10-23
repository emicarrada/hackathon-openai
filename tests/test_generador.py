"""
Tests para el módulo de generación y refinamiento
"""

import pytest
from src.nodos.generar_refinar import generar_y_refinar

def test_generar_y_refinar_estructura():
    """Prueba que la función retorne la estructura correcta."""
    resultado = generar_y_refinar("Suma 2+2", "baja")
    
    # Verificar estructura del resultado
    assert isinstance(resultado, dict)
    assert "respuesta_inicial" in resultado
    assert "respuesta_refinada" in resultado
    assert "modelo_usado" in resultado
    assert "metricas" in resultado
    
    # Verificar modelo usado
    assert resultado["modelo_usado"] in ["gpt-3.5-turbo", "gpt-4"]

def test_generar_y_refinar_complejidad():
    """Prueba la selección de modelo según complejidad."""
    resultado_baja = generar_y_refinar("Suma 2+2", "baja")
    resultado_alta = generar_y_refinar("Explica la teoría de la relatividad", "alta")
    
    assert resultado_baja["modelo_usado"] == "gpt-3.5-turbo"
    assert resultado_alta["modelo_usado"] == "gpt-4"