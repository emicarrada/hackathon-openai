"""
Nodos del sistema Smart Optimizer - Arquitectura 6 Nodos con Automejora

Sistema completo de aprendizaje:
1. recibir_tarea - Clasificación de tipo de tarea
2. consultar_memoria - Búsqueda de estrategias aprendidas
3. ejecutar_tarea - Ejecución con modelo seleccionado
4. evaluar_contador - Captura de métricas (tokens, latencia)
5. auditor_feedback - Análisis de eficiencia con LLM-Crítico
6. actualizar_memoria - Persistencia de estrategias optimizadas
"""

from .recibir_tarea import recibir_tarea
from .consultar_memoria import consultar_memoria
from .ejecutar_tarea import ejecutar_tarea
from .evaluar_contador import evaluar_con_contador
from .auditor_feedback import generar_feedback_auditor
from .actualizar_memoria import actualizar_memoria

__all__ = [
    'recibir_tarea',
    'consultar_memoria',
    'ejecutar_tarea',
    'evaluar_con_contador',
    'generar_feedback_auditor',
    'actualizar_memoria'
]
