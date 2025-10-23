"""
Nodo 2: Generación y Refinamiento

Este nodo genera la respuesta inicial y la refina usando un solo LLM.
Implementa Self-Refine para mejorar iterativamente las respuestas.
"""

from typing import Dict, Optional
from openai import OpenAI
import os
from ..prompts import PROMPT_INICIAL, PROMPT_REFINAMIENTO, PROMPT_VALIDACION
from ..utils import client

def generar_y_refinar(tarea: str, complejidad: str) -> Dict:
    """
    Genera respuesta y la refina con auto-feedback.

    Args:
        tarea (str): Tarea a resolver.
        complejidad (str): Nivel de complejidad ("baja", "media", "alta")

    Returns:
        Dict: {
            "respuesta_inicial": str,
            "respuesta_refinada": str,
            "modelo_usado": str,
            "metricas": Dict
        }
    """
    # Seleccionar modelo basado en complejidad
    if complejidad == "baja":
        modelo = "gpt-4o-mini"  # Versión ligera para tareas simples
    else:  # media o alta
        modelo = "gpt-4o"  # Versión completa para tareas complejas
    
    # Generar respuesta inicial
    respuesta_inicial = generar_respuesta(tarea, modelo)
    
    # Refinar respuesta
    respuesta_refinada = refinar_respuesta(tarea, respuesta_inicial, modelo)
    
    # Validar calidad
    metricas = validar_respuesta(tarea, respuesta_refinada, modelo)
    
    return {
        "respuesta_inicial": respuesta_inicial,
        "respuesta_refinada": respuesta_refinada,
        "modelo_usado": modelo,
        "metricas": metricas
    }

def generar_respuesta(tarea: str, modelo: str) -> str:
    """Genera la respuesta inicial usando el modelo especificado."""
    prompt = PROMPT_INICIAL.format(tarea=tarea)
    response = client.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def refinar_respuesta(tarea: str, respuesta_inicial: str, modelo: str) -> str:
    """Refina la respuesta usando Self-Refine."""
    prompt = PROMPT_REFINAMIENTO.format(
        tarea=tarea,
        respuesta_inicial=respuesta_inicial
    )
    response = client.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def validar_respuesta(tarea: str, respuesta_refinada: str, modelo: str) -> Dict:
    """Valida la calidad de la respuesta refinada."""
    prompt = PROMPT_VALIDACION.format(
        tarea=tarea,
        respuesta_refinada=respuesta_refinada
    )
    response = client.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return {"evaluacion": response.choices[0].message.content}
