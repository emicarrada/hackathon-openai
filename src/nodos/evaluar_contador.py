"""
Nodo 4: Evaluar con Contador

Extrae métricas de tokens y latencia de la ejecución.
"""

from typing import Dict, Any
import time


def evaluar_con_contador(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evalúa la respuesta del modelo de OpenAI y calcula métricas detalladas
    de rendimiento, costo y eficiencia.

    Métricas calculadas:
        - tokens_totales, tokens_prompt, tokens_completion
        - latencia real (segundos)
        - costo_total (USD)
        - tokens_por_segundo
        - eficiencia (tokens_por_dólar)

    Args:
        state (Dict[str, Any]): Estado del flujo, debe contener:
            - respuesta_raw: respuesta del modelo OpenAI
            - tiempo_inicio: timestamp (float) guardado antes de la ejecución
            - modelo_a_usar: nombre del modelo usado

    Returns:
        Dict[str, Any]: Estado actualizado con la clave "metricas_ejecucion"
    """

    # Precios en USD por 1M de tokens (input/output)
    PRECIOS_POR_MODELO = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    }

    respuesta_raw = state.get("respuesta_raw")
    modelo = state.get("modelo_a_usar", "desconocido")
    tiempo_inicio = state.get("tiempo_inicio", None)

    # Si no hay respuesta, devolver métricas vacías
    if respuesta_raw is None:
        state["metricas_ejecucion"] = {
            "tokens_totales": 0,
            "tokens_prompt": 0,
            "tokens_completion": 0,
            "latencia": 0.0,
            "costo_total": 0.0,
            "tokens_por_segundo": 0.0,
            "eficiencia": 0.0,
            "modelo_usado": modelo,
        }
        return state

    try:
        # Extraer métricas de uso del objeto respuesta
        usage = getattr(respuesta_raw, "usage", None)
        if usage is None:
            raise AttributeError("La respuesta no contiene información de usage.")

        tokens_totales = getattr(usage, "total_tokens", 0)
        tokens_prompt = getattr(usage, "prompt_tokens", 0)
        tokens_completion = getattr(usage, "completion_tokens", 0)

        # Calcular latencia real
        latencia = time.time() - tiempo_inicio if tiempo_inicio else 0.0

        # Calcular costo total
        precios = PRECIOS_POR_MODELO.get(modelo, {"input": 0.0, "output": 0.0})
        costo_input = (tokens_prompt / 1_000_000) * precios["input"]
        costo_output = (tokens_completion / 1_000_000) * precios["output"]
        costo_total = costo_input + costo_output

        # Calcular métricas derivadas
        tokens_por_segundo = tokens_totales / latencia if latencia > 0 else 0.0
        eficiencia = tokens_totales / costo_total if costo_total > 0 else 0.0

        # Construir dict final
        metricas_ejecucion = {
            "tokens_totales": tokens_totales,
            "tokens_prompt": tokens_prompt,
            "tokens_completion": tokens_completion,
            "latencia": round(latencia, 4),
            "costo_total": round(costo_total, 8),
            "tokens_por_segundo": round(tokens_por_segundo, 2),
            "eficiencia": round(eficiencia, 2),
            "modelo_usado": modelo,
        }

        state["metricas_ejecucion"] = metricas_ejecucion

        # Log informativo
        print("📊 Métricas capturadas:")
        for k, v in metricas_ejecucion.items():
            print(f"   - {k}: {v}")

    except Exception as e:
        print(f"⚠️  Error al evaluar métricas: {e}")
        state["metricas_ejecucion"] = {
            "tokens_totales": 0,
            "error": str(e),
            "modelo_usado": modelo,
        }

    return state

