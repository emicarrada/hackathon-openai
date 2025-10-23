"""
Utilidades para interactuar con la API de OpenAI.
Maneja la inicialización del cliente y llamadas básicas.
"""

from openai import OpenAI
import os
from typing import Optional, Any

def inicializar_openai() -> OpenAI:
    """
    Inicializa y retorna un cliente de OpenAI.
    
    Returns:
        OpenAI: Cliente inicializado con la API key del ambiente
    
    Raises:
        ValueError: Si no hay API key configurada
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY no está configurada en el ambiente")
    return OpenAI(api_key=api_key)

def llamar_openai_simple(prompt: str, modelo: str = "gpt-3.5-turbo") -> str:
    """
    Realiza una llamada simple a la API de OpenAI.
    
    Args:
        prompt (str): El prompt a enviar
        modelo (str): Modelo a usar (default: gpt-3.5-turbo)
    
    Returns:
        str: La respuesta del modelo
    
    Raises:
        Exception: Si hay error en la llamada a la API
    """
    try:
        cliente = inicializar_openai()
        response = cliente.chat.completions.create(
            model=modelo,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error al llamar a OpenAI: {str(e)}")
        raise

# Cliente global (se inicializa solo si hay API key)
try:
    client = inicializar_openai()
except ValueError:
    client = None  # Fallback seguro si no hay API key