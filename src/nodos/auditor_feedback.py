"""
Nodo 5: Auditor de Feedback

LLM-Crítico que analiza métricas y genera recomendación de optimización.
"""

from typing import Dict, Any, Optional
import json
from math import fabs
from src.utils import llamar_openai_simple

# Benchmarks de eficiencia por tipo de tarea
BENCHMARKS_POR_TIPO = {
    "resumen": {
        "modelo_optimo": "gpt-3.5-turbo",
        "tokens_esperados": 200,
        "razon": "Tareas de resumen no requieren razonamiento complejo"
    },
    "traduccion": {
        "modelo_optimo": "gpt-3.5-turbo",
        "tokens_esperados": 250,
        "razon": "Traducción básica funciona bien con modelos económicos"
    },
    "clasificacion": {
        "modelo_optimo": "gpt-3.5-turbo",
        "tokens_esperados": 150,
        "razon": "Clasificación simple es eficiente con modelos base"
    },
    "extraccion": {
        "modelo_optimo": "gpt-3.5-turbo",
        "tokens_esperados": 300,
        "razon": "Extracción de datos no requiere razonamiento avanzado"
    },
    "analisis": {
        "modelo_optimo": "gpt-4o",
        "tokens_esperados": 800,
        "razon": "Análisis profundo requiere mayor capacidad de razonamiento"
    },
    "codigo": {
        "modelo_optimo": "gpt-4o",
        "tokens_esperados": 500,
        "razon": "Generación de código requiere precisión y contexto"
    },
    "creatividad": {
        "modelo_optimo": "gpt-4o",
        "tokens_esperados": 600,
        "razon": "Tareas creativas se benefician de mayor capacidad"
    },
    "qa": {
        "modelo_optimo": "gpt-3.5-turbo",
        "tokens_esperados": 400,
        "razon": "Q&A general funciona bien con modelos base"
    },
    "comparacion": {
        "modelo_optimo": "gpt-4o",
        "tokens_esperados": 700,
        "razon": "Comparaciones requieren análisis profundo"
    },
    "general": {
        "modelo_optimo": "gpt-3.5-turbo",
        "tokens_esperados": 300,
        "razon": "Tareas generales usan modelo económico por defecto"
    }
}


def calcular_costo(modelo: str, tokens: int) -> float:
    """
    Calcula el costo estimado basado en el modelo y tokens.
    """
    costos = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60}
    }
    
    if modelo not in costos:
        return 0.0
    
    # Asumimos 70% input, 30% output como aproximación
    input_tokens = int(tokens * 0.7)
    output_tokens = tokens - input_tokens
    
    costo = (input_tokens * costos[modelo]["input"] + 
             output_tokens * costos[modelo]["output"]) / 1_000_000
    
    return round(costo, 4)

def validar_json_feedback(data: Dict[str, Any]) -> bool:
    """
    Valida que el JSON de feedback tenga todos los campos requeridos.
    """
    campos_requeridos = {"requiere_optimizacion", "analisis", "recomendacion"}
    return all(campo in data for campo in campos_requeridos)

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
    
    # Obtener benchmark
    benchmark = BENCHMARKS_POR_TIPO.get(tipo_tarea, BENCHMARKS_POR_TIPO["general"])
    
    # Calcular costos y diferencias
    costo_actual = calcular_costo(modelo_usado, tokens)
    costo_optimo = calcular_costo(benchmark["modelo_optimo"], benchmark["tokens_esperados"])
    diferencia_costo = abs(costo_actual - costo_optimo) / costo_optimo * 100
    
    # Si hay exceso de tokens, optimizar directamente
    tokens_excedidos = tokens > benchmark["tokens_esperados"] * 2
    if tokens_excedidos:
        state["feedback_auditor"] = {
            "requiere_optimizacion": True,
            "analisis": f"Uso excesivo de tokens: {tokens} vs {benchmark['tokens_esperados']} esperados",
            "recomendacion": benchmark["modelo_optimo"]
        }
        print(f"⚠️ Uso excesivo de tokens detectado: {tokens} vs {benchmark['tokens_esperados']} esperados")
        return state
    
    # Si usamos modelo barato o la diferencia es < 20%, no optimizar
    if (modelo_usado in ["gpt-3.5-turbo", "gpt-4o-mini"] or diferencia_costo < 20):
        state["feedback_auditor"] = {
            "requiere_optimizacion": False,
            "analisis": f"Modelo {modelo_usado} es eficiente (diferencia: {diferencia_costo:.1f}%)",
            "recomendacion": modelo_usado
        }
        print(f"✅ Modelo {modelo_usado} es óptimo - diferencia de costo: {diferencia_costo:.1f}%")
        return state
    
    # Analizar uso excesivo de tokens
    tokens_excedidos = tokens > benchmark["tokens_esperados"] * 2
    razon_tokens = tokens / benchmark["tokens_esperados"]
    
    print(f"🔍 Auditando: {tipo_tarea} con {modelo_usado} ({tokens} tokens vs {benchmark['tokens_esperados']} esperados)")
    
    # Prompt del Auditor mejorado
    prompt = f"""Eres un Auditor Senior de Eficiencia en APIs de IA.

CONTEXTO DE LA EJECUCIÓN:
- Tipo de tarea: {tipo_tarea}
- Modelo usado: {modelo_usado}
- Tokens consumidos: {tokens} (ratio: {razon_tokens:.1f}x esperado)
- Costo estimado: ${costo_actual:.4f}

BENCHMARK PARA "{tipo_tarea}":
- Modelo óptimo: {benchmark['modelo_optimo']}
- Tokens esperados: {benchmark['tokens_esperados']}
- Razón: {benchmark['razon']}
- Costo benchmark: ${costo_optimo:.4f}

TABLA DE COSTOS (por 1M tokens):
┌──────────────┬────────┬─────────┐
│ Modelo       │ Input  │ Output  │
├──────────────┼────────┼─────────┤
│ GPT-4o       │ $2.50  │ $10.00  │
│ GPT-3.5      │ $0.50  │ $1.50   │
│ GPT-4o-mini  │ $0.15  │ $0.60   │
└──────────────┴────────┴─────────┘

INSTRUCCIONES:
1. Compara el modelo usado con el benchmark
2. Analiza si hubo desperdicio de recursos {f'ALERTA: {razon_tokens:.1f}x tokens esperados!' if tokens_excedidos else ''}
3. Considera calidad vs costo (diferencia: {diferencia_costo:.1f}%)
4. Responde en JSON exacto:

{{
    "requiere_optimizacion": true/false,
    "analisis": "explicación técnica en 1-2 líneas",
    "recomendacion": "modelo_recomendado" o "ninguna"
}}

IMPORTANTE:
- Si modelo usado == modelo óptimo → requiere_optimizacion: false
- Si usaste GPT-4o para tarea simple → requiere_optimizacion: true
- Si usaste GPT-3.5 para tarea compleja → revisar calidad antes
- Si diferencia costo < 20% → no optimizar
- Si tokens > 2x esperados → investigar causa
"""
    
    try:
        # Llamar a OpenAI usando la función de utils
        feedback_text = llamar_openai_simple(
            prompt=prompt,
            modelo="gpt-4o-mini"  # Auditor usa modelo barato
        ).strip()
        
        # Parsear JSON con mejor manejo de errores
        try:
            # Extraer JSON si está en un bloque de código
            if "```" in feedback_text:
                feedback_text = feedback_text.split("```")[1].split("```")[0].strip()
                if feedback_text.startswith("json"):
                    feedback_text = feedback_text[4:].strip()
            
            feedback = json.loads(feedback_text)
            
            # Validar estructura del JSON
            if not validar_json_feedback(feedback):
                raise ValueError("JSON incompleto")
                
        except (json.JSONDecodeError, ValueError) as e:
            print(f"⚠️ Error al parsear JSON: {str(e)}")
            # Feedback por defecto basado en heurísticas
            feedback = {
                "requiere_optimizacion": (
                    tokens_excedidos or 
                    ("gpt-4o" in modelo_usado and benchmark["modelo_optimo"] == "gpt-3.5-turbo")
                ),
                "analisis": (
                    "Tokens excedidos" if tokens_excedidos 
                    else "Modelo más potente que el necesario"
                ),
                "recomendacion": benchmark["modelo_optimo"]
            }
        
        state["feedback_auditor"] = feedback
        
        print(f"📋 Auditoría completada:")
        print(f"   - Optimizar: {feedback['requiere_optimizacion']}")
        print(f"   - Análisis: {feedback['analisis']}")
        print(f"   - Recomendación: {feedback['recomendacion']}")
        if tokens_excedidos:
            print(f"   ⚠️ Alerta: {razon_tokens:.1f}x tokens esperados")
        
    except Exception as e:
        print(f"❌ Error en auditoría: {e}")
        state["feedback_auditor"] = {
            "requiere_optimizacion": False,
            "analisis": f"Error en auditoría: {str(e)}",
            "recomendacion": modelo_usado
        }
    
    return state
