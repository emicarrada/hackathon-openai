"""
Nodo 4: Evaluar con Contador

Extrae métricas de tokens y latencia de la ejecución.
"""

from typing import Dict, Any
import time


def evaluar_con_contador(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extrae métricas de la respuesta de OpenAI.
    
    Args:
        state (dict): Estado con respuesta_raw.
        
    Returns:
        dict: Estado con metricas_ejecucion.
    """
    respuesta_raw = state.get("respuesta_raw")
    
    if respuesta_raw is None:
        state["metricas_ejecucion"] = {
            "tokens_totales": 0,
            "tokens_prompt": 0,
            "tokens_completion": 0,
            "latencia": 0.0,
            "modelo_usado": state.get("modelo_a_usar", "desconocido")
        }
        return state
    
    try:
        # Extraer métricas de usage
        usage = respuesta_raw.usage
        
        metricas = {
            "tokens_totales": usage.total_tokens,
            "tokens_prompt": usage.prompt_tokens,
            "tokens_completion": usage.completion_tokens,
            "latencia": 0.0,  # Se medirá en el futuro con time tracking
            "modelo_usado": state.get("modelo_a_usar", "desconocido")
        }
        
        state["metricas_ejecucion"] = metricas
        
        print(f"📊 Métricas capturadas:")
        print(f"   - Tokens totales: {metricas['tokens_totales']}")
        print(f"   - Tokens prompt: {metricas['tokens_prompt']}")
        print(f"   - Tokens completion: {metricas['tokens_completion']}")
        print(f"   - Modelo: {metricas['modelo_usado']}")
        
    except Exception as e:
        print(f"⚠️  Error extrayendo métricas: {e}")
        state["metricas_ejecucion"] = {
            "tokens_totales": 0,
            "error": str(e)
        }
    
    return state
