import pytest
from src.contador import medir_llamada_llm

def test_medir_llamada_llm_demo():
    """Test que medir_llamada_llm funciona en modo demo (stub)."""
    # Simula una llamada en modo demo
    resultado = medir_llamada_llm("Test prompt", modelo="gpt-3.5-turbo", modo_demo=True)
    assert "demo" in resultado.lower() or isinstance(resultado, dict)  # Verifica respuesta demo

def test_medir_llamada_llm_normal():
    """Test que medir_llamada_llm maneja errores sin API key (stub)."""
    try:
        resultado = medir_llamada_llm("Test prompt", modelo="gpt-3.5-turbo", modo_demo=False)
        assert False  # Debería fallar sin key
    except Exception as e:
        assert "API key" in str(e) or "openai" in str(e).lower()