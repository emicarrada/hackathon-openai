import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente de OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def test_modelo(modelo, prompt):
    """Ejecuta un test con el modelo especificado y mide el tiempo de respuesta"""
    start_time = time.time()
    try:
        response = client.chat.completions.create(
            model=modelo,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        end_time = time.time()
        return {
            "respuesta": response.choices[0].message.content,
            "tiempo": end_time - start_time
        }
    except Exception as e:
        print(f"Error con {modelo}: {str(e)}")
        return None

# Prompts de prueba
PROMPT_SIMPLE = """
Implementa una función en Python que calcule el factorial de un número n.
Requisitos:
1. Debe manejar casos de error (números negativos)
2. Debe ser eficiente
3. Debe incluir docstring y comentarios
4. Debe incluir tests básicos
"""

PROMPT_COMPLEJO = """
Implementa un algoritmo de ordenamiento híbrido en Python llamado QuickMergeSort que combine 
características de Quicksort y Mergesort de la siguiente manera:

1. El algoritmo debe usar la estrategia de división de Quicksort
2. Para sublistas menores a un umbral, debe usar Mergesort
3. Debe incluir optimizaciones como:
   - Selección de pivote mediante mediana de tres
   - Inserción directa para sublistas muy pequeñas
   - Manejo de duplicados eficiente
4. Debe incluir análisis de complejidad
5. Debe tener manejo de casos especiales
6. Implementa tests que comparen su rendimiento con sort() nativo de Python

La implementación debe ser detallada, eficiente y bien documentada.
"""

def main():
    # Modelos a probar
    modelos = ["gpt-3.5-turbo-1106", "gpt-4o"]
    
    print("\n=== PRUEBA CASO SIMPLE: FACTORIAL ===")
    for modelo in modelos:
        print(f"\nProbando {modelo}...")
        resultado = test_modelo(modelo, PROMPT_SIMPLE)
        if resultado:
            print(f"Tiempo de respuesta: {resultado['tiempo']:.2f} segundos")
            print("\nRespuesta:")
            print(resultado['respuesta'])
            print("\n" + "="*50)
    
    print("\n=== PRUEBA CASO COMPLEJO: QUICKMERGESORT ===")
    for modelo in modelos:
        print(f"\nProbando {modelo}...")
        resultado = test_modelo(modelo, PROMPT_COMPLEJO)
        if resultado:
            print(f"Tiempo de respuesta: {resultado['tiempo']:.2f} segundos")
            print("\nRespuesta:")
            print(resultado['respuesta'])
            print("\n" + "="*50)

if __name__ == "__main__":
    main()