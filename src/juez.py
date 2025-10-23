"""
LLM-Juez para Validación de Calidad

Evalúa objetivamente la calidad de respuestas comparándolas.
Implementado durante el hackathon (23 oct 2025).
"""

from src.contador import medir_llamada_llm
from typing import Dict, Any


def juez_llm(respuesta_a: str, respuesta_b: str, tarea: str) -> Dict[str, Any]:
    """
    Compara dos respuestas usando un LLM como juez objetivo.

    Args:
        respuesta_a (str): Primera respuesta a evaluar.
        respuesta_b (str): Segunda respuesta a evaluar.
        tarea (str): La tarea/pregunta original.

    Returns:
        dict: Resultado con ganador, puntajes, justificación y métricas.
            {
                "ganador": "A" | "B" | "empate",
                "puntaje_a": float (0-10),
                "puntaje_b": float (0-10),
                "justificacion": str,
                "metricas_juez": dict
            }
    """
    
    # Prompt objetivo para el juez
    prompt = f"""Eres un juez objetivo que evalúa la calidad de respuestas.

TAREA ORIGINAL: {tarea}

RESPUESTA A:
{respuesta_a}

RESPUESTA B:
{respuesta_b}

Evalúa ambas respuestas considerando:
1. Corrección: ¿La información es correcta?
2. Completitud: ¿Responde completamente la pregunta?
3. Claridad: ¿Es fácil de entender?
4. Concisión: ¿Es clara sin ser excesivamente larga?

Responde EXACTAMENTE en este formato:
GANADOR: [A o B o EMPATE]
PUNTAJE_A: [número de 0 a 10]
PUNTAJE_B: [número de 0 a 10]
JUSTIFICACION: [breve explicación de tu decisión]
"""
    
    mensajes = [{"role": "user", "content": prompt}]
    
    # Usar GPT-4o-mini para juzgar (barato, rápido y mejor que 3.5)
    respuesta, metricas = medir_llamada_llm(
        modelo="gpt-4o-mini",
        mensajes=mensajes
    )
    
    # Manejar error de API
    if respuesta is None:
        return {
            "ganador": "error",
            "puntaje_a": 0.0,
            "puntaje_b": 0.0,
            "justificacion": "Error al llamar al juez LLM",
            "metricas_juez": metricas,
            "error": metricas.get("error", "Error desconocido")
        }
    
    # Parsear respuesta del juez (robusto)
    resultado = {
        "ganador": "empate",
        "puntaje_a": 5.0,
        "puntaje_b": 5.0,
        "justificacion": respuesta,
        "metricas_juez": metricas
    }
    
    # Parsear línea por línea
    lineas = respuesta.split('\n')
    for linea in lineas:
        linea_upper = linea.upper().strip()
        
        # Detectar ganador
        if "GANADOR:" in linea_upper:
            if "A" in linea_upper and "EMPATE" not in linea_upper:
                resultado["ganador"] = "A"
            elif "B" in linea_upper:
                resultado["ganador"] = "B"
            elif "EMPATE" in linea_upper:
                resultado["ganador"] = "empate"
        
        # Detectar puntaje A
        elif "PUNTAJE_A:" in linea_upper or "PUNTAJE A:" in linea_upper:
            try:
                # Extraer número después de los dos puntos
                puntaje_str = linea.split(":")[-1].strip()
                # Remover cualquier texto adicional
                puntaje_str = ''.join(c for c in puntaje_str if c.isdigit() or c == '.')
                resultado["puntaje_a"] = float(puntaje_str)
            except (ValueError, IndexError):
                pass  # Mantener default
        
        # Detectar puntaje B
        elif "PUNTAJE_B:" in linea_upper or "PUNTAJE B:" in linea_upper:
            try:
                puntaje_str = linea.split(":")[-1].strip()
                puntaje_str = ''.join(c for c in puntaje_str if c.isdigit() or c == '.')
                resultado["puntaje_b"] = float(puntaje_str)
            except (ValueError, IndexError):
                pass  # Mantener default
        
        # Detectar justificación
        elif "JUSTIFICACION:" in linea_upper or "JUSTIFICACIÓN:" in linea_upper:
            try:
                justif = linea.split(":", 1)[-1].strip()
                if justif:
                    resultado["justificacion"] = justif
            except IndexError:
                pass
    
    return resultado