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
        modelo = state.get("modelo_a_usar", "desconocido")
        
        # 🆕 Calcular latencia real desde time tracking
        tiempo_inicio = state.get("tiempo_inicio", 0)
        tiempo_fin = state.get("tiempo_fin", 0)
        latencia_segundos = tiempo_fin - tiempo_inicio if tiempo_fin > tiempo_inicio else 0.0
        
        # 🆕 Calcular costo real en USD (precios OpenAI)
        PRECIOS = {
            "gpt-4o": {"input": 0.0025 / 1000, "output": 0.01 / 1000},  # $2.50 / $10 por 1M tokens
            "gpt-4o-mini": {"input": 0.00015 / 1000, "output": 0.0006 / 1000},  # $0.15 / $0.60 por 1M tokens
            "gpt-3.5-turbo": {"input": 0.0005 / 1000, "output": 0.0015 / 1000},  # $0.50 / $1.50 por 1M tokens
        }
        
        precios_modelo = PRECIOS.get(modelo, {"input": 0, "output": 0})
        costo_input = usage.prompt_tokens * precios_modelo["input"]
        costo_output = usage.completion_tokens * precios_modelo["output"]
        costo_total = costo_input + costo_output
        
        metricas = {
            "tokens_totales": usage.total_tokens,
            "tokens_prompt": usage.prompt_tokens,
            "tokens_completion": usage.completion_tokens,
            "latencia": round(latencia_segundos, 3),  # 🆕 Latencia real
            "costo_total": round(costo_total, 6),  # 🆕 Costo en USD
            "modelo_usado": modelo
        }
        
        state["metricas_ejecucion"] = metricas
        
        print(f"📊 Métricas capturadas:")
        print(f"   - Tokens totales: {metricas['tokens_totales']}")
        print(f"   - Tokens prompt: {metricas['tokens_prompt']}")
        print(f"   - Tokens completion: {metricas['tokens_completion']}")
        print(f"   - Latencia: {metricas['latencia']}s")
        print(f"   - Costo: ${metricas['costo_total']:.6f}")
        print(f"   - Modelo: {metricas['modelo_usado']}")
        
    except Exception as e:
        print(f"⚠️  Error extrayendo métricas: {e}")
        state["metricas_ejecucion"] = {
            "tokens_totales": 0,
            "error": str(e)
        }
    
    return state
