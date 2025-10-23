"""
Tests para los prompts especializados y configuraciones de ejecución.
"""

import pytest
from src.nodos.ejecutar_tarea import PROMPTS_SISTEMA, CONFIGURACIONES_POR_TIPO, ejecutar_tarea

def test_prompts_completos():
    """Verifica que existan prompts para todos los tipos requeridos"""
    tipos_requeridos = {
        "resumen", "traduccion", "clasificacion", "extraccion", "analisis",
        "codigo", "creatividad", "qa", "comparacion", "general"
    }
    
    assert set(PROMPTS_SISTEMA.keys()) == tipos_requeridos
    
    # Verificar que cada prompt tenga contenido sustancial
    for tipo, prompt in PROMPTS_SISTEMA.items():
        assert len(prompt) >= 100, f"Prompt de {tipo} es muy corto"
        assert "objetivo" in prompt.lower(), f"Prompt de {tipo} debe definir objetivo"
        assert "método" in prompt.lower() or "formato" in prompt.lower(), \
            f"Prompt de {tipo} debe explicar método o formato"

def test_configuraciones_completas():
    """Verifica que existan configuraciones para todos los tipos"""
    assert set(CONFIGURACIONES_POR_TIPO.keys()) == set(PROMPTS_SISTEMA.keys())
    
    for tipo, config in CONFIGURACIONES_POR_TIPO.items():
        assert "temperature" in config, f"Falta temperature en config de {tipo}"
        assert "max_tokens" in config, f"Faltan max_tokens en config de {tipo}"
        assert 0 <= config["temperature"] <= 1, f"Temperature inválida en {tipo}"
        assert config["max_tokens"] > 0, f"max_tokens debe ser positivo en {tipo}"

def test_configuraciones_especificas():
    """Verifica valores específicos de configuración por tipo"""
    # Tipos que requieren alta precisión
    assert CONFIGURACIONES_POR_TIPO["codigo"]["temperature"] <= 0.3
    assert CONFIGURACIONES_POR_TIPO["traduccion"]["temperature"] <= 0.3
    
    # Tipos que requieren creatividad
    assert CONFIGURACIONES_POR_TIPO["creatividad"]["temperature"] >= 0.8
    
    # Tipos con necesidad de tokens extendidos
    assert CONFIGURACIONES_POR_TIPO["analisis"]["max_tokens"] >= 800
    assert CONFIGURACIONES_POR_TIPO["codigo"]["max_tokens"] >= 500

def test_ejecucion_parametros():
    """Verifica que se usen los parámetros correctos según el tipo"""
    tipos_prueba = {
        "creatividad": {"min_temp": 0.8},  # Alta creatividad
        "codigo": {"max_temp": 0.3},  # Alta precisión
        "resumen": {"max_tokens": 300},  # Respuestas concisas
        "analisis": {"min_tokens": 800}  # Respuestas extensas
    }
    
    for tipo, expectativas in tipos_prueba.items():
        config = CONFIGURACIONES_POR_TIPO[tipo]
        if "min_temp" in expectativas:
            assert config["temperature"] >= expectativas["min_temp"], \
                f"{tipo} debe tener temperature >= {expectativas['min_temp']}"
        if "max_temp" in expectativas:
            assert config["temperature"] <= expectativas["max_temp"], \
                f"{tipo} debe tener temperature <= {expectativas['max_temp']}"
        if "min_tokens" in expectativas:
            assert config["max_tokens"] >= expectativas["min_tokens"], \
                f"{tipo} debe tener max_tokens >= {expectativas['min_tokens']}"
        if "max_tokens" in expectativas:
            assert config["max_tokens"] <= expectativas["max_tokens"], \
                f"{tipo} debe tener max_tokens <= {expectativas['max_tokens']}"