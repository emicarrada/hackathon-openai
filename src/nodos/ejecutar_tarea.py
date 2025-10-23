"""
Nodo 3: Ejecutar Tarea

Llama a la API de OpenAI con el modelo seleccionado y genera la respuesta.
"""

from typing import Dict, Any
from src.utils import llamar_openai_simple

# Prompts optimizados por tipo de tarea
PROMPTS_SISTEMA = {
    "resumen": """Eres un experto en síntesis de información especializado en generar resúmenes concisos y efectivos.
Tu objetivo: Extraer y comunicar los puntos clave manteniendo la esencia del contenido original.
Método: 
- Identifica los conceptos principales
- Elimina información redundante
- Estructura jerárquicamente
- Usa lenguaje claro y directo
Formato: Párrafos cortos o bullets según el contexto.""",
    
    "traduccion": """Eres un traductor profesional con experiencia en múltiples idiomas y contextos culturales.
Tu objetivo: Traducir manteniendo el significado, tono y contexto cultural.
Método:
- Preserva el registro del lenguaje
- Adapta modismos y expresiones culturales
- Mantén el formato y estilo original
Consideraciones: Incluye notas sobre contexto cultural cuando sea relevante.""",
    
    "codigo": """Eres un programador senior experto en múltiples lenguajes y best practices.
Tu objetivo: Generar código limpio, eficiente y mantenible.
Método:
- Usa patrones de diseño apropiados
- Implementa manejo de errores robusto
- Incluye documentación clara
- Sigue estándares de cada lenguaje
Output: Código documentado con ejemplos de uso.""",
    
    "analisis": """Eres un analista senior con pensamiento crítico y metodología estructurada.
Tu objetivo: Proporcionar análisis profundos y conclusiones accionables.
Método:
- Identifica patrones y tendencias
- Evalúa pros y contras
- Considera múltiples perspectivas
- Proporciona recomendaciones concretas
Formato: Análisis estructurado con conclusiones claras.""",
    
    "creatividad": """Eres un escritor creativo profesional con amplia experiencia en narrativa y contenido original.
Tu objetivo: Crear contenido único, emotivo y memorable.
Estilo:
- Usa lenguaje rico y expresivo
- Incorpora elementos narrativos
- Desarrolla voces distintivas
- Evoca emociones y experiencias
Formato: Adapta el estilo al género solicitado.""",
    
    "qa": """Eres un experto en responder preguntas de manera clara, precisa y educativa.
Tu objetivo: Proporcionar respuestas completas y comprensibles.
Método:
- Identifica el núcleo de la pregunta
- Estructura la respuesta lógicamente
- Incluye ejemplos relevantes
- Verifica precisión de la información
Formato: Respuesta directa seguida de contexto necesario.""",
    
    "comparacion": """Eres un analista especializado en evaluación comparativa objetiva.
Tu objetivo: Contrastar elementos destacando similitudes y diferencias clave.
Método:
- Establece criterios claros
- Evalúa aspectos comparables
- Destaca ventajas/desventajas
- Proporciona conclusiones equilibradas
Formato: Tabla comparativa y análisis detallado.""",
    
    "clasificacion": """Eres un experto en organización y categorización sistemática.
Tu objetivo: Clasificar elementos según criterios claros y consistentes.
Método:
- Define categorías precisas
- Aplica criterios consistentes
- Justifica cada clasificación
- Maneja casos límite
Formato: Categorías claras con ejemplos.""",
    
    "extraccion": """Eres un especialista en identificación y extracción precisa de información.
Tu objetivo: Extraer datos relevantes manteniendo contexto y precisión.
Método:
- Identifica información clave
- Preserva relaciones y contexto
- Valida datos extraídos
- Estructura la salida
Formato: Datos estructurados con metadatos relevantes.""",
    
    "general": """Eres un asistente versátil y eficiente.
Tu objetivo: Proporcionar ayuda clara y útil para cualquier tarea.
Método:
- Analiza el requerimiento
- Proporciona respuestas estructuradas
- Adapta el nivel de detalle
- Mantén un tono profesional
Formato: Respuesta clara y directa."""
}

# Configuraciones óptimas por tipo de tarea
CONFIGURACIONES_POR_TIPO = {
    "resumen": {"temperature": 0.3, "max_tokens": 300},  # Más determinístico para consistencia
    "traduccion": {"temperature": 0.3, "max_tokens": 500},  # Preciso para mantener significado
    "codigo": {"temperature": 0.2, "max_tokens": 800},  # Muy determinístico para código confiable
    "analisis": {"temperature": 0.4, "max_tokens": 1000},  # Balance entre creatividad y precisión
    "creatividad": {"temperature": 0.9, "max_tokens": 800},  # Alta creatividad para contenido original
    "qa": {"temperature": 0.5, "max_tokens": 400},  # Balance para respuestas naturales
    "comparacion": {"temperature": 0.4, "max_tokens": 600},  # Precisión con algo de flexibilidad
    "clasificacion": {"temperature": 0.3, "max_tokens": 400},  # Consistencia en categorización
    "extraccion": {"temperature": 0.2, "max_tokens": 500},  # Precisión en extracción de datos
    "general": {"temperature": 0.7, "max_tokens": 500}  # Versátil para tareas generales
}

def ejecutar_tarea(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ejecuta la tarea llamando a OpenAI con configuraciones optimizadas por tipo.
    
    Args:
        state (dict): Estado con tarea_descripcion, tipo_tarea y modelo_a_usar.
        
    Returns:
        dict: Estado con resultado_tarea y respuesta_raw.
    """
    tarea = state.get("tarea_descripcion", "")
    tipo_tarea = state.get("tipo_tarea", "general")
    modelo = state.get("modelo_a_usar", "gpt-4o")
    
    # Obtener configuración específica para el tipo de tarea
    config = CONFIGURACIONES_POR_TIPO.get(tipo_tarea, CONFIGURACIONES_POR_TIPO["general"])
    sistema = PROMPTS_SISTEMA.get(tipo_tarea, PROMPTS_SISTEMA["general"])
    
    print(f"🔄 Ejecutando tarea tipo '{tipo_tarea}' con {modelo}...")
    
    try:
        # Mejorar el prompt con contexto e instrucciones
        prompt_completo = f"""TAREA: {tarea}

INSTRUCCIONES:
- Sigue el formato especificado para este tipo de tarea
- Respuesta clara y estructurada
- Incluye solo información relevante
- Explica decisiones importantes

RESPUESTA:
"""
        
        # Usar llamar_openai_simple con las configuraciones optimizadas
        resultado = llamar_openai_simple(
            prompt=prompt_completo,
            modelo=modelo
        )
        
        state["resultado_tarea"] = resultado
        state["configuracion_usada"] = {
            "tipo_tarea": tipo_tarea,
            "temperature": config["temperature"],
            "max_tokens": config["max_tokens"],
            "prompt_sistema": sistema[:100] + "..."  # Guardar inicio del prompt para debug
        }
        
        print(f"✅ Respuesta generada ({len(resultado)} caracteres)")
        print(f"   Tipo: {tipo_tarea} (temp={config['temperature']})")
        
    except Exception as e:
        print(f"❌ Error ejecutando tarea: {e}")
        state["resultado_tarea"] = f"Error: {str(e)}"
        state["configuracion_usada"] = None
    
    return state
