"""
Demo de clasificación inteligente de tareas.
Muestra cómo el sistema detecta diferentes tipos y adapta sus respuestas.
"""

from src.agente import SmartOptimizerAgent
from src.utils import llamar_openai_simple
from typing import Dict, Any
import time
import os

def configurar_ambiente():
    """Configura el ambiente y valida la API key"""
    # Intentar obtener API Key de diferentes fuentes
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        # Si no está en variables de ambiente, buscar en archivo .env
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")
        except ImportError:
            pass
    
    if not api_key:
        print("\n❌ Error: OPENAI_API_KEY no encontrada")
        print("\nPor favor, configura tu API key de alguna de estas formas:")
        print("1. Variable de ambiente:")
        print("   export OPENAI_API_KEY='tu-api-key'")
        print("\n2. Archivo .env en el directorio del proyecto:")
        print("   OPENAI_API_KEY=tu-api-key")
        exit(1)
    
    try:
        # Configurar la API key
        llamar_openai_simple(api_key)
        print("✅ API key configurada correctamente\n")
    except Exception as e:
        print(f"\n❌ Error al configurar API key: {str(e)}")
        exit(1)

# Configurar ambiente antes de comenzar
configurar_ambiente()


# Ejemplos de tareas diseñadas para demostrar cada tipo
tareas_ejemplo = [
    # Tareas simples (deberían usar GPT-3.5-turbo)
    "Resume en 3 puntos el siguiente artículo sobre IA",
    "Traduce al inglés: Los sistemas inteligentes mejoran cada día",
    "Extrae las palabras clave de este párrafo técnico",
    
    # Tareas complejas (posiblemente necesiten GPT-4)
    "Analiza el impacto de la IA en el mercado laboral y sugiere adaptaciones",
    "Compara detalladamente las arquitecturas de Python y JavaScript",
    "Genera una implementación eficiente de QuickSort en Python con análisis",
    
    # Tareas creativas o especializadas
    "Escribe un poema técnico sobre el futuro de la programación",
    "Explica el concepto de transformers en deep learning",
    "Clasifica estos algoritmos según su complejidad computacional"
]

def imprimir_cabecera():
    """Imprime la cabecera del demo con estilo"""
    print("\n" + "="*70)
    print("🎯 DEMO: Sistema de Clasificación Inteligente con Automejora")
    print("="*70 + "\n")
    print("Este demo muestra el sistema completo en acción:")
    print("1. 🎯 Clasificación automática del tipo de tarea")
    print("2. 🧠 Consulta de memoria para estrategias previas")
    print("3. 🤖 Ejecución optimizada según el tipo")
    print("4. 📊 Métricas de uso (tokens, modelo)")
    print("5. 🔍 Auditoría de eficiencia")
    print("6. 💾 Actualización de memoria con mejoras\n")
    print("Para cada tarea, verás:")
    print("- Run 1: Primera ejecución (sin estrategia previa)")
    print("- Run 2: Segunda ejecución (con estrategia aprendida)")
    print("- Comparación y ahorro conseguido\n")

def formatear_resultado(resultado: Dict[str, Any]) -> None:
    """Formatea y muestra el resultado de una tarea"""
    tipo = resultado.get("tipo_tarea", "?")
    modelo = resultado.get("metricas_ejecucion", {}).get("modelo_usado", "?")
    tokens = resultado.get("metricas_ejecucion", {}).get("tokens_totales", 0)
    
    # Emojis según tipo de tarea
    emojis_tipo = {
        "codigo": "💻",
        "creatividad": "🎨",
        "analisis": "📊",
        "qa": "❓",
        "resumen": "📝",
        "traduccion": "🌎",
        "clasificacion": "🏷️",
        "extraccion": "🔍",
        "comparacion": "⚖️",
        "general": "🔄"
    }
    emoji = emojis_tipo.get(tipo, "🔄")
    
    print(f"\n   {emoji} Tipo detectado: {tipo}")
    print(f"   📋 Modelo elegido: {modelo}")
    print(f"   🔢 Tokens usados: {tokens}")
    
    # Mostrar ruta y estrategia
    ruta = resultado.get("ruta", "default")
    print(f"   🛣️  Ruta: {ruta}")
    
    # Mostrar feedback del auditor si existe
    feedback = resultado.get("feedback_auditor", {})
    if feedback:
        requiere_opt = feedback.get("requiere_optimizacion", False)
        print(f"\n   📊 Análisis del Auditor:")
        print(f"   {'⚠️' if requiere_opt else '✅'} {feedback.get('analisis', 'No disponible')}")
        if requiere_opt:
            print(f"   💡 Recomendación: {feedback.get('recomendacion', 'No disponible')}")
    
    # Mostrar si se actualizó la memoria
    if resultado.get("memoria_actualizada"):
        print(f"\n   💾 ¡Memoria actualizada con nueva estrategia!")
    
    print()

def ejecutar_demo_tarea(agente: SmartOptimizerAgent, tarea: str, numero: int) -> None:
    """Ejecuta una tarea individual y muestra sus resultados"""
    print(f"\n{numero}. 📝 Tarea: {tarea}")
    print("   " + "-" * 50)
    
    try:
        # Run 1: Primera ejecución (sin estrategia aprendida)
        print("   🔄 Run 1 (Sin estrategia previa)...")
        resultado1 = agente.ejecutar(tarea)
        formatear_resultado(resultado1)
        
        # Pequeña pausa para legibilidad
        time.sleep(1)
        
        # Run 2: Segunda ejecución (con estrategia aprendida)
        print("\n   🔄 Run 2 (Con estrategia aprendida)...")
        resultado2 = agente.ejecutar(tarea)
        formatear_resultado(resultado2)
        
        # Mostrar comparación de tokens
        tokens1 = resultado1.get("metricas_ejecucion", {}).get("tokens_totales", 0)
        tokens2 = resultado2.get("metricas_ejecucion", {}).get("tokens_totales", 0)
        if tokens1 and tokens2:
            ahorro = ((tokens1 - tokens2) / tokens1) * 100
            print(f"\n   💰 Ahorro conseguido: {ahorro:.1f}%")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}\n")
    
    print("=" * 70 + "\n")

def main():
    """Función principal del demo"""
    try:
        imprimir_cabecera()
        
        # Inicializar agente
        agente = SmartOptimizerAgent()
        
        # Procesar cada tarea de ejemplo
        for i, tarea in enumerate(tareas_ejemplo, 1):
            ejecutar_demo_tarea(agente, tarea, i)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrumpido por el usuario")
        exit(0)
    except Exception as e:
        print(f"\n❌ Error en la ejecución del demo: {str(e)}")
        print("\nAsegúrate de que:")
        print("1. La API key está configurada correctamente")
        print("2. Tienes conexión a internet")
        print("3. El servicio de OpenAI está disponible")
        exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error en el demo: {str(e)}")