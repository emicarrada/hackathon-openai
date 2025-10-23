"""
Prompts base para el sistema de generación y refinamiento.
"""

PROMPT_INICIAL = """
Tarea: {tarea}

Instrucciones:
1. Lee y analiza cuidadosamente la tarea
2. Genera una respuesta clara y concisa
3. Asegúrate de cubrir todos los aspectos requeridos

Respuesta:
"""

PROMPT_REFINAMIENTO = """
Analiza la siguiente respuesta a la tarea: "{tarea}"

Respuesta actual:
{respuesta_inicial}

Instrucciones para refinamiento:
1. Identifica áreas de mejora en la respuesta
2. Sugiere cambios específicos
3. Proporciona una versión mejorada

Formato de respuesta:
ANÁLISIS:
[Análisis de la respuesta actual]

MEJORAS SUGERIDAS:
- [Mejora 1]
- [Mejora 2]
...

VERSIÓN REFINADA:
[Nueva versión mejorada de la respuesta]
"""

PROMPT_VALIDACION = """
Evalúa la calidad de la respuesta refinada:

Tarea original: {tarea}
Respuesta refinada: {respuesta_refinada}

Criterios de evaluación:
1. Precisión y exactitud
2. Claridad y coherencia
3. Completitud
4. Relevancia

Proporciona una evaluación detallada y una puntuación del 1 al 10.
"""