"""
Tests para el nodo evaluar_contador (extracción de métricas)
"""
import pytest
from src.nodos.evaluar_contador import evaluar_con_contador


def test_evaluar_contador_sin_respuesta():
    """Test que evaluar_contador maneja estado sin respuesta_raw."""
    state = {
        "modelo_a_usar": "gpt-4o",
        "respuesta_raw": None
    }
    
    resultado = evaluar_con_contador(state)
    
    assert "metricas_ejecucion" in resultado
    assert resultado["metricas_ejecucion"]["tokens_totales"] == 0
    assert resultado["metricas_ejecucion"]["modelo_usado"] == "gpt-4o"


def test_evaluar_contador_con_respuesta_mock():
    """Test que evaluar_contador extrae métricas correctamente."""
    # Mock de respuesta OpenAI
    class MockUsage:
        total_tokens = 150
        prompt_tokens = 50
        completion_tokens = 100
    
    class MockResponse:
        usage = MockUsage()
    
    state = {
        "modelo_a_usar": "gpt-3.5-turbo",
        "respuesta_raw": MockResponse(),
        "tiempo_inicio": 1.0,
        "tiempo_fin": 2.5
    }
    
    resultado = evaluar_con_contador(state)
    
    assert "metricas_ejecucion" in resultado
    metricas = resultado["metricas_ejecucion"]
    
    assert metricas["tokens_totales"] == 150
    assert metricas["tokens_prompt"] == 50
    assert metricas["tokens_completion"] == 100
    assert metricas["latencia"] == 1.5  # 2.5 - 1.0
    assert metricas["costo_total"] > 0  # Debe calcular costo
    assert metricas["modelo_usado"] == "gpt-3.5-turbo"


def test_evaluar_contador_calcula_costos():
    """Test que evaluar_contador calcula costos correctos por modelo."""
    class MockUsage:
        total_tokens = 1000
        prompt_tokens = 500
        completion_tokens = 500
    
    class MockResponse:
        usage = MockUsage()
    
    # Test con gpt-4o (más caro)
    state_gpt4 = {
        "modelo_a_usar": "gpt-4o",
        "respuesta_raw": MockResponse(),
        "tiempo_inicio": 0,
        "tiempo_fin": 1
    }
    
    resultado_gpt4 = evaluar_con_contador(state_gpt4)
    costo_gpt4 = resultado_gpt4["metricas_ejecucion"]["costo_total"]
    
    # Test con gpt-3.5-turbo (más barato)
    state_gpt35 = {
        "modelo_a_usar": "gpt-3.5-turbo",
        "respuesta_raw": MockResponse(),
        "tiempo_inicio": 0,
        "tiempo_fin": 1
    }
    
    resultado_gpt35 = evaluar_con_contador(state_gpt35)
    costo_gpt35 = resultado_gpt35["metricas_ejecucion"]["costo_total"]
    
    # gpt-4o debe ser más caro que gpt-3.5-turbo
    assert costo_gpt4 > costo_gpt35