"""
Demo Interactiva - Smart Optimizer
Hackathon OpenAI México 2025

Permite al usuario ingresar CUALQUIER tarea y demuestra el ciclo de automejora:
1. Usuario ingresa tarea libre
2. Sistema clasifica automáticamente el tipo
3. Run 1: Usa modelo caro sin estrategia
4. Auditor detecta ineficiencia
5. Memoria se actualiza con modelo optimizado
6. Run 2: Usa modelo optimizado
7. Visualizador muestra comparación impresionante

Uso:
    python demo_interactiva.py
"""

import os
import sys
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Verificar API key
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: OPENAI_API_KEY no encontrada en .env")
    print("💡 Tip: Copia env.template a .env y agrega tu API key")
    sys.exit(1)

from src.agente import SmartOptimizerAgent
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)


def mostrar_header():
    """Muestra el header de la demo interactiva"""
    print("\n" + "="*80)
    print(Fore.CYAN + Style.BRIGHT + "🎯 DEMO INTERACTIVA - SMART OPTIMIZER".center(80) + Style.RESET_ALL)
    print(Fore.CYAN + "Hackathon OpenAI México 2025".center(80) + Style.RESET_ALL)
    print("="*80)


def mostrar_ejemplos():
    """Muestra ejemplos de tareas que el usuario puede ingresar"""
    print("\n" + Fore.YELLOW + "📝 Escribe CUALQUIER tarea que quieras ejecutar:" + Style.RESET_ALL)
    print("\n" + Fore.GREEN + "Ejemplos de tareas que puedes probar:" + Style.RESET_ALL)
    print("  • " + Fore.CYAN + "Resume este artículo sobre inteligencia artificial" + Style.RESET_ALL)
    print("  • " + Fore.CYAN + "Traduce 'Hello World' al español y francés" + Style.RESET_ALL)
    print("  • " + Fore.CYAN + "Explícame qué es machine learning en 3 puntos" + Style.RESET_ALL)
    print("  • " + Fore.CYAN + "Escribe un email profesional de seguimiento a un cliente" + Style.RESET_ALL)
    print("  • " + Fore.CYAN + "Genera 5 ideas para un proyecto de Python" + Style.RESET_ALL)
    print("  • " + Fore.CYAN + "Analiza este código y sugiere mejoras" + Style.RESET_ALL)
    print("  • " + Fore.CYAN + "Crea un plan de marketing para un startup" + Style.RESET_ALL)


def obtener_input_usuario():
    """
    Obtiene la tarea del usuario de forma interactiva.
    
    Returns:
        str: La tarea ingresada por el usuario
    """
    mostrar_header()
    mostrar_ejemplos()
    
    print("\n" + "-"*80)
    print()
    
    try:
        tarea = input(Fore.YELLOW + Style.BRIGHT + "💬 Tu tarea: " + Style.RESET_ALL).strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Demo cancelada por el usuario")
        sys.exit(0)
    
    if not tarea:
        print(Fore.RED + "❌ Error: Debes ingresar una tarea" + Style.RESET_ALL)
        sys.exit(1)
    
    if len(tarea) < 10:
        print(Fore.YELLOW + "⚠️  Advertencia: Tarea muy corta, considera dar más detalles" + Style.RESET_ALL)
    
    return tarea


def limpiar_memoria():
    """
    Limpia la memoria para empezar fresh (sin estrategias previas).
    Esto asegura que el Run 1 siempre use el modelo caro por default.
    """
    print("\n" + Fore.CYAN + "🧹 Limpiando memoria del sistema..." + Style.RESET_ALL)
    
    try:
        with open("data/estrategias.json", "w") as f:
            json.dump({}, f, indent=2)
        print(Fore.GREEN + "✅ Memoria limpiada - Sistema empieza sin conocimiento previo" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"⚠️  Advertencia: No se pudo limpiar memoria: {e}" + Style.RESET_ALL)
    
    print()


def confirmar_ejecucion(tarea: str) -> bool:
    """
    Pide confirmación al usuario antes de ejecutar.
    
    Args:
        tarea: La tarea a ejecutar
    
    Returns:
        bool: True si el usuario confirma, False si cancela
    """
    print("\n" + "="*80)
    print(Fore.YELLOW + "📋 Tarea a ejecutar:" + Style.RESET_ALL)
    print(Fore.CYAN + f'   "{tarea}"' + Style.RESET_ALL)
    print("="*80)
    
    print("\n" + Fore.YELLOW + "El sistema ejecutará:" + Style.RESET_ALL)
    print("  1️⃣  " + Fore.RED + "Run 1: Modelo caro (GPT-4o) sin estrategia" + Style.RESET_ALL)
    print("  2️⃣  " + Fore.CYAN + "Auditor analiza y detecta ineficiencia" + Style.RESET_ALL)
    print("  3️⃣  " + Fore.GREEN + "Memoria se actualiza con modelo optimizado" + Style.RESET_ALL)
    print("  4️⃣  " + Fore.GREEN + "Run 2: Modelo optimizado (GPT-3.5-turbo o GPT-4o-mini)" + Style.RESET_ALL)
    print("  5️⃣  " + Fore.MAGENTA + "Visualizador muestra comparación" + Style.RESET_ALL)
    
    print("\n" + Fore.YELLOW + "⏱️  Tiempo estimado: 30-45 segundos" + Style.RESET_ALL)
    print()
    
    try:
        respuesta = input(Fore.YELLOW + "¿Continuar? (s/n): " + Style.RESET_ALL).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 Demo cancelada")
        return False
    
    return respuesta in ['s', 'si', 'sí', 'y', 'yes', '']


def mostrar_seccion_run1():
    """Muestra el header del Run 1"""
    print("\n" + "="*80)
    print(Fore.RED + Style.BRIGHT + "🔴 RUN 1 - SISTEMA INOCENTE (Sin estrategia)".center(80) + Style.RESET_ALL)
    print("="*80)
    print(Fore.RED + "💭 El sistema NO sabe qué modelo usar → Default GPT-4o (caro)" + Style.RESET_ALL)
    print()


def mostrar_seccion_aprendizaje(resultado1: dict):
    """
    Muestra la sección de aprendizaje entre Run 1 y Run 2.
    
    Args:
        resultado1: Resultado del Run 1 con métricas y feedback del auditor
    """
    print("\n" + "="*80)
    print(Fore.YELLOW + Style.BRIGHT + "🧠 SISTEMA APRENDIENDO".center(80) + Style.RESET_ALL)
    print("="*80)
    
    auditor_analysis = resultado1.get("auditor_analysis", "")
    auditor_recommendation = resultado1.get("auditor_recommendation", "desconocido")
    
    if auditor_analysis:
        print(Fore.YELLOW + "🔍 Auditor detectó:" + Style.RESET_ALL)
        print(f"   {auditor_analysis[:200]}...")
        print()
    
    print(Fore.GREEN + f"💡 Recomendación: Usar {auditor_recommendation}" + Style.RESET_ALL)
    print(Fore.GREEN + "💾 Memoria actualizada con estrategia optimizada" + Style.RESET_ALL)
    print()


def mostrar_seccion_run2():
    """Muestra el header del Run 2"""
    print("\n" + "="*80)
    print(Fore.GREEN + Style.BRIGHT + "🟢 RUN 2 - SISTEMA INTELIGENTE (Con estrategia aprendida)".center(80) + Style.RESET_ALL)
    print("="*80)
    print(Fore.GREEN + "💡 El sistema YA sabe qué modelo usar → Usa estrategia optimizada" + Style.RESET_ALL)
    print()


