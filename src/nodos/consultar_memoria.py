"""
Nodo 2: Consultar Memoria

Busca si existe una estrategia aprendida para el tipo de tarea.
"""

from typing import Dict, Any
from src.memoria import Memoria


def consultar_memoria(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Consulta la memoria estratégica para optimización.
    
    Args:
        state (dict): Estado con tipo_tarea.
        
    Returns:
        dict: Estado con modelo_a_usar y estrategia_encontrada (bool).
    """
    tipo_tarea = state.get("tipo_tarea", "general")
    
    # Cargar memoria
    memoria = Memoria()
    estrategia = memoria.consultar_estrategia(tipo_tarea)
    
    if estrategia:
        # ✅ Estrategia encontrada - usar modelo optimizado
        modelo = estrategia.get("modelo", "gpt-4o")
        state["modelo_a_usar"] = modelo
        state["estrategia_encontrada"] = True
        state["ruta"] = "optimizada"
        
        print(f"✅ Estrategia encontrada para '{tipo_tarea}': {modelo}")
        print(f"📊 Métricas históricas: {estrategia.get('tokens_promedio')} tokens, "
              f"{estrategia.get('latencia_promedio')}s latencia")
    else:
        # ❌ No hay estrategia - usar modelo default (caro)
        state["modelo_a_usar"] = "gpt-4o"  # Modelo caro por defecto
        state["estrategia_encontrada"] = False
        state["ruta"] = "default"
        
        print(f"⚠️  Sin estrategia para '{tipo_tarea}' - usando GPT-4o (default)")
    
    return state
