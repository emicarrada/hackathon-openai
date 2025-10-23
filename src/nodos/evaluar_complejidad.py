"""
Nodo 1: Evaluación Contextual

Este nodo evalúa la complejidad de la tarea para seleccionar el modelo LLM más eficiente.
La complejidad se determina basándose en:
- Longitud del texto
- Palabras clave que indican complejidad
- Patrones de la tarea
"""

from typing import Dict, Any, List
import re

# Constantes para configuración
UMBRAL_LONGITUD_ALTA = 150  # Bajado de 200 para ser más sensible
UMBRAL_LONGITUD_BAJA = 30   # Bajado de 50 para ser más preciso

KEYWORDS_ALTA = [
    "complejo", "avanzado", "técnico", "matemático",
    "análisis", "detallado", "profundo", "explicar",
    "comparar", "evaluar", "diseñar", "implementar",
    "optimizar", "quantum", "machine learning", "algoritmo",
    "arquitectura", "sistema", "framework", "metodología",
    "criptografía", "funcionamiento", "detalladamente"
]

KEYWORDS_BAJA = [
    "simple", "básico", "fácil", "ayuda",
    "qué es", "ejemplo", "definir", "hola",
    "gracias", "por favor", "lista", "menciona"
]

# Palabras que indican complejidad media
KEYWORDS_MEDIA = [
    "cómo", "funciona", "describir", "explicar",
    "cuál es", "por qué", "cuando", "donde"
]

def evaluar_complejidad(tarea: str) -> Dict[str, Any]:
    """
    Evalúa la complejidad de una tarea basada en análisis de texto.

    Args:
        tarea (str): Descripción de la tarea del usuario.

    Returns:
        Dict[str, Any]: Información de complejidad y modelo recomendado.
            {
                "complejidad": "baja"|"media"|"alta",
                "modelo": "gpt-3.5-turbo"|"gpt-4o-mini"|"gpt-4o",
                "factores": {
                    "longitud": int,
                    "keywords_alta": int,
                    "keywords_baja": int,
                    "patrones_complejos": int
                }
            }
    """
    try:
        # Normalizar texto
        texto = tarea.lower().strip()
        
        # 1. Análisis de longitud
        longitud = len(texto)
        
        # 2. Búsqueda de keywords
        conteo_alta = sum(1 for kw in KEYWORDS_ALTA if kw in texto)
        conteo_baja = sum(1 for kw in KEYWORDS_BAJA if kw in texto)
        
        # 3. Análisis de patrones complejos
        patrones_complejos = 0
        if re.search(r'comparar?|diferencias?|versus|vs\.?', texto):
            patrones_complejos += 1
        if re.search(r'por qué|explica|analiza', texto):
            patrones_complejos += 1
        if re.search(r'paso a paso|metodología|proceso', texto):
            patrones_complejos += 1
        
        # 4. Determinar complejidad
        # Contar palabras de complejidad media
        conteo_media = sum(1 for kw in KEYWORDS_MEDIA if kw in texto)
        
        # Sistema de puntos para determinar complejidad
        puntos = 0
        puntos += 3 if longitud > UMBRAL_LONGITUD_ALTA else (1 if longitud > UMBRAL_LONGITUD_BAJA else 0)
        puntos += conteo_alta * 2  # Keywords de alta valen más
        puntos -= conteo_baja * 2  # Keywords de baja restan
        puntos += patrones_complejos
        puntos += conteo_media
        
        # La lógica más ajustada para distinguir entre media y alta
        if (conteo_alta > 1 and patrones_complejos >= 1) or "quantum" in texto or "criptografía" in texto:
            complejidad = "alta"
            modelo = "gpt-4o"  # Actualizado de gpt-4
        elif conteo_baja > 1 or (puntos <= 0 and longitud < UMBRAL_LONGITUD_BAJA):
            complejidad = "baja"
            modelo = "gpt-3.5-turbo"
        else:
            complejidad = "media"
            modelo = "gpt-4o-mini"  # Actualizado de gpt-3.5-turbo para diferenciar de baja
        
        # 5. Retornar resultado estructurado
        return {
            "complejidad": complejidad,
            "modelo": modelo,
            "factores": {
                "longitud": longitud,
                "keywords_alta": conteo_alta,
                "keywords_baja": conteo_baja,
                "patrones_complejos": patrones_complejos
            }
        }
    except Exception as e:
        return {
            "error": str(e),
            "complejidad": "desconocida",
            "modelo": "gpt-3.5-turbo"  # Por defecto el modelo más económico
        }