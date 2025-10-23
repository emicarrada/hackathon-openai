"""
Nodo 5: Auditor de Feedback

LLM-Crítico que analiza métricas y genera recomendación de optimización.
"""

from typing import Dict, Any
from openai import OpenAI
import os
import json


def generar_feedback_auditor(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LLM-Auditor analiza métricas y recomienda optimización.
    
    Args:
        state (dict): Estado con tipo_tarea, metricas_ejecucion, modelo_usado.
        
    Returns:
        dict: Estado con feedback_auditor.
    """
    tipo_tarea = state.get("tipo_tarea", "general")
    metricas = state.get("metricas_ejecucion", {})
    modelo_usado = metricas.get("modelo_usado", "desconocido")
    tokens = metricas.get("tokens_totales", 0)
    
    # Si usamos modelo barato, no auditar
    if modelo_usado in ["gpt-3.5-turbo", "gpt-4o-mini"]:
        state["feedback_auditor"] = {
            "requiere_optimizacion": False,
            "analisis": "Modelo ya optimizado",
            "recomendacion": modelo_usado
        }
        print(f"✅ Modelo {modelo_usado} ya es óptimo - sin auditoría")
        return state
    
    print(f"🔍 Auditando: {tipo_tarea} con {modelo_usado} ({tokens} tokens)...")
    
    # Prompt del Auditor
    prompt = f"""Eres un Auditor de Eficiencia de APIs de IA.

TAREA ANALIZADA:
- Tipo: {tipo_tarea}
- Modelo usado: {modelo_usado}
- Tokens totales: {tokens}

CONTEXTO:
- GPT-4o cuesta 10x más que GPT-3.5-turbo
- GPT-4o-mini cuesta 5x menos que GPT-4o
- Tareas simples (resumen, clasificación) pueden usar modelos más baratos

ANÁLISIS REQUERIDO:
1. ¿El modelo usado fue eficiente para este tipo de tarea?
2. ¿Se podría lograr la misma calidad con un modelo más barato?

RESPONDE EN FORMATO JSON ESTRICTO:
{{
  "requiere_optimizacion": true/false,
  "analisis": "breve análisis de 1-2 líneas",
  "recomendacion": "gpt-3.5-turbo" | "gpt-4o-mini" | "{modelo_usado}"
}}"""
    
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Auditor usa modelo barato
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,  # Más determinístico
            max_tokens=200
        )
        
        feedback_text = response.choices[0].message.content.strip()
        
        # Parsear JSON (robusto)
        try:
            # Buscar JSON en la respuesta
            if "```json" in feedback_text:
                feedback_text = feedback_text.split("```json")[1].split("```")[0].strip()
            elif "```" in feedback_text:
                feedback_text = feedback_text.split("```")[1].split("```")[0].strip()
            
            feedback = json.loads(feedback_text)
        except json.JSONDecodeError:
            # Fallback: parsear manualmente
            feedback = {
                "requiere_optimizacion": "gpt-4o" in modelo_usado or "gpt-4-turbo" in modelo_usado,
                "analisis": "Modelo costoso usado para tarea simple",
                "recomendacion": "gpt-4o-mini"
            }
        
        state["feedback_auditor"] = feedback
        
        print(f"📋 Auditoría completada:")
        print(f"   - Optimizar: {feedback.get('requiere_optimizacion')}")
        print(f"   - Análisis: {feedback.get('analisis')}")
        print(f"   - Recomendación: {feedback.get('recomendacion')}")
        
    except Exception as e:
        print(f"❌ Error en auditoría: {e}")
        state["feedback_auditor"] = {
            "requiere_optimizacion": False,
            "analisis": f"Error: {str(e)}",
            "recomendacion": modelo_usado
        }
    
    return state
