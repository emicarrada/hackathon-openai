"""
Nodo 6: Actualizar Memoria

Guarda la estrategia aprendida en estrategias.json para futuras optimizaciones.
"""

from typing import Dict, Any
from src.memoria import Memoria


def actualizar_memoria(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Actualiza la memoria con la estrategia aprendida.
    
    Args:
        state (dict): Estado con feedback_auditor, tipo_tarea, metricas.
        
    Returns:
        dict: Estado sin cambios (solo efecto secundario en archivo).
    """
    feedback = state.get("feedback_auditor", {})
    requiere_opt = feedback.get("requiere_optimizacion", False)
    
    if not requiere_opt:
        print("⏭️  Sin optimización necesaria - memoria no actualizada")
        return state
    
    tipo_tarea = state.get("tipo_tarea", "general")
    modelo_recomendado = feedback.get("recomendacion", "gpt-4o-mini")
    metricas = state.get("metricas_ejecucion", {})
    
    tokens = metricas.get("tokens_totales", 0)
    latencia = metricas.get("latencia", 0.0)
    
    # Actualizar memoria
    memoria = Memoria()
    memoria.agregar_estrategia(
        tipo_tarea=tipo_tarea,
        modelo=modelo_recomendado,
        tokens=tokens,
        latencia=latencia
    )
    
    print(f"💾 Memoria actualizada:")
    print(f"   - Tipo tarea: {tipo_tarea}")
    print(f"   - Modelo nuevo: {modelo_recomendado}")
    print(f"   - Estrategia guardada en estrategias.json")
    
    state["memoria_actualizada"] = True
    
    return state
