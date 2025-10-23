"""
Nodo 3: Ejecutar Tarea

Llama a la API de OpenAI con el modelo seleccionado y genera la respuesta.
"""

from typing import Dict, Any
from openai import OpenAI
import os
import time


def ejecutar_tarea(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ejecuta la tarea llamando a OpenAI con el modelo seleccionado.
    
    Args:
        state (dict): Estado con tarea_descripcion y modelo_a_usar.
        
    Returns:
        dict: Estado con resultado_tarea, respuesta_raw, tiempo_inicio y tiempo_fin.
    """
    tarea = state.get("tarea_descripcion", "")
    modelo = state.get("modelo_a_usar", "gpt-4o")
    
    print(f"🔄 Ejecutando con {modelo}...")
    
    # 🆕 Iniciar medición de tiempo
    tiempo_inicio = time.time()
    
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Eres un asistente útil y conciso."},
                {"role": "user", "content": tarea}
            ],
            temperature=0.7,
            max_tokens=500  # Limitamos para control de costos
        )
        
        # 🆕 Finalizar medición de tiempo
        tiempo_fin = time.time()
        
        resultado = response.choices[0].message.content
        state["resultado_tarea"] = resultado
        state["respuesta_raw"] = response  # Para extraer métricas después
        state["tiempo_inicio"] = tiempo_inicio
        state["tiempo_fin"] = tiempo_fin
        
        print(f"✅ Respuesta generada ({len(resultado)} caracteres)")
        
    except Exception as e:
        tiempo_fin = time.time()
        print(f"❌ Error ejecutando tarea: {e}")
        state["resultado_tarea"] = f"Error: {str(e)}"
        state["respuesta_raw"] = None
        state["tiempo_inicio"] = tiempo_inicio
        state["tiempo_fin"] = tiempo_fin
    
    return state
