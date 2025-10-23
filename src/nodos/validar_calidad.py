"""
Nodo 3: Validación de Calidad

Este nodo valida la calidad de la respuesta usando un LLM-Juez.
Implementado durante el hackathon (23 oct 2025).
"""

from src.juez import juez_llm
from src.contador import medir_llamada_llm
from typing import Dict, Any, Optional


def validar_calidad(respuesta: str, baseline: Optional[str] = None, tarea: Optional[str] = None) -> Dict[str, Any]:
    """
    Compara respuesta con baseline usando LLM-Juez.

    Args:
        respuesta (str): Respuesta generada por el modelo seleccionado.
        baseline (str, optional): Respuesta de comparación (ej: GPT-4). 
                                  Si es None, se genera una.
        tarea (str, optional): Tarea original para contexto.

    Returns:
        dict: Métricas de calidad y ahorro.
            {
                "mejor": "respuesta" | "baseline" | "empate",
                "puntaje_respuesta": float,
                "puntaje_baseline": float,
                "ahorro_tokens": int,
                "mejora_vs_baseline": str,
                "metricas": dict
            }
    """
    
    # Si no hay baseline, generar uno con GPT-4
    if baseline is None or baseline == "":
        if tarea:
            baseline, metricas_baseline = _generar_baseline(tarea)
        else:
            # No podemos generar baseline sin tarea
            return {
                "error": "No se proporcionó baseline ni tarea para generarlo",
                "puntaje_respuesta": 0.0,
                "puntaje_baseline": 0.0,
                "ahorro_tokens": 0,
                "metricas": {}
            }
    else:
        metricas_baseline = {"tokens_totales": len(baseline.split())}  # Aproximación
    
    # Asegurar que tenemos tarea
    if tarea is None:
        tarea = "Comparar calidad de respuestas"
    
    # Llamar al juez para comparar
    juicio = juez_llm(
        respuesta_a=respuesta,
        respuesta_b=baseline,
        tarea=tarea
    )
    
    # Verificar si hubo error
    if "error" in juicio:
        return {
            "error": juicio["error"],
            "puntaje_respuesta": juicio["puntaje_a"],
            "puntaje_baseline": juicio["puntaje_b"],
            "ahorro_tokens": 0,
            "metricas": juicio.get("metricas_juez", {})
        }
    
    # Calcular ahorro de tokens (aproximación)
    tokens_respuesta = len(respuesta.split())
    tokens_baseline = len(baseline.split())
    ahorro_tokens = tokens_baseline - tokens_respuesta
    
    # Determinar mejora
    if juicio["ganador"] == "A":
        mejor = "respuesta"
        mejora = "✅ Respuesta optimizada es mejor"
    elif juicio["ganador"] == "B":
        mejor = "baseline"
        mejora = "⚠️ Baseline es mejor (considerar usar modelo más potente)"
    else:
        mejor = "empate"
        mejora = "🟰 Calidad similar"
    
    # Construir resultado
    resultado = {
        "mejor": mejor,
        "puntaje_respuesta": juicio["puntaje_a"],
        "puntaje_baseline": juicio["puntaje_b"],
        "ahorro_tokens": ahorro_tokens,
        "mejora_vs_baseline": mejora,
        "justificacion": juicio["justificacion"],
        "metricas": {
            "tokens_respuesta": tokens_respuesta,
            "tokens_baseline": tokens_baseline,
            "juez": juicio.get("metricas_juez", {})
        }
    }
    
    return resultado


def _generar_baseline(tarea: str) -> tuple[str, Dict[str, Any]]:
    """
    Genera una respuesta baseline usando GPT-4.1 (mejor modelo disponible).

    Args:
        tarea (str): La tarea a resolver.

    Returns:
        tuple: (respuesta_baseline, metricas)
    """
    mensajes = [
        {"role": "system", "content": "Eres un asistente útil y preciso."},
        {"role": "user", "content": tarea}
    ]
    
    respuesta, metricas = medir_llamada_llm(
        modelo="gpt-4.1",  # Mejor modelo disponible para baseline
        mensajes=mensajes
    )
    
    if respuesta is None:
        # Fallback si falla GPT-4.1
        return "Error al generar baseline", metricas
    
    return respuesta, metricas