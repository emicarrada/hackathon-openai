"""
Demo Interactiva RÁPIDA - Smart Optimizer
Para ejecutar directamente sin confirmaciones (útil para demos)

Uso:
    python demo_rapida_input.py "Tu tarea aquí"
    
Ejemplo:
    python demo_rapida_input.py "Resume este artículo sobre IA en 3 puntos"
"""

import os
import sys
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Verificar API key
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: OPENAI_API_KEY no encontrada")
    sys.exit(1)

from src.agente import SmartOptimizerAgent
from src.visualizador import mostrar_comparacion_run1_vs_run2
from colorama import Fore, Style, init

init(autoreset=True)


def limpiar_memoria():
    """Limpia memoria"""
    with open("data/estrategias.json", "w") as f:
        json.dump({}, f, indent=2)
    print("🧹 Memoria limpiada\n")


def main():
    # Obtener tarea del argumento o pedir input
    if len(sys.argv) > 1:
        tarea = " ".join(sys.argv[1:])
    else:
        print("\n" + "="*80)
        print(Fore.CYAN + Style.BRIGHT + "🎯 DEMO INTERACTIVA RÁPIDA".center(80))
        print("="*80 + "\n")
        tarea = input(Fore.YELLOW + "💬 Tu tarea: " + Style.RESET_ALL).strip()
        if not tarea:
            print("❌ Debes ingresar una tarea")
            sys.exit(1)
    
    print("\n" + "="*80)
    print(Fore.CYAN + f'📋 Tarea: "{tarea}"' + Style.RESET_ALL)
    print("="*80 + "\n")
    
    # Limpiar memoria
    limpiar_memoria()
    
    # Inicializar agente
    agente = SmartOptimizerAgent()
    
    # RUN 1
    print("="*80)
    print(Fore.RED + Style.BRIGHT + "🔴 RUN 1 - SISTEMA INOCENTE".center(80))
    print("="*80)
    print(Fore.RED + "💭 Sin estrategia → Usa GPT-4o (caro)\n")
    
    resultado1 = agente.ejecutar(tarea)
    metricas1 = resultado1.get("metricas_ejecucion", {})
    respuesta1 = resultado1.get("resultado_tarea", "")
    
    print(Fore.GREEN + f"\n✅ Run 1 completado: {metricas1.get('modelo_usado', 'N/A')}")
    print(f"   Tokens: {metricas1.get('tokens_totales', 0)}")
    print(f"   Costo: ${metricas1.get('costo_total', 0):.6f}")
    print(f"\n{Fore.CYAN}📝 Respuesta:{Style.RESET_ALL}")
    print(f"   {respuesta1[:200]}..." if len(respuesta1) > 200 else f"   {respuesta1}")
    
    # Aprendizaje
    print("\n" + "="*80)
    print(Fore.YELLOW + Style.BRIGHT + "🧠 APRENDIZAJE".center(80))
    print("="*80)
    print(Fore.GREEN + f"💡 Memoria actualizada: {resultado1.get('auditor_recommendation', 'N/A')}\n")
    
    # RUN 2
    print("="*80)
    print(Fore.GREEN + Style.BRIGHT + "🟢 RUN 2 - SISTEMA INTELIGENTE".center(80))
    print("="*80)
    print(Fore.GREEN + "💡 Con estrategia → Usa modelo optimizado\n")
    
    resultado2 = agente.ejecutar(tarea)
    metricas2 = resultado2.get("metricas_ejecucion", {})
    respuesta2 = resultado2.get("resultado_tarea", "")
    
    print(Fore.GREEN + f"\n✅ Run 2 completado: {metricas2.get('modelo_usado', 'N/A')}")
    print(f"   Tokens: {metricas2.get('tokens_totales', 0)}")
    print(f"   Costo: ${metricas2.get('costo_total', 0):.6f}")
    print(f"\n{Fore.CYAN}📝 Respuesta:{Style.RESET_ALL}")
    print(f"   {respuesta2[:200]}..." if len(respuesta2) > 200 else f"   {respuesta2}")
    
    # Visualización
    if metricas1.get('tokens_totales', 0) > 0 and metricas2.get('tokens_totales', 0) > 0:
        mostrar_comparacion_run1_vs_run2(
            metricas1=metricas1,
            metricas2=metricas2,
            modelo1=metricas1.get('modelo_usado', 'gpt-4o'),
            modelo2=metricas2.get('modelo_usado', 'gpt-3.5-turbo'),
            ruta1='default',
            ruta2='optimizada'
        )
    
    print("\n" + "="*80)
    print(Fore.GREEN + Style.BRIGHT + "✅ DEMO COMPLETADA".center(80))
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo cancelada")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
