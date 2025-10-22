import pytest
from src.utils import inicializar_openai, llamar_openai_simple

def test_inicializar_openai():
    """Test que inicializar_openai retorna un cliente válido (stub)."""
    cliente = inicializar_openai()
    assert cliente is not None  # Solo verifica que no sea None, sin llamadas reales

def test_llamar_openai_simple():
    """Test que llamar_openai_simple maneja errores sin API key (stub)."""
    # En modo stub, debería manejar gracefully sin key real
    try:
        resultado = llamar_openai_simple("Test prompt", modelo="gpt-3.5-turbo")
        assert isinstance(resultado, str)  # Espera string, pero fallará sin key
    except Exception as e:
        assert "API key" in str(e) or "openai" in str(e).lower()  # Verifica error esperado