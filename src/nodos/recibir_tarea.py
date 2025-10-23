"""
Nodo 1: Recibir Tarea

Punto de entrada del sistema. Recibe y clasifica la tarea del usuario.
"""

from typing import Dict, Any


def recibir_tarea(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Nodo inicial que recibe la tarea y la clasifica.
    
    Args:
        state (dict): Estado del grafo con la tarea del usuario.
        
    Returns:
        dict: Estado actualizado con tipo_tarea clasificado.
    """
    tarea_descripcion = state.get("tarea_descripcion", "")
    
    # Clasificación simple por palabras clave
    texto = tarea_descripcion.lower()
    
    if any(palabra in texto for palabra in ["resume", "resumen", "sintetiza"]):
        tipo_tarea = "resumen"
    elif any(palabra in texto for palabra in ["traduce", "traducir", "translation"]):
        tipo_tarea = "traduccion"
    elif any(palabra in texto for palabra in ["clasifica", "categoriza", "clasificar"]):
        tipo_tarea = "clasificacion"
    elif any(palabra in texto for palabra in ["extrae", "extraer", "obtener datos"]):
        tipo_tarea = "extraccion"
    else:
        tipo_tarea = "general"
    
    state["tipo_tarea"] = tipo_tarea
    state["run_number"] = state.get("run_number", 1)  # Para tracking Run 1 vs Run 2
    
    print(f"📥 Tarea recibida: '{tarea_descripcion[:50]}...'")
    print(f"🏷️  Tipo detectado: {tipo_tarea}")
    
    return state
