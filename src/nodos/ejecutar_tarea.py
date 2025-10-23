"""
Nodo 3: Ejecutar Tarea

Llama a la API de OpenAI con el modelo seleccionado y genera la respuesta.
"""

from typing import Dict, Any
from openai import OpenAI
import os


def ejecutar_tarea(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ejecuta la tarea llamando a OpenAI con el modelo seleccionado.
    
    Args:
        state (dict): Estado con tarea_descripcion y modelo_a_usar.
        
    Returns:
        dict: Estado con resultado_tarea y respuesta_raw.
    """
    tarea = state.get("tarea_descripcion", "")
    modelo = state.get("modelo_a_usar", "gpt-4o")
    
    print(f"🔄 Ejecutando con {modelo}...")
    
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
        
        resultado = response.choices[0].message.content
        state["resultado_tarea"] = resultado
        state["respuesta_raw"] = response  # Para extraer métricas después
        
        print(f"✅ Respuesta generada ({len(resultado)} caracteres)")
        
    except Exception as e:
        print(f"❌ Error ejecutando tarea: {e}")
        state["resultado_tarea"] = f"Error: {str(e)}"
        state["respuesta_raw"] = None
    
    return state
