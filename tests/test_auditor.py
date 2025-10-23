"""
Tests para el módulo de auditoría y feedback.
"""

import pytest
from src.nodos.auditor_feedback import (
    generar_feedback_auditor,
    calcular_costo,
    validar_json_feedback,
    BENCHMARKS_POR_TIPO
)

def test_benchmarks_completos():
    """Verifica que todos los tipos tengan sus benchmarks completos"""
    tipos_requeridos = {
        "resumen", "traduccion", "clasificacion", "extraccion",
        "analisis", "codigo", "creatividad", "qa", "comparacion", "general"
    }
    
    assert set(BENCHMARKS_POR_TIPO.keys()) == tipos_requeridos
    
    for tipo, benchmark in BENCHMARKS_POR_TIPO.items():
        assert "modelo_optimo" in benchmark
        assert "tokens_esperados" in benchmark
        assert "razon" in benchmark
        assert isinstance(benchmark["tokens_esperados"], int)
        assert len(benchmark["razon"]) > 20  # Razón detallada

def test_calculo_costos():
    """Prueba el cálculo de costos para diferentes modelos"""
    casos_prueba = [
        ("gpt-4o", 1000, 0.0047),  # 1000 tokens * (0.7 * $2.50 + 0.3 * $10.00) / 1M
        ("gpt-3.5-turbo", 1000, 0.0009),  # 1000 tokens * (0.7 * $0.50 + 0.3 * $1.50) / 1M
        ("gpt-4o-mini", 1000, 0.0003),  # 1000 tokens * (0.7 * $0.15 + 0.3 * $0.60) / 1M
        ("modelo-desconocido", 1000, 0.0)  # Modelo no reconocido
    ]
    
    for modelo, tokens, costo_esperado in casos_prueba:
        costo = calcular_costo(modelo, tokens)
        assert abs(costo - costo_esperado) < 0.0001, \
            f"Para {modelo} con {tokens} tokens, se esperaba ${costo_esperado} pero se obtuvo ${costo}"

def test_validacion_json():
    """Prueba la validación de estructura JSON"""
    # JSON válido
    assert validar_json_feedback({
        "requiere_optimizacion": True,
        "analisis": "Test",
        "recomendacion": "gpt-3.5-turbo"
    })
    
    # JSON incompleto
    assert not validar_json_feedback({
        "requiere_optimizacion": True,
        "analisis": "Test"
    })
    
    # JSON con campos extra
    assert validar_json_feedback({
        "requiere_optimizacion": True,
        "analisis": "Test",
        "recomendacion": "gpt-3.5-turbo",
        "campo_extra": "valor"
    })

def test_feedback_modelo_barato():
    """Prueba que no se optimiza cuando ya usamos modelo barato"""
    state = {
        "tipo_tarea": "resumen",
        "metricas_ejecucion": {
            "modelo_usado": "gpt-3.5-turbo",
            "tokens_totales": 150
        }
    }
    
    resultado = generar_feedback_auditor(state)
    feedback = resultado["feedback_auditor"]
    
    assert not feedback["requiere_optimizacion"]
    assert "eficiente" in feedback["analisis"].lower()
    assert feedback["recomendacion"] == "gpt-3.5-turbo"

def test_feedback_tokens_excedidos():
    """Prueba detección de uso excesivo de tokens y diferencia de costos"""
    benchmark = BENCHMARKS_POR_TIPO["resumen"]
    tokens_excedidos = benchmark["tokens_esperados"] * 2.5  # 2.5x tokens esperados
    
    # Verificar que la diferencia de costos es significativa
    costo_actual = calcular_costo("gpt-4o", tokens_excedidos)
    costo_optimo = calcular_costo(benchmark["modelo_optimo"], benchmark["tokens_esperados"])
    diferencia = abs(costo_actual - costo_optimo) / costo_optimo * 100
    
    assert diferencia > 20, f"La diferencia de costo ({diferencia:.1f}%) debería ser mayor al 20%"
    
    # Verificar que se detecta el uso excesivo
    state = {
        "tipo_tarea": "resumen",
        "metricas_ejecucion": {
            "modelo_usado": "gpt-4o",
            "tokens_totales": int(tokens_excedidos)
        }
    }
    
    # Como hay exceso de tokens, debería dar feedback sin llamar a OpenAI
    resultado = generar_feedback_auditor(state)
    feedback = resultado.get("feedback_auditor", {})
    
    # En el caso de tokens excedidos, el feedback debería ser automático
    assert feedback.get("requiere_optimizacion", False), \
        "Debería requerir optimización por exceso de tokens"
    assert feedback.get("recomendacion") == benchmark["modelo_optimo"], \
        "Debería recomendar el modelo óptimo del benchmark"

def test_feedback_modelo_optimo():
    """Prueba que no optimiza cuando usamos modelo óptimo con tokens normales"""
    state = {
        "tipo_tarea": "codigo",  # código usa gpt-4o por defecto
        "metricas_ejecucion": {
            "modelo_usado": "gpt-4o",
            "tokens_totales": 400  # Dentro del rango esperado
        }
    }
    
    resultado = generar_feedback_auditor(state)
    feedback = resultado["feedback_auditor"]
    
    assert not feedback["requiere_optimizacion"]
    assert feedback["recomendacion"] == "gpt-4o"

def test_manejo_errores():
    """Prueba el manejo de estados inválidos"""
    casos_prueba = [
        # Sin tipo_tarea
        {"metricas_ejecucion": {"modelo_usado": "gpt-4o", "tokens_totales": 100}},
        # Sin modelo_usado
        {"tipo_tarea": "resumen", "metricas_ejecucion": {"tokens_totales": 100}},
        # Sin tokens
        {"tipo_tarea": "resumen", "metricas_ejecucion": {"modelo_usado": "gpt-4o"}},
        # Métricas vacías
        {"tipo_tarea": "resumen", "metricas_ejecucion": {}},
        # Sin métricas
        {"tipo_tarea": "resumen"},
        # Estado completamente vacío
        {}
    ]
    
    for state in casos_prueba:
        resultado = generar_feedback_auditor(state)
        assert "feedback_auditor" in resultado
        feedback = resultado["feedback_auditor"]
        assert not feedback["requiere_optimizacion"]  # Por defecto, no optimizar en caso de error
        assert isinstance(feedback["analisis"], str)
        assert isinstance(feedback["recomendacion"], str)

def test_zona_gris():
    """Prueba el manejo de la zona gris (diferencia < 20%)"""
    state = {
        "tipo_tarea": "qa",
        "metricas_ejecucion": {
            "modelo_usado": "gpt-4o",
            "tokens_totales": 420  # Muy cercano al benchmark
        }
    }
    
    resultado = generar_feedback_auditor(state)
    feedback = resultado["feedback_auditor"]
    
    # Si la diferencia de costo es < 20%, no debería sugerir optimización
    assert not feedback["requiere_optimizacion"]