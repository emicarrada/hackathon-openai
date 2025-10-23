"""
Tests para el módulo de evaluación de complejidad.
"""

import os
import sys
import pytest

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nodos.evaluar_complejidad import evaluar_complejidad

CASOS_PRUEBA = [
    # Casos de complejidad baja
    ("Hola", "baja"),
    ("¿Qué es Python?", "baja"),
    ("Dame un ejemplo básico", "baja"),
    
    # Casos de complejidad media
    ("Explica cómo funciona una computadora", "media"),
    ("¿Cuáles son las partes de un auto?", "media"),
    
    # Casos de complejidad alta
    ("Explica detalladamente el funcionamiento del quantum computing y sus aplicaciones en criptografía", "alta"),
    ("Compara y analiza las diferencias técnicas entre machine learning supervisado y no supervisado", "alta"),
    ("Implementa un algoritmo avanzado de optimización para resolver el problema del viajero", "alta")
]

def test_evaluacion_casos():
    """Prueba la evaluación de complejidad con varios casos."""
    for tarea, esperado in CASOS_PRUEBA:
        resultado = evaluar_complejidad(tarea)
        assert resultado["complejidad"] == esperado, \
            f'Para "{tarea}" se esperaba "{esperado}" pero se obtuvo "{resultado["complejidad"]}"'
        assert "modelo" in resultado
        assert "factores" in resultado
        assert all(k in resultado["factores"] for k in ["longitud", "keywords_alta", "keywords_baja", "patrones_complejos"])

def test_manejo_errores():
    """Prueba el manejo de errores con input inválido."""
    resultado = evaluar_complejidad(None)  # Debería manejar el error
    assert "error" in resultado
    assert resultado["complejidad"] == "desconocida"
    assert resultado["modelo"] == "gpt-3.5-turbo"

def test_seleccion_modelo():
    """Prueba que la selección del modelo sea correcta según la complejidad."""
    casos_modelo = [
        ("Tarea simple y básica", "gpt-3.5-turbo"),  # baja
        ("Explica cómo funciona Git", "gpt-4o-mini"),  # media
        ("Análisis técnico avanzado de sistemas complejos", "gpt-4o")  # alta
    ]
    
    for tarea, modelo_esperado in casos_modelo:
        resultado = evaluar_complejidad(tarea)
        assert resultado["modelo"] == modelo_esperado, \
            f'Para "{tarea}" se esperaba modelo "{modelo_esperado}" pero se obtuvo "{resultado["modelo"]}"'