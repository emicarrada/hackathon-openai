import pytest
from src.nodos.evaluar_complejidad import evaluar_complejidad
from src.nodos.generar_refinar import generar_refinar
from src.nodos.validar_calidad import validar_calidad

def test_evaluar_complejidad():
    """Test que evaluar_complejidad retorna dict básico (stub)."""
    resultado = evaluar_complejidad("Texto simple")
    assert isinstance(resultado, dict)
    assert "complejidad" in resultado
    assert "modelo" in resultado

def test_generar_refinar():
    """Test que generar_refinar retorna string (stub)."""
    resultado = generar_refinar("Prompt simple", modelo="gpt-3.5-turbo")
    assert isinstance(resultado, str)  # Stub retorna placeholder

def test_validar_calidad():
    """Test que validar_calidad retorna dict (stub)."""
    resultado = validar_calidad("Texto generado", "Texto original")
    assert isinstance(resultado, dict)  # Stub retorna placeholder