"""
LLM-Juez para Validación de Calidad

Evalúa objetivamente la calidad de respuestas comparándolas.
Implementado durante el hackathon (23 oct 2025).

MEJORAS:
- Fallback robusto si el juez falla (rate limit, timeout, etc.)
- Heurística simple basada en longitud y detección de errores
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
{respuesta_a[:2000]}

RESPUESTA B:
{respuesta_b[:2000]}

Evalúa ambas respuestas considerando:
1. Corrección: ¿La información es correcta?
2. Completitud: ¿Responde completamente la pregunta?
3. Claridad: ¿Es fácil de entender?
4. Concisión: ¿Es clara sin ser excesivamente larga?

IMPORTANTE:
- Para tareas simples, valora la concisión
- Para tareas complejas, valora la profundidad
- NO favorezcas respuestas largas automáticamente

Responde EXACTAMENTE en este formato:
GANADOR: [A o B o EMPATE]
PUNTAJE_A: [número de 0 a 10]
PUNTAJE_B: [número de 0 a 10]
JUSTIFICACION: [breve explicación de tu decisión]
"""
    
    mensajes = [{"role": "user", "content": prompt}]
    
    try:
        # Usar GPT-4o-mini para juzgar (barato, rápido y mejor que 3.5)
        respuesta, metricas = medir_llamada_llm(
            modelo="gpt-4o-mini",
            mensajes=mensajes
        )
        
        # Manejar error de API
        if respuesta is None or metricas.get("error"):
            raise Exception(metricas.get("error", "Error al llamar al juez"))
        
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
                    puntaje_str = linea.split(":")[-1].strip()
                    puntaje_str = ''.join(c for c in puntaje_str if c.isdigit() or c == '.')
                    resultado["puntaje_a"] = float(puntaje_str)
                except (ValueError, IndexError):
                    pass
            
            # Detectar puntaje B
            elif "PUNTAJE_B:" in linea_upper or "PUNTAJE B:" in linea_upper:
                try:
                    puntaje_str = linea.split(":")[-1].strip()
                    puntaje_str = ''.join(c for c in puntaje_str if c.isdigit() or c == '.')
                    resultado["puntaje_b"] = float(puntaje_str)
                except (ValueError, IndexError):
                    pass
            
            # Detectar justificación
            elif "JUSTIFICACION:" in linea_upper or "JUSTIFICACIÓN:" in linea_upper:
                try:
                    justif = linea.split(":", 1)[-1].strip()
                    if justif:
                        resultado["justificacion"] = justif
                except IndexError:
                    pass
        
        return resultado
    
    # 🆕 FIX #3: FALLBACK ROBUSTO SI JUEZ FALLA
    except Exception as e:
        print(f"⚠️  Juez LLM no disponible ({type(e).__name__}) - Usando heurística simple")
        
        # Fallback: Comparación por longitud y detección de errores
        len_a = len(respuesta_a)
        len_b = len(respuesta_b)
        
        # Detectar errores obvios
        errores_a = any(kw in respuesta_a[:200].lower() for kw in ['error', '❌', 'no puedo', 'lo siento', '⚠️'])
        errores_b = any(kw in respuesta_b[:200].lower() for kw in ['error', '❌', 'no puedo', 'lo siento', '⚠️'])
        
        if errores_a and not errores_b:
            return {
                "ganador": "B",
                "puntaje_a": 3.0,
                "puntaje_b": 7.0,
                "justificacion": f"⚠️ Juez no disponible. Fallback: A tiene error, B válida.",
                "metricas_juez": {}
            }
        
        if errores_b and not errores_a:
            return {
                "ganador": "A",
                "puntaje_a": 7.0,
                "puntaje_b": 3.0,
                "justificacion": f"⚠️ Juez no disponible. Fallback: B tiene error, A válida.",
                "metricas_juez": {}
            }
        
        # Detectar si tarea pide respuesta larga
        tarea_larga = any(kw in tarea.lower() for kw in ['ensayo', 'detallado', 'completo', 'extenso', 'palabras'])
        
        if tarea_larga:
            # Tarea larga: más largo = mejor
            if len_a > len_b * 1.3:
                return {
                    "ganador": "A",
                    "puntaje_a": 7.0,
                    "puntaje_b": 6.0,
                    "justificacion": f"⚠️ Juez no disponible. Fallback: Tarea extensa, A más completa ({len_a} vs {len_b} chars).",
                    "metricas_juez": {}
                }
            elif len_b > len_a * 1.3:
                return {
                    "ganador": "B",
                    "puntaje_a": 6.0,
                    "puntaje_b": 7.0,
                    "justificacion": f"⚠️ Juez no disponible. Fallback: Tarea extensa, B más completa ({len_b} vs {len_a} chars).",
                    "metricas_juez": {}
                }
        
        # Default: empate conservador
        return {
            "ganador": "empate",
            "puntaje_a": 6.0,
            "puntaje_b": 6.0,
            "justificacion": f"⚠️ Juez no disponible ({type(e).__name__}). Fallback: Ambas respuestas parecen válidas.",
            "metricas_juez": {}
        }