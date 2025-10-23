"""
Tests para el sistema de clasificación de tareas.
"""

import pytest
from src.nodos.recibir_tarea import recibir_tarea, clasificar_por_keywords, TIPOS_TAREA, PRIORIDAD_TIPOS

def test_clasificacion_por_keywords():
    """Prueba la clasificación basada en keywords"""
    casos_prueba = [
        ("Escribe un poema sobre IA", "creatividad"),
        ("Genera un script Python", "codigo"),
        ("Analiza el impacto de la IA", "analisis"),
        ("Compara Python vs JavaScript", "comparacion"),
        ("¿Qué es machine learning?", "qa"),
        ("Resume este artículo", "resumen"),
        ("Traduce al inglés", "traduccion"),
        ("Clasifica estos emails", "clasificacion"),
        ("Extrae los datos", "extraccion")
    ]
    
    for tarea, tipo_esperado in casos_prueba:
        tipo_detectado = clasificar_por_keywords(tarea)
        assert tipo_detectado == tipo_esperado, \
            f"Para '{tarea}' se esperaba '{tipo_esperado}' pero se obtuvo '{tipo_detectado}'"

def test_keywords_suficientes():
    """Verifica que cada tipo tenga suficientes keywords"""
    min_keywords = 5
    for tipo, keywords in TIPOS_TAREA.items():
        if tipo != "general":  # general no necesita keywords
            assert len(keywords) >= min_keywords, \
                f"El tipo '{tipo}' debe tener al menos {min_keywords} keywords, tiene {len(keywords)}"

def test_recibir_tarea_estado():
    """Prueba que la función principal actualiza el estado correctamente"""
    state = {"tarea_descripcion": "Escribe un poema"}
    resultado = recibir_tarea(state)
    
    # Verificar campos requeridos
    assert "tipo_tarea" in resultado
    assert "run_number" in resultado
    assert resultado["tipo_tarea"] == "creatividad"

def test_tarea_desconocida():
    """Prueba el manejo de tareas sin keywords conocidas"""
    state = {"tarea_descripcion": "xyz 123"}
    resultado = recibir_tarea(state)
    assert resultado["tipo_tarea"] == "general"

def test_tipos_completos():
    """Verifica que estén implementados todos los tipos requeridos"""
    tipos_requeridos = {
        "resumen", "traduccion", "clasificacion", "extraccion",
        "analisis", "codigo", "creatividad", "qa", "comparacion", "general"
    }
    assert set(TIPOS_TAREA.keys()) == tipos_requeridos

def test_prioridad_tipos():
    """Verifica que la prioridad de tipos esté correctamente definida"""
    # Todos los tipos (excepto general) deben estar en la lista de prioridad
    tipos_sin_general = set(TIPOS_TAREA.keys()) - {"general"}
    tipos_en_prioridad = set(PRIORIDAD_TIPOS)
    assert tipos_sin_general == tipos_en_prioridad, \
        "Todos los tipos (excepto 'general') deben estar en PRIORIDAD_TIPOS"

def test_clasificacion_multiple():
    """Prueba la clasificación cuando hay múltiples coincidencias"""
    # Casos donde hay overlap de keywords pero debe ganar el de mayor prioridad
    casos_prueba = [
        ("Escribe código creativo para generar arte ascii", "codigo"),  # código > creatividad
        ("Ayuda a debuggear este código que no funciona", "debug"),  # debug > código
        ("Analiza y compara estos dos algoritmos", "analisis"),  # análisis > comparación
        ("Extrae y resume la información del texto", "extraccion"),  # extracción > resumen
    ]
    
    for tarea, tipo_esperado in casos_prueba:
        tipo_detectado = clasificar_por_keywords(tarea)
        assert tipo_detectado == tipo_esperado, \
            f"Para '{tarea}' se esperaba '{tipo_esperado}' pero se obtuvo '{tipo_detectado}'"