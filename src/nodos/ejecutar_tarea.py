"""
Nodo 3: Ejecutar Tarea

Llama a la API de OpenAI con el modelo seleccionado y genera la respuesta.

MEJORAS:
- Detección automática de max_tokens según tipo de tarea
- Manejo robusto de errores API (rate limit, auth, timeout, etc.)
"""

from typing import Dict, Any
from openai import OpenAI
import os
import time
import re


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
    
    # 🆕 DETECCIÓN INTELIGENTE DE max_tokens
    max_tokens = 500  # Default
    
    # Detectar "X palabras"
    palabras_match = re.search(r'(\d+)\s*palabras?', tarea.lower())
    if palabras_match:
        palabras_req = int(palabras_match.group(1))
        max_tokens = min(int(palabras_req * 1.5 * 1.2), 4096)
        print(f"🎯 Detectado: {palabras_req} palabras → {max_tokens} tokens")
    
    # Tareas largas
    elif any(kw in tarea.lower() for kw in ['ensayo', 'artículo', 'detallado', 'completo', 'extenso', 'profundidad']):
        max_tokens = 2500
        print(f"📝 Tarea extensa → {max_tokens} tokens")
    
    # Código extenso
    elif any(kw in tarea.lower() for kw in ['script completo', 'código completo', 'implementación completa', 'programa']):
        max_tokens = 2000
        print(f"💻 Código extenso → {max_tokens} tokens")
    
    # Listas largas
    elif re.search(r'(\d+)\s*(ideas|nombres|opciones|ejemplos)', tarea.lower()):
        cantidad_match = re.search(r'(\d+)', tarea.lower())
        if cantidad_match:
            cantidad = int(cantidad_match.group(1))
            max_tokens = min(cantidad * 15, 2000)
            print(f"📋 Lista de {cantidad} items → {max_tokens} tokens")
    
    # Tareas cortas
    elif any(kw in tarea.lower() for kw in ['traduce', 'resume en', 'breve', 'brevemente', 'en pocas palabras']):
        max_tokens = 300
        print(f"⚡ Tarea corta → {max_tokens} tokens")
    
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
            max_tokens=max_tokens  # 🆕 Dinámico
        )
        
        tiempo_fin = time.time()
        
        resultado = response.choices[0].message.content
        state["resultado_tarea"] = resultado
        state["respuesta_raw"] = response
        state["tiempo_inicio"] = tiempo_inicio
        state["tiempo_fin"] = tiempo_fin
        state["max_tokens_usado"] = max_tokens
        
        print(f"✅ Respuesta generada ({len(resultado)} caracteres)")
        
    # 🆕 MANEJO ROBUSTO DE ERRORES
    except Exception as e:
        tiempo_fin = time.time()
        error_msg = str(e).lower()
        
        # Rate limit
        if "rate_limit" in error_msg or "rate limit" in error_msg:
            print(f"⚠️  Rate limit excedido")
            state["resultado_tarea"] = "⚠️ API rate limit excedido. Intenta de nuevo en 60 segundos."
            state["error"] = "rate_limit"
        
        # Auth error
        elif "authentication" in error_msg or "api_key" in error_msg or "invalid" in error_msg:
            print(f"❌ Error de autenticación")
            state["resultado_tarea"] = "❌ Error de autenticación. Verifica tu OPENAI_API_KEY."
            state["error"] = "authentication"
        
        # Timeout
        elif "timeout" in error_msg or "timed out" in error_msg:
            print(f"⏱️  Timeout")
            state["resultado_tarea"] = "⏱️ Timeout: La API tardó demasiado. Intenta con tarea más corta."
            state["error"] = "timeout"
        
        # Context length exceeded
        elif "context_length" in error_msg or "maximum context" in error_msg or "too long" in error_msg:
            print(f"📏 Contexto excedido")
            state["resultado_tarea"] = f"📏 Error: Tarea excede límite de contexto de {modelo}. Intenta más corta."
            state["error"] = "context_length"
        
        # Modelo no encontrado
        elif "model" in error_msg and ("not found" in error_msg or "does not exist" in error_msg):
            print(f"🤖 Modelo '{modelo}' no encontrado - Reintentando con GPT-4o...")
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Eres un asistente útil y conciso."},
                        {"role": "user", "content": tarea}
                    ],
                    temperature=0.7,
                    max_tokens=max_tokens
                )
                tiempo_fin = time.time()
                state["resultado_tarea"] = response.choices[0].message.content
                state["respuesta_raw"] = response
                state["tiempo_inicio"] = tiempo_inicio
                state["tiempo_fin"] = tiempo_fin
                state["modelo_a_usar"] = "gpt-4o"  # Override
                print(f"✅ Respuesta con fallback GPT-4o")
                return state
            except:
                state["resultado_tarea"] = f"❌ Modelo '{modelo}' no disponible y fallback falló."
                state["error"] = "invalid_model"
        
        # Error genérico
        else:
            print(f"❌ Error: {type(e).__name__}")
            state["resultado_tarea"] = f"❌ Error inesperado: {str(e)[:200]}"
            state["error"] = "unknown"
        
        state["respuesta_raw"] = None
        state["tiempo_inicio"] = tiempo_inicio
        state["tiempo_fin"] = tiempo_fin
    
    return state