def main():
    """
    Función principal de la demo interactiva.
    
    Flujo:
        1. Obtiene input del usuario
        2. Limpia memoria
        3. Ejecuta Run 1 (modelo caro)
        4. Muestra aprendizaje del sistema
        5. Ejecuta Run 2 (modelo optimizado)
        6. Muestra visualización comparativa
    """
    try:
        # 1. Obtener input del usuario
        tarea_usuario = obtener_input_usuario()
        
        # 2. Confirmar ejecución
        if not confirmar_ejecucion(tarea_usuario):
            print("\n👋 Demo cancelada")
            sys.exit(0)
        
        # 3. Limpiar memoria para empezar fresh
        limpiar_memoria()
        
        # 4. Inicializar agente
        print(Fore.CYAN + "🚀 Inicializando Smart Optimizer Agent..." + Style.RESET_ALL)
        agente = SmartOptimizerAgent()
        print(Fore.GREEN + "✅ Agente inicializado" + Style.RESET_ALL)
        
        # 5. RUN 1 - Sistema inocente
        mostrar_seccion_run1()
        
        print(Fore.CYAN + "⏳ Ejecutando Run 1 (esto puede tardar 10-15 segundos)..." + Style.RESET_ALL)
        print()
        
        resultado1 = agente.ejecutar(tarea_usuario)
        
        metricas1 = resultado1.get("metricas_ejecucion", {})
        tokens1 = metricas1.get("tokens_totales", 0)
        modelo1 = metricas1.get("modelo_usado", "desconocido")
        costo1 = metricas1.get("costo_total", 0)
        
        print(Fore.GREEN + f"\n✅ Run 1 completado" + Style.RESET_ALL)
        print(f"   Modelo: {Fore.RED}{modelo1}{Style.RESET_ALL}")
        print(f"   Tokens: {tokens1}")
        print(f"   Costo: {Fore.RED}${costo1:.6f}{Style.RESET_ALL}")
        
        # 6. Mostrar aprendizaje
        mostrar_seccion_aprendizaje(resultado1)
        
        # 7. RUN 2 - Sistema inteligente
        mostrar_seccion_run2()
        
        print(Fore.CYAN + "⏳ Ejecutando Run 2 (esto puede tardar 10-15 segundos)..." + Style.RESET_ALL)
        print()
        
        resultado2 = agente.ejecutar(tarea_usuario)
        
        metricas2 = resultado2.get("metricas_ejecucion", {})
        tokens2 = metricas2.get("tokens_totales", 0)
        modelo2 = metricas2.get("modelo_usado", "desconocido")
        costo2 = metricas2.get("costo_total", 0)
        
        print(Fore.GREEN + f"\n✅ Run 2 completado" + Style.RESET_ALL)
        print(f"   Modelo: {Fore.GREEN}{modelo2}{Style.RESET_ALL}")
        print(f"   Tokens: {tokens2}")
        print(f"   Costo: {Fore.GREEN}${costo2:.6f}{Style.RESET_ALL}")
        
        # 8. Mostrar visualización comparativa (si ambos runs tienen métricas)
        if tokens1 > 0 and tokens2 > 0:
            from src.visualizador import mostrar_comparacion_run1_vs_run2
            
            mostrar_comparacion_run1_vs_run2(
                metricas1=metricas1,
                metricas2=metricas2,
                modelo1=modelo1,
                modelo2=modelo2,
                ruta1=resultado1.get('ruta', 'default'),
                ruta2=resultado2.get('ruta', 'optimizada')
            )
        else:
            print(Fore.RED + "\n⚠️  No se pudieron calcular comparaciones (falta de métricas)" + Style.RESET_ALL)
        
        # 9. Mensaje final
        print("\n" + "="*80)
        print(Fore.GREEN + Style.BRIGHT + "✅ DEMO COMPLETADA".center(80) + Style.RESET_ALL)
        print("="*80)
        
        # Calcular ahorro
        if costo1 > 0 and costo2 > 0:
            ahorro_costo = costo1 - costo2
            porcentaje_ahorro = (ahorro_costo / costo1) * 100
            
            print()
            print(Fore.YELLOW + "💰 Resumen del ahorro:" + Style.RESET_ALL)
            print(f"   Ahorro: {Fore.GREEN}${ahorro_costo:.6f}{Style.RESET_ALL} ({Fore.GREEN}{porcentaje_ahorro:.1f}%{Style.RESET_ALL})")
            print(f"   Proyección (1000 runs): {Fore.GREEN}${ahorro_costo * 1000:.2f}{Style.RESET_ALL}")
            
            if porcentaje_ahorro > 50:
                print()
                print(Fore.GREEN + Style.BRIGHT + "🏆 ¡EXCELENTE! Automejora demostrada con éxito" + Style.RESET_ALL)
        
        print()
        print(Fore.CYAN + "💡 Tip: Puedes ejecutar la demo cuantas veces quieras con diferentes tareas" + Style.RESET_ALL)
        print()
        
    except KeyboardInterrupt:
        print("\n\n" + Fore.YELLOW + "👋 Demo interrumpida por el usuario" + Style.RESET_ALL)
        sys.exit(0)
    except Exception as e:
        print("\n" + Fore.RED + f"❌ Error durante la demo: {e}" + Style.RESET_ALL)
        print(Fore.YELLOW + "💡 Tip: Verifica que tu OPENAI_API_KEY esté configurada correctamente" + Style.RESET_ALL)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
