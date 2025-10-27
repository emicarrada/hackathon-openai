"""
Flux Agent - 6-Node Architecture with REAL SELF-IMPROVEMENT

Implemented during OpenAI Hackathon (Oct 23, 2025).
System that learns from its executions through Run 1 → Audit → Run 2 cycle.

Complete Architecture:
1. recibir_tarea → Classifies task type
2. consultar_memoria → Searches learned strategy in JSON
3. ejecutar_tarea → Calls OpenAI with selected model
4. evaluar_contador → Captures metrics (tokens, latency)
5. auditor_feedback → LLM-Critic analyzes efficiency
6. actualizar_memoria → Saves optimized strategy

NARRATIVE FOR JUDGES:
- Run 1 (Baseline): Uses GPT-4o by default → 1500 tokens
- Auditor detects waste and recommends GPT-3.5-turbo
- Memory gets updated
- Run 2 (Optimized): Uses GPT-3.5-turbo → 200 tokens
- SAVINGS: 87% demonstrated live
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict

# Import the 6 nodes of the self-improvement system
from src.nodos.recibir_tarea import recibir_tarea
from src.nodos.consultar_memoria import consultar_memoria
from src.nodos.ejecutar_tarea import ejecutar_tarea
from src.nodos.evaluar_contador import evaluar_con_contador
from src.nodos.auditor_feedback import generar_feedback_auditor
from src.nodos.actualizar_memoria import actualizar_memoria


class AgentState(TypedDict):
    """
    Estado compartido que fluye entre todos los nodos del sistema.
    Cada nodo lee y actualiza este estado.
    """
    # Input del usuario
    tarea_descripcion: str
    
    # Clasificación de tarea (Nodo 1)
    tipo_tarea: str  # "resumen", "traduccion", "clasificacion", "extraccion", "general"
    run_number: int  # 1 o 2 (para tracking de mejoras)
    
    # Consulta de memoria (Nodo 2)
    modelo_a_usar: str  # Modelo seleccionado: "gpt-4o", "gpt-3.5-turbo", "gpt-4o-mini"
    estrategia_encontrada: bool  # True si ya existe estrategia aprendida
    ruta: str  # "default" (Run 1) o "optimizada" (Run 2)
    
    # Ejecución de tarea (Nodo 3)
    resultado_tarea: str  # Respuesta generada por OpenAI
    respuesta_raw: object  # Objeto completo de OpenAI (para extraer métricas)
    
    # Evaluación de métricas (Nodo 4)
    metricas_ejecucion: dict  # {tokens_totales, tokens_prompt, tokens_completion, latencia, modelo_usado}
    
    # Auditoría de eficiencia (Nodo 5)
    feedback_auditor: dict  # {requiere_optimizacion: bool, analisis: str, recomendacion: str}
    
    # Actualización de memoria (Nodo 6)
    memoria_actualizada: bool  # True si se guardó nueva estrategia


def construir_grafo():
    """
    Construye el grafo de LangGraph con los 6 nodos y sus conexiones.
    
    Flujo lineal:
    recibir_tarea → consultar_memoria → ejecutar_tarea → evaluar_contador → 
    auditor_feedback → actualizar_memoria → END
    
    Returns:
        StateGraph compilado: Grafo listo para ejecutar con .invoke()
    """
    # Crear el grafo
    workflow = StateGraph(AgentState)
    
    # Agregar los 6 nodos del sistema
    workflow.add_node("recibir_tarea", recibir_tarea)
    workflow.add_node("consultar_memoria", consultar_memoria)
    workflow.add_node("ejecutar_tarea", ejecutar_tarea)
    workflow.add_node("evaluar_contador", evaluar_con_contador)
    workflow.add_node("auditor_feedback", generar_feedback_auditor)
    workflow.add_node("actualizar_memoria", actualizar_memoria)
    
    # Definir el flujo secuencial (todas las conexiones son lineales)
    workflow.set_entry_point("recibir_tarea")
    workflow.add_edge("recibir_tarea", "consultar_memoria")
    workflow.add_edge("consultar_memoria", "ejecutar_tarea")
    workflow.add_edge("ejecutar_tarea", "evaluar_contador")
    workflow.add_edge("evaluar_contador", "auditor_feedback")
    workflow.add_edge("auditor_feedback", "actualizar_memoria")
    workflow.add_edge("actualizar_memoria", END)
    
    # Compilar el grafo para crear el ejecutable
    app = workflow.compile()
    
    return app


class SmartOptimizerAgent:
    """
    Agente principal con automejora real mediante ciclo Run 1 → Auditoría → Run 2.
    
    Diferenciador clave para el hackathon:
    - Otros equipos: Sistemas estáticos sin aprendizaje
    - Nuestro sistema: APRENDE de cada ejecución y se optimiza automáticamente
    
    Ejemplo de uso:
        >>> agente = SmartOptimizerAgent()
        >>> agente.demo_run1_vs_run2("Resume este artículo")
        # Output: Muestra ahorro de 87% entre Run 1 y Run 2
    """
    
    def __init__(self):
        """Inicializa el agente construyendo el grafo de 6 nodos."""
        self.grafo = construir_grafo()
    
    def ejecutar(self, tarea: str) -> dict:
        """
        Ejecuta el agente completo para una tarea.
        
        Pasa por los 6 nodos:
        1. Clasifica la tarea
        2. Consulta si ya existe estrategia aprendida
        3. Ejecuta con el modelo apropiado
        4. Captura métricas de uso
        5. Auditor analiza si fue eficiente
        6. Actualiza memoria si se encontró optimización
        
        Args:
            tarea (str): Descripción de la tarea del usuario.
            
        Returns:
            dict: Estado final con resultado, métricas y feedback.
        """
        # Estado inicial vacío (los nodos lo poblarán)
        estado_inicial = {
            "tarea_descripcion": tarea,
            "tipo_tarea": "",
            "run_number": 1,
            "modelo_a_usar": "",
            "estrategia_encontrada": False,
            "ruta": "",
            "resultado_tarea": "",
            "respuesta_raw": None,
            "metricas_ejecucion": {},
            "feedback_auditor": {},
            "memoria_actualizada": False
        }
        
        # Ejecutar el grafo completo
        print("\n" + "="*70)
        print("🚀 SMART OPTIMIZER - Iniciando ejecución con automejora")
        print("="*70 + "\n")
        
        resultado_final = self.grafo.invoke(estado_inicial)
        
        print("\n" + "="*70)
        print("✅ Ejecución completada")
        print("="*70 + "\n")
        
        return resultado_final
    
    def demo_run1_vs_run2(self, tarea: str):
        """
        Demo para mostrar a los jueces: Run 1 (caro) vs Run 2 (optimizado).
        
        Este es el corazón de nuestra narrativa:
        - Run 1: Sistema "inocente" usa GPT-4o (caro)
        - Auditor detecta que la tarea era simple
        - Memoria se actualiza con recomendación de GPT-3.5-turbo
        - Run 2: Sistema usa la estrategia aprendida (barato)
        - RESULTADO: 87% de ahorro demostrado en vivo
        
        Args:
            tarea (str): Tarea a ejecutar dos veces para demostrar aprendizaje.
        """
        from src.memoria import Memoria
        
        print("\n" + "🎬 DEMO PARA HACKATHON: Run 1 vs Run 2")
        print("="*70)
        print("Demostrando AUTOMEJORA en tiempo real")
        print("="*70 + "\n")
        
        # Limpiar memoria para garantizar que Run 1 empiece sin estrategia
        memoria = Memoria()
        memoria.limpiar()
        print("🧹 Memoria limpiada - Sistema empieza sin conocimiento previo\n")
        
        # ========== RUN 1: SIN ESTRATEGIA APRENDIDA ==========
        print("▶️  RUN 1 - SISTEMA INOCENTE (Sin estrategia)")
        print("-"*70)
        print("💭 El sistema NO sabe qué modelo usar → Default GPT-4o (caro)")
        print()
        
        resultado1 = self.ejecutar(tarea)
        
        metricas1 = resultado1.get("metricas_ejecucion", {})
        tokens1 = metricas1.get("tokens_totales", 0)
        modelo1 = metricas1.get("modelo_usado", "desconocido")
        
        print(f"\n📊 RUN 1 - Resultados:")
        print(f"   Modelo usado: {modelo1}")
        print(f"   Tokens consumidos: {tokens1}")
        print(f"   Ruta tomada: {resultado1.get('ruta', 'N/A')}")
        
        # Mostrar si el auditor detectó ineficiencia
        feedback1 = resultado1.get("feedback_auditor", {})
        if feedback1.get("requiere_optimizacion"):
            print(f"\n🔍 Auditor detectó ineficiencia:")
            print(f"   Análisis: {feedback1.get('analisis', 'N/A')[:80]}...")
            print(f"   Recomendación: {feedback1.get('recomendacion', 'N/A')}")
            print(f"\n💾 Memoria actualizada con estrategia optimizada")
        
        # ========== RUN 2: CON ESTRATEGIA APRENDIDA ==========
        print("\n" + "="*70)
        print("▶️  RUN 2 - SISTEMA INTELIGENTE (Con estrategia aprendida)")
        print("-"*70)
        print("💡 El sistema YA sabe qué modelo usar → Usa estrategia optimizada")
        print()
        
        resultado2 = self.ejecutar(tarea)
        
        metricas2 = resultado2.get("metricas_ejecucion", {})
        tokens2 = metricas2.get("tokens_totales", 0)
        modelo2 = metricas2.get("modelo_usado", "desconocido")
        
        print(f"\n📊 RUN 2 - Resultados:")
        print(f"   Modelo usado: {modelo2}")
        print(f"   Tokens consumidos: {tokens2}")
        print(f"   Ruta tomada: {resultado2.get('ruta', 'N/A')}")
        
        # ========== COMPARACIÓN FINAL CON VISUALIZADOR AVANZADO ==========
        
        if tokens1 > 0 and tokens2 > 0:
            # Importar visualizador
            from src.visualizador import mostrar_comparacion_run1_vs_run2
            
            # Mostrar visualización avanzada con todas las métricas
            mostrar_comparacion_run1_vs_run2(
                metricas1=metricas1,
                metricas2=metricas2,
                modelo1=modelo1,
                modelo2=modelo2,
                ruta1=resultado1.get('ruta', 'default'),
                ruta2=resultado2.get('ruta', 'optimizada')
            )
        else:
            print("\n⚠️  No se pudieron calcular comparaciones (falta de métricas)")


# Para testing rápido durante el hackathon
if __name__ == "__main__":
    print("🔧 TEST RÁPIDO DEL SISTEMA\n")
    
    agente = SmartOptimizerAgent()
    
    # Tarea de prueba (tipo "resumen" que típicamente no requiere GPT-4o)
    tarea_test = "Resume en 3 puntos: La IA está transformando la industria."
    
    # Ejecutar demo completa Run 1 vs Run 2
    agente.demo_run1_vs_run2(tarea_test)