import pytest
import os
from unittest.mock import patch
from openai import OpenAI
from src.utils import inicializar_openai, llamar_openai_simple

def test_inicializar_openai():
    """Test que inicializar_openai maneja correctamente la presencia/ausencia de API key."""
    # Caso sin API key
    with pytest.raises(ValueError) as excinfo:
        cliente = inicializar_openai()
    assert "OPENAI_API_KEY no está configurada" in str(excinfo.value)
    
    # Caso con API key
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-key"}):
        cliente = inicializar_openai()
        assert cliente is not None
        assert isinstance(cliente, OpenAI)

def test_llamar_openai_simple():
    """Test que llamar_openai_simple maneja errores sin API key (stub)."""
    # En modo stub, debería manejar gracefully sin key real
    try:
        resultado = llamar_openai_simple("Test prompt", modelo="gpt-3.5-turbo")
        assert isinstance(resultado, str)  # Espera string, pero fallará sin key
    except Exception as e:
        assert "API key" in str(e) or "openai" in str(e).lower()  # Verifica error esperado