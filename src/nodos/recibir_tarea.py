"""
Nodo 1: Recibir Tarea

Punto de entrada del sistema. Recibe y clasifica la tarea del usuario.
Implementa clasificación avanzada con keywords y opcionalmente LLM.
"""

from typing import Dict, Any
import os
from src.utils import client, llamar_openai_simple

# Prioridad de tipos para resolver ambigüedades
PRIORIDAD_TIPOS = ["qa", "debug", "comparacion", "codigo", "analisis", "resumen", "traduccion", "clasificacion", "extraccion", "creatividad"]

# Diccionario extendido de tipos de tarea y sus keywords
TIPOS_TAREA = {
    "resumen": ["resume", "resumen", "resumir", "sintetiza", "sinopsis", "abstract", "condensar", "simplificar"],
    "traduccion": ["traduce", "traducir", "translate", "translation", "convertir", "idioma", "lengua", "interpretar"],
    "clasificacion": ["clasifica", "categoriza", "classify", "category", "ordena", "agrupa", "etiqueta", "tipo"],
    "extraccion": ["extrae", "extract", "obtén", "encuentra", "busca", "localiza", "identifica", "detecta"],
    "analisis": ["analiza", "analyze", "evalúa", "assess", "estudia", "investiga", "examina", "diagnostica"],
    "codigo": ["codigo", "code", "programa", "script", "función", "implementa", "desarrolla", "implementación"],
    "creatividad": ["escribe", "crea", "genera", "inventa", "historia", "diseña", "imagina", "compone"],
    "qa": ["pregunta", "responde", "question", "answer", "qué es", "cómo", "por qué", "explica"],
    "comparacion": ["compara", "compare", "diferencias", "vs", "versus", "contrasta", "similar", "diferente"],
    "debug": ["debug", "error", "falla", "arregla", "corrige", "soluciona", "fix", "issue"],
    "general": []  # Fallback
}

def clasificar_con_llm(tarea: str) -> str:
    """
    Usa GPT-4o-mini para clasificar la tarea con alta precisión.
    
    Args:
        tarea (str): Descripción de la tarea a clasificar
        
    Returns:
        str: Categoría detectada (una de las definidas en TIPOS_TAREA)
    """
    prompt = f"""Clasifica esta tarea en UNA de estas categorías:
- resumen
- traduccion
- clasificacion
- extraccion
- analisis
- codigo
- creatividad
- qa
- comparacion
- general

Tarea: "{tarea}"

Responde SOLO con la categoría (una palabra, minúsculas):"""
    
    try:
        categoria = llamar_openai_simple(prompt, modelo="gpt-4o-mini").strip().lower()
        return categoria if categoria in TIPOS_TAREA else "general"
    except Exception as e:
        print(f"⚠️ Error en clasificación LLM: {e}")
        return "general"

def clasificar_por_keywords(tarea: str) -> str:
    """
    Clasifica la tarea usando el diccionario de keywords y prioridades.
    
    Args:
        tarea (str): Descripción de la tarea a clasificar
        
    Returns:
        str: Tipo de tarea detectado
    """
    tarea_lower = tarea.lower()
    tipos_encontrados = set()
    
    # Recolectar todos los tipos que coinciden
    for tipo, keywords in TIPOS_TAREA.items():
        if tipo == "general":
            continue
        if any(keyword in tarea_lower for keyword in keywords):
            tipos_encontrados.add(tipo)
    
    # Si no hay coincidencias, retornar general
    if not tipos_encontrados:
        return "general"
    
    # Si hay múltiples coincidencias, usar prioridad
    for tipo in PRIORIDAD_TIPOS:
        if tipo in tipos_encontrados:
            return tipo
    
    # Si ningún tipo prioritario coincide, retornar el primero encontrado
    return next(iter(tipos_encontrados))
    
    return "general"

def recibir_tarea(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Nodo inicial que recibe la tarea y la clasifica usando keywords y opcionalmente LLM.
    
    Args:
        state (dict): Estado del grafo con la tarea del usuario.
        
    Returns:
        dict: Estado actualizado con tipo_tarea clasificado.
    """
    tarea_descripcion = state.get("tarea_descripcion", "")
    print(f"🔍 Clasificando: {tarea_descripcion[:50]}...")
    
    # Primero intentar con keywords
    tipo_tarea = clasificar_por_keywords(tarea_descripcion)
    
    # Si es general y hay cliente disponible, intentar con LLM
    if tipo_tarea == "general" and client is not None:
        tipo_tarea = clasificar_con_llm(tarea_descripcion)
    
    state["tipo_tarea"] = tipo_tarea
    state["run_number"] = state.get("run_number", 1)  # Para tracking Run 1 vs Run 2
    
    print(f"✓ Tipo detectado: {tipo_tarea}")
    
    return state
