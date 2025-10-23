"""
Tests para la clasificación de tareas y prompts.
"""

import pytest
from src.nodos.recibir_tarea import recibir_tarea, TIPOS_TAREA

def test_clasificacion_extendida():
    """Verifica que los nuevos tipos de tarea funcionan correctamente"""
    casos_prueba = [
        ("Escribe un poema sobre IA", "creatividad"),
        ("Genera un script Python que ordene una lista", "codigo"),
        ("Analiza el impacto de la IA en empleos", "analisis"),
        ("Compara Python vs JavaScript", "comparacion"),
        ("¿Qué es el aprendizaje profundo?", "qa"),
        ("Resume este artículo sobre IA", "resumen"),
        ("Traduce al inglés: Hola mundo", "traduccion"),
        ("Clasifica estos emails por prioridad", "clasificacion"),
        ("Extrae los números de este texto", "extraccion"),
    ]
    
    for tarea, tipo_esperado in casos_prueba:
        state = {"tarea_descripcion": tarea}
        resultado = recibir_tarea(state)
        assert resultado["tipo_tarea"] == tipo_esperado, \
            f"Para '{tarea}' se esperaba '{tipo_esperado}' pero se obtuvo '{resultado['tipo_tarea']}'"

def test_keywords_por_tipo():
    """Verifica que cada tipo tiene suficientes keywords"""
    for tipo, keywords in TIPOS_TAREA.items():
        if tipo != "general":  # general es el fallback, no necesita keywords
            assert len(keywords) >= 5, \
                f"El tipo '{tipo}' debe tener al menos 5 keywords, tiene {len(keywords)}"

def test_clasificacion_fallback():
    """Verifica que tareas sin keywords claras van a general"""
    state = {"tarea_descripcion": "xyz 123"}
    resultado = recibir_tarea(state)
    assert resultado["tipo_tarea"] == "general"

def test_tipos_tarea_completos():
    """Verifica que están implementados todos los tipos requeridos"""
    tipos_requeridos = {
        "resumen", "traduccion", "clasificacion", "extraccion",
        "analisis", "codigo", "creatividad", "qa", "comparacion", "general"
    }
    
    tipos_implementados = set(TIPOS_TAREA.keys())
    
    assert tipos_implementados == tipos_requeridos, \
        f"Faltan implementar los tipos: {tipos_requeridos - tipos_implementados}"