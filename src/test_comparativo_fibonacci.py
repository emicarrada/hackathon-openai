"""
Test comparativo: GPT-3.5 vs GPT-4o para el problema de Fibonacci
"""
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import client
from typing import Dict
import json

def test_modelo(tarea: str, modelo: str) -> Dict:
    """Prueba un modelo específico y mide su rendimiento."""
    print(f"\n🔄 Probando {modelo}...")
    print("-" * 50)
    
    try:
        inicio = time.time()
        response = client.chat.completions.create(
            model=modelo,
            messages=[{
                "role": "user", 
                "content": tarea
            }],
            temperature=0.7
        )
        tiempo = time.time() - inicio
        
        resultado = response.choices[0].message.content
        print(f"\n✅ Respuesta de {modelo} (tiempo: {tiempo:.2f}s):")
        print(resultado)
        
        return {
            "modelo": modelo,
            "tiempo": tiempo,
            "respuesta": resultado,
            "exitoso": True
        }
    except Exception as e:
        print(f"❌ Error con {modelo}:")
        print(str(e))
        return {
            "modelo": modelo,
            "tiempo": 0,
            "respuesta": str(e),
            "exitoso": False
        }

def comparar_modelos():
    """Compara GPT-3.5 y GPT-4o en el problema de Fibonacci."""
    tarea = """Implementa tres versiones de la función Fibonacci en Python:
1. Recursiva simple
2. Con memoización
3. Iterativa

Para cada versión:
- Incluye tipos (type hints)
- Documentación completa
- Análisis de complejidad temporal y espacial
- Ejemplos de uso

Compara y explica por qué cada versión mejora la anterior."""

    print("\n🚀 COMPARACIÓN DE MODELOS: Fibonacci")
    print("=" * 50)
    
    # Test con GPT-3.5-turbo
    resultado_gpt3 = test_modelo(tarea, "gpt-3.5-turbo")
    
    # Test con GPT-4o
    resultado_gpt4o = test_modelo(tarea, "gpt-4o")
    
    print("\n📊 RESUMEN COMPARATIVO")
    print("=" * 50)
    
    if resultado_gpt3["exitoso"] and resultado_gpt4o["exitoso"]:
        print(f"\nTiempos de respuesta:")
        print(f"- GPT-3.5-turbo: {resultado_gpt3['tiempo']:.2f}s")
        print(f"- GPT-4o: {resultado_gpt4o['tiempo']:.2f}s")
        
        # Guardar resultados
        resultados = {
            "gpt3": resultado_gpt3,
            "gpt4o": resultado_gpt4o,
            "tarea": tarea
        }
        
        with open("resultados_comparacion.json", "w") as f:
            json.dump(resultados, f, indent=2)
        print("\n✅ Resultados guardados en resultados_comparacion.json")
    else:
        print("\n⚠️ No se pudieron comparar los modelos debido a errores")

if __name__ == "__main__":
    comparar_modelos()