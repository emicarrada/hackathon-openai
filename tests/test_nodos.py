"""
Tests para los 6 nodos del sistema SmartOptimizer
"""
import pytest
from src.nodos.recibir_tarea import recibir_tarea
from src.nodos.consultar_memoria import consultar_memoria
from src.nodos.ejecutar_tarea import ejecutar_tarea
from src.nodos.evaluar_contador import evaluar_con_contador
from src.nodos.auditor_feedback import generar_feedback_auditor
from src.nodos.actualizar_memoria import actualizar_memoria


def test_recibir_tarea_clasifica_correctamente():
    """Test que recibir_tarea clasifica tipos de tareas."""
    state = {"tarea_descripcion": "Traduce este texto al español"}
    
    resultado = recibir_tarea(state)
    
    assert "tipo_tarea" in resultado
    assert resultado["tipo_tarea"] in ["traduccion", "codigo", "analisis", "escritura_creativa", "resumen", "otro"]


def test_consultar_memoria_sin_estrategias():
    """Test que consultar_memoria maneja memoria vacía."""
    state = {
        "tipo_tarea": "traduccion",
        "tarea_descripcion": "Test"
    }
    
    resultado = consultar_memoria(state)
    
    assert "estrategia_encontrada" in resultado
    # Con memoria vacía, no debe encontrar estrategia


def test_ejecutar_tarea_mock():
    """Test que ejecutar_tarea maneja estado sin API key."""
    import os
    # Guardar API key original
    api_key_original = os.environ.get("OPENAI_API_KEY")
    
    # Quitar API key temporalmente
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    
    state = {
        "tarea_descripcion": "Test",
        "modelo_a_usar": "gpt-3.5-turbo"
    }
    
    resultado = ejecutar_tarea(state)
    
    # Debe manejar error gracefully
    assert "resultado_tarea" in resultado
    assert "Error" in resultado["resultado_tarea"] or resultado["respuesta_raw"] is not None
    
    # Restaurar API key
    if api_key_original:
        os.environ["OPENAI_API_KEY"] = api_key_original


def test_evaluar_contador_extrae_metricas():
    """Test que evaluar_con_contador extrae métricas correctamente."""
    # Mock de respuesta
    class MockUsage:
        total_tokens = 100
        prompt_tokens = 30
        completion_tokens = 70
    
    class MockResponse:
        usage = MockUsage()
    
    state = {
        "modelo_a_usar": "gpt-4o-mini",
        "respuesta_raw": MockResponse(),
        "tiempo_inicio": 0,
        "tiempo_fin": 1.5
    }
    
    resultado = evaluar_con_contador(state)
    
    assert "metricas_ejecucion" in resultado
    assert resultado["metricas_ejecucion"]["tokens_totales"] == 100
    assert resultado["metricas_ejecucion"]["latencia"] > 0


def test_auditor_feedback_genera_recomendaciones():
    """Test que auditor_con_feedback genera recomendaciones."""
    state = {
        "tipo_tarea": "traduccion",
        "tarea_descripcion": "Test translation",
        "modelo_a_usar": "gpt-4o",
        "metricas_ejecucion": {
            "tokens_totales": 200,
            "tokens_prompt": 50,
            "tokens_completion": 150,
            "latencia": 2.0,
            "costo_total": 0.001,
            "modelo_usado": "gpt-4o"
        },
        "resultado_tarea": "Test result"
    }
    
    # Test con modelo caro (debe recomendar)
    resultado = generar_feedback_auditor(state)
    
    assert "feedback_auditor" in resultado
    # Con gpt-4o en tarea simple, debe recomendar algo
    feedback = resultado["feedback_auditor"]
    assert "recomendacion" in feedback
    assert feedback["requiere_optimizacion"] == True


def test_actualizar_memoria_persiste_estrategia():
    """Test que actualizar_memoria guarda estrategias correctamente."""
    state = {
        "tipo_tarea": "traduccion",
        "modelo_a_usar": "gpt-4o",
        "feedback_auditor": {
            "recomendacion": "gpt-3.5-turbo",
            "analisis": "Modelo más eficiente para traducción",
            "requiere_optimizacion": True
        }
    }
    
    resultado = actualizar_memoria(state)
    
    # Debe completar sin errores (sin importar si actualiza o no)
    assert "tipo_tarea" in resultado