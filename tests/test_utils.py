"""
Tests para utilidades del sistema (utils.py)
"""
import pytest
from src.utils import client
import os


def test_client_inicializado():
    """Test que el cliente de OpenAI está correctamente inicializado."""
    assert client is not None
    assert hasattr(client, 'chat')


def test_api_key_configurada():
    """Test que la API key está configurada en el entorno."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Si no hay API key, el test debe advertir
    if not api_key:
        pytest.skip("API key no configurada (esperado en CI/CD)")
    
    assert api_key is not None
    assert len(api_key) > 20  # Las API keys de OpenAI son largas