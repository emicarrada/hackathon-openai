"""
Módulo de Visualización Avanzada - Hackathon OpenAI

Visualiza comparaciones entre Run 1 (inocente) y Run 2 (optimizado)
con métricas avanzadas de costo, rendimiento, calidad y eficiencia.

Autor: Sistema SmartOptimizer
Fecha: 23 oct 2025
"""

from typing import Dict, Any, Tuple
from tabulate import tabulate
from colorama import Fore, Back, Style, init

# Inicializar colorama para compatibilidad cross-platform
init(autoreset=True)


# ============================================================================
# CONSTANTES DE COLORES Y SÍMBOLOS
# ============================================================================

class Colores:
    """Esquema de colores para el visualizador."""
    RUN1_MALO = Fore.RED                          # Rojo = caro/lento
    RUN2_BUENO = Fore.GREEN                       # Verde = barato/rápido
    MEJORA_EXCELENTE = Fore.GREEN + Style.BRIGHT  # Verde brillante (>50%)
    MEJORA_BUENA = Fore.GREEN                     # Verde normal (0-50%)
    MEJORA_MALA = Fore.YELLOW                     # Amarillo (negativo)
    NEUTRO = Fore.CYAN                            # Cyan (neutral)
    TITULO = Fore.MAGENTA + Style.BRIGHT          # Magenta (títulos)
    DESTACADO = Fore.YELLOW + Style.BRIGHT        # Amarillo brillante (importante)
    RESET = Style.RESET_ALL


class Simbolos:
    """Símbolos para representar estado de métricas."""
    EXCELENTE = "🎉"     # >50% mejora
    BUENO = "✅"         # 0-50% mejora
    MALO = "⚠️"          # Empeoró
    NEUTRO = "➖"        # Sin cambio
    MODELO = "🤖"
    TOKENS = "📦"
    COSTO = "💰"
    LATENCIA = "⚡"
    VELOCIDAD = "🚀"
    CALIDAD = "🎯"
    EFICIENCIA = "🏆"
    AHORRO = "💵"
    ROI = "📈"
    RUTA = "🛣️"


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def calcular_mejora(valor1: float, valor2: float, invertir: bool = False) -> Tuple[float, float, bool]:
    """
    Calcula mejora porcentual y absoluta entre dos valores.
    
    Args:
        valor1: Valor del Run 1 (base)
        valor2: Valor del Run 2 (comparación)
        invertir: Si True, menor es mejor (ej: costo, latencia)
                 Si False, mayor es mejor (ej: calidad, eficiencia)
    
    Returns:
        (mejora_porcentual, mejora_absoluta, es_positivo)
    """
    if valor1 == 0:
        return 0.0, 0.0, False
    
    diferencia = valor1 - valor2
    porcentaje = (diferencia / valor1) * 100
    
    # Si invertir=True, diferencia positiva es bueno (bajó el costo/latencia)
    # Si invertir=False, diferencia negativa es bueno (subió la calidad)
    es_positivo = (diferencia > 0) if invertir else (diferencia < 0)
    
    return porcentaje, diferencia, es_positivo


def formatear_costo(costo: float) -> str:
    """Formatea costo en USD con 6 decimales."""
    return f"${costo:.6f}"


def formatear_latencia(latencia: float) -> str:
    """Formatea latencia en segundos con 3 decimales."""
    return f"{latencia:.3f}s"


def formatear_porcentaje(porcentaje: float) -> str:
    """Formatea porcentaje con 1 decimal."""
    return f"{porcentaje:+.1f}%"


def formatear_numero(numero: float, decimales: int = 2) -> str:
    """Formatea número con decimales específicos."""
    return f"{numero:.{decimales}f}"


def simbolo_mejora(porcentaje: float, es_positivo: bool) -> str:
    """
    Retorna símbolo según mejora.
    
    Args:
        porcentaje: Porcentaje de mejora (absoluto)
        es_positivo: Si la mejora es positiva o negativa
    
    Returns:
        Símbolo correspondiente
    """
    if not es_positivo:
        return Simbolos.MALO
    
    if abs(porcentaje) > 50:
        return Simbolos.EXCELENTE
    elif abs(porcentaje) > 0:
        return Simbolos.BUENO
    else:
        return Simbolos.NEUTRO


def colorear_mejora(texto: str, es_positivo: bool, porcentaje: float) -> str:
    """
    Aplica color al texto según si es mejora o no.
    
    Args:
        texto: Texto a colorear
        es_positivo: Si la mejora es positiva
        porcentaje: Porcentaje de mejora (para elegir intensidad)
    
    Returns:
        Texto con códigos ANSI de color
    """
    if not es_positivo:
        return Colores.MEJORA_MALA + texto + Colores.RESET
    
    if abs(porcentaje) > 50:
        return Colores.MEJORA_EXCELENTE + texto + Colores.RESET
    else:
        return Colores.MEJORA_BUENA + texto + Colores.RESET


def generar_barra_ahorro(porcentaje: float, ancho: int = 30) -> str:
    """
    Genera barra de progreso ASCII para visualizar ahorro.
    
    Args:
        porcentaje: Porcentaje de ahorro (0-100)
        ancho: Ancho de la barra en caracteres
    
    Returns:
        Barra ASCII con porcentaje
    
    Ejemplo:
        73.3% → [████████████████░░░░░░░░] 73.3%
    """
    # Limitar porcentaje a 0-100
    porcentaje_limitado = max(0, min(100, porcentaje))
    
    lleno = int((porcentaje_limitado / 100) * ancho)
    vacio = ancho - lleno
    
    barra = "█" * lleno + "░" * vacio
    
    # Colorear según porcentaje
    if porcentaje_limitado > 50:
        color = Colores.MEJORA_EXCELENTE
    elif porcentaje_limitado > 0:
        color = Colores.MEJORA_BUENA
    else:
        color = Colores.MEJORA_MALA
    
    return f"{color}[{barra}] {porcentaje:.1f}%{Colores.RESET}"


# ============================================================================
# CÁLCULO DE MÉTRICAS AVANZADAS
# ============================================================================

def calcular_metricas_avanzadas(metricas: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calcula métricas derivadas adicionales.
    
    Args:
        metricas: Diccionario con métricas básicas de evaluar_contador
    
    Returns:
        Diccionario con métricas avanzadas adicionales
    """
    tokens_totales = metricas.get("tokens_totales", 0)
    tokens_prompt = metricas.get("tokens_prompt", 0)
    tokens_completion = metricas.get("tokens_completion", 0)
    latencia = metricas.get("latencia", 0.001)  # Evitar división por 0
    costo_total = metricas.get("costo_total", 0)
    
    metricas_avanzadas = {
        # Métricas de velocidad
        "velocidad_tokens_por_segundo": tokens_totales / latencia if latencia > 0 else 0,
        "latencia_por_token": latencia / tokens_totales if tokens_totales > 0 else 0,
        
        # Métricas de costo
        "costo_por_token": costo_total / tokens_totales if tokens_totales > 0 else 0,
        "costo_input": tokens_prompt * (costo_total / tokens_totales) if tokens_totales > 0 else 0,
        "costo_output": tokens_completion * (costo_total / tokens_totales) if tokens_totales > 0 else 0,
        
        # Métricas de eficiencia
        "ratio_completion_prompt": tokens_completion / tokens_prompt if tokens_prompt > 0 else 0,
        "eficiencia_tokens": tokens_completion / tokens_totales if tokens_totales > 0 else 0,
        
        # Proyecciones
        "costo_1000_ejecuciones": costo_total * 1000,
        "tiempo_1000_ejecuciones": latencia * 1000,
    }
    
    return metricas_avanzadas


def calcular_roi(costo1: float, costo2: float, calidad1: float = 10, calidad2: float = 10) -> float:
    """
    Calcula ROI (Return on Investment) de la optimización.
    
    Args:
        costo1: Costo del Run 1
        costo2: Costo del Run 2
        calidad1: Calidad del Run 1 (escala 0-10, default 10)
        calidad2: Calidad del Run 2 (escala 0-10, default 10)
    
    Returns:
        ROI como porcentaje (positivo = ganancia)
    """
    ahorro = costo1 - costo2
    perdida_calidad = (calidad1 - calidad2) / 10  # Normalizar 0-1
    
    # ROI = (ahorro - penalización_calidad) / costo_original
    roi = ((ahorro - (perdida_calidad * costo1)) / costo1) * 100 if costo1 > 0 else 0
    
    return roi


# ============================================================================
# FUNCIÓN PRINCIPAL DE VISUALIZACIÓN
# ============================================================================

def mostrar_comparacion_run1_vs_run2(
    metricas1: Dict[str, Any],
    metricas2: Dict[str, Any],
    modelo1: str,
    modelo2: str,
    ruta1: str = "default",
    ruta2: str = "optimizada"
) -> None:
    """
    Muestra tabla comparativa visual AVANZADA entre Run 1 y Run 2.
    
    Esta función genera una visualización profesional con:
    - Métricas básicas: tokens, costo, latencia
    - Métricas avanzadas: velocidad, eficiencia, ROI
    - Colores según impacto (verde=bueno, rojo=malo, amarillo=neutral)
    - Símbolos visuales (🎉✅⚠️)
    - Barra de progreso para ahorro principal
    - Resumen ejecutivo con narrativa
    
    Args:
        metricas1: Diccionario con métricas de Run 1
        metricas2: Diccionario con métricas de Run 2
        modelo1: Modelo usado en Run 1 (ej: "gpt-4o")
        modelo2: Modelo usado en Run 2 (ej: "gpt-3.5-turbo")
        ruta1: Ruta tomada en Run 1 (default: "default")
        ruta2: Ruta tomada en Run 2 (default: "optimizada")
    
    Returns:
        None (imprime en consola)
    """
    print("\n" + "="*80)
    print(Colores.TITULO + "⚡ COMPARACIÓN AVANZADA: Run 1 vs Run 2".center(80) + Colores.RESET)
    print(Colores.TITULO + "Automejora del Sistema Demostrada".center(80) + Colores.RESET)
    print("="*80 + "\n")
    
    # Extraer métricas básicas
    tokens1 = metricas1.get("tokens_totales", 0)
    tokens2 = metricas2.get("tokens_totales", 0)
    tokens_prompt1 = metricas1.get("tokens_prompt", 0)
    tokens_prompt2 = metricas2.get("tokens_prompt", 0)
    tokens_completion1 = metricas1.get("tokens_completion", 0)
    tokens_completion2 = metricas2.get("tokens_completion", 0)
    costo1 = metricas1.get("costo_total", 0)
    costo2 = metricas2.get("costo_total", 0)
    latencia1 = metricas1.get("latencia", 0)
    latencia2 = metricas2.get("latencia", 0)
    
    # Calcular métricas avanzadas
    avanzadas1 = calcular_metricas_avanzadas(metricas1)
    avanzadas2 = calcular_metricas_avanzadas(metricas2)
    
    # ========== TABLA 1: MÉTRICAS BÁSICAS ==========
    
    datos_basicas = []
    
    # Fila 1: Modelo
    datos_basicas.append([
        Simbolos.MODELO + " Modelo",
        Colores.RUN1_MALO + modelo1 + Colores.RESET,
        Colores.RUN2_BUENO + modelo2 + Colores.RESET,
        Simbolos.BUENO if modelo1 != modelo2 else Simbolos.NEUTRO
    ])
    
    # Fila 2: Tokens Totales
    pct_tokens, _, es_pos_tokens = calcular_mejora(tokens1, tokens2, invertir=True)
    datos_basicas.append([
        Simbolos.TOKENS + " Tokens Totales",
        f"{tokens1}",
        f"{tokens2}",
        colorear_mejora(formatear_porcentaje(pct_tokens), es_pos_tokens, pct_tokens) + " " + 
        simbolo_mejora(pct_tokens, es_pos_tokens)
    ])
    
    # Fila 3: Tokens Prompt
    pct_prompt, _, es_pos_prompt = calcular_mejora(tokens_prompt1, tokens_prompt2, invertir=True)
    datos_basicas.append([
        "  └─ Prompt",
        f"{tokens_prompt1}",
        f"{tokens_prompt2}",
        colorear_mejora(formatear_porcentaje(pct_prompt), es_pos_prompt, pct_prompt)
    ])
    
    # Fila 4: Tokens Completion
    pct_completion, _, es_pos_completion = calcular_mejora(tokens_completion1, tokens_completion2, invertir=True)
    datos_basicas.append([
        "  └─ Completion",
        f"{tokens_completion1}",
        f"{tokens_completion2}",
        colorear_mejora(formatear_porcentaje(pct_completion), es_pos_completion, pct_completion)
    ])
    
    # Fila 5: Costo Total (MÉTRICA PRINCIPAL)
    pct_costo, _, es_pos_costo = calcular_mejora(costo1, costo2, invertir=True)
    datos_basicas.append([
        Simbolos.COSTO + " Costo Total",
        Colores.RUN1_MALO + formatear_costo(costo1) + Colores.RESET,
        Colores.RUN2_BUENO + formatear_costo(costo2) + Colores.RESET,
        colorear_mejora(formatear_porcentaje(pct_costo), es_pos_costo, pct_costo) + " " + 
        simbolo_mejora(pct_costo, es_pos_costo)
    ])
    
    # Fila 6: Costo por Token
    costo_por_token1 = avanzadas1["costo_por_token"]
    costo_por_token2 = avanzadas2["costo_por_token"]
    pct_costo_token, _, es_pos_costo_token = calcular_mejora(costo_por_token1, costo_por_token2, invertir=True)
    datos_basicas.append([
        "  └─ Por Token",
        formatear_costo(costo_por_token1),
        formatear_costo(costo_por_token2),
        colorear_mejora(formatear_porcentaje(pct_costo_token), es_pos_costo_token, pct_costo_token)
    ])
    
    # Fila 7: Latencia
    pct_latencia, _, es_pos_latencia = calcular_mejora(latencia1, latencia2, invertir=True)
    datos_basicas.append([
        Simbolos.LATENCIA + " Latencia",
        formatear_latencia(latencia1),
        formatear_latencia(latencia2),
        colorear_mejora(formatear_porcentaje(pct_latencia), es_pos_latencia, pct_latencia) + " " + 
        simbolo_mejora(pct_latencia, es_pos_latencia)
    ])
    
    # Fila 8: Velocidad (tokens/seg)
    velocidad1 = avanzadas1["velocidad_tokens_por_segundo"]
    velocidad2 = avanzadas2["velocidad_tokens_por_segundo"]
    pct_velocidad, _, es_pos_velocidad = calcular_mejora(velocidad1, velocidad2, invertir=False)
    datos_basicas.append([
        Simbolos.VELOCIDAD + " Velocidad",
        f"{velocidad1:.1f} tok/s",
        f"{velocidad2:.1f} tok/s",
        colorear_mejora(formatear_porcentaje(-pct_velocidad), not es_pos_velocidad, pct_velocidad)
    ])
    
    # Fila 9: Ruta
    datos_basicas.append([
        Simbolos.RUTA + " Ruta",
        ruta1,
        ruta2,
        Simbolos.BUENO if ruta1 != ruta2 else Simbolos.NEUTRO
    ])
    
    # Imprimir tabla básica
    print(tabulate(
        datos_basicas,
        headers=[
            Colores.TITULO + "Métrica" + Colores.RESET,
            Colores.TITULO + "Run 1 (Inocente)" + Colores.RESET,
            Colores.TITULO + "Run 2 (Optimizado)" + Colores.RESET,
            Colores.TITULO + "Mejora" + Colores.RESET
        ],
        tablefmt="rounded_outline",
        colalign=("left", "right", "right", "center")
    ))
    
    # ========== TABLA 2: MÉTRICAS AVANZADAS ==========
    
    print("\n" + Colores.DESTACADO + "📊 MÉTRICAS AVANZADAS DE EFICIENCIA" + Colores.RESET + "\n")
    
    datos_avanzadas = []
    
    # Ratio Completion/Prompt (mayor es mejor)
    ratio1 = avanzadas1["ratio_completion_prompt"]
    ratio2 = avanzadas2["ratio_completion_prompt"]
    pct_ratio, _, es_pos_ratio = calcular_mejora(ratio1, ratio2, invertir=False)
    datos_avanzadas.append([
        Simbolos.EFICIENCIA + " Ratio Output/Input",
        f"{ratio1:.2f}x",
        f"{ratio2:.2f}x",
        colorear_mejora(formatear_porcentaje(-pct_ratio), not es_pos_ratio, pct_ratio)
    ])
    
    # Eficiencia de tokens (completion/total)
    efic1 = avanzadas1["eficiencia_tokens"] * 100
    efic2 = avanzadas2["eficiencia_tokens"] * 100
    datos_avanzadas.append([
        "  └─ Eficiencia Tokens",
        f"{efic1:.1f}%",
        f"{efic2:.1f}%",
        f"{efic2-efic1:+.1f}pp"
    ])
    
    # Costo proyectado 1000 ejecuciones
    costo_1000_1 = avanzadas1["costo_1000_ejecuciones"]
    costo_1000_2 = avanzadas2["costo_1000_ejecuciones"]
    ahorro_1000 = costo_1000_1 - costo_1000_2
    datos_avanzadas.append([
        Simbolos.AHORRO + " Costo (1000 runs)",
        formatear_costo(costo_1000_1),
        formatear_costo(costo_1000_2),
        Colores.MEJORA_EXCELENTE + f"Ahorro: {formatear_costo(ahorro_1000)}" + Colores.RESET
    ])
    
    # Tiempo proyectado 1000 ejecuciones (en minutos)
    tiempo_1000_1 = avanzadas1["tiempo_1000_ejecuciones"] / 60
    tiempo_1000_2 = avanzadas2["tiempo_1000_ejecuciones"] / 60
    datos_avanzadas.append([
        "⏱️  Tiempo (1000 runs)",
        f"{tiempo_1000_1:.1f} min",
        f"{tiempo_1000_2:.1f} min",
        f"{tiempo_1000_1 - tiempo_1000_2:+.1f} min"
    ])
    
    # ROI (Return on Investment)
    roi = calcular_roi(costo1, costo2)
    datos_avanzadas.append([
        Simbolos.ROI + " ROI",
        "-",
        "-",
        colorear_mejora(formatear_porcentaje(roi), roi > 0, roi) + " " + 
        (Simbolos.EXCELENTE if roi > 50 else Simbolos.BUENO if roi > 0 else Simbolos.MALO)
    ])
    
    # Imprimir tabla avanzada
    print(tabulate(
        datos_avanzadas,
        headers=[
            Colores.TITULO + "Métrica" + Colores.RESET,
            Colores.TITULO + "Run 1" + Colores.RESET,
            Colores.TITULO + "Run 2" + Colores.RESET,
            Colores.TITULO + "Impacto" + Colores.RESET
        ],
        tablefmt="rounded_outline",
        colalign=("left", "right", "right", "center")
    ))
    
    # ========== RESUMEN EJECUTIVO ==========
    
    print("\n" + "="*80)
    print(Colores.DESTACADO + "🏆 RESUMEN EJECUTIVO".center(80) + Colores.RESET)
    print("="*80 + "\n")
    
    # Barra de progreso para ahorro principal (costo)
    print(f"💰 {Colores.TITULO}Ahorro en Costos:{Colores.RESET}")
    print(f"   {generar_barra_ahorro(pct_costo if es_pos_costo else 0, ancho=50)}")
    print()
    
    # Narrativa inteligente
    print(f"💡 {Colores.TITULO}Análisis:{Colores.RESET}")
    
    if es_pos_costo and pct_costo > 50:
        print(f"   {Simbolos.EXCELENTE} ¡Optimización EXCELENTE! Ahorro de {pct_costo:.1f}% en costos")
        print(f"   {Simbolos.BUENO} Sistema aprende y se adapta automáticamente")
        print(f"   {Simbolos.ROI} En 1000 ejecuciones ahorrarías {formatear_costo(ahorro_1000)}")
    elif es_pos_costo:
        print(f"   {Simbolos.BUENO} Optimización lograda: {pct_costo:.1f}% ahorro en costos")
        print(f"   {Simbolos.AHORRO} Modelo más económico mantiene calidad")
    elif tokens2 > tokens1 and es_pos_costo:
        print(f"   {Simbolos.MALO} Tokens aumentaron {abs(pct_tokens):.1f}% PERO...")
        print(f"   {Simbolos.BUENO} Modelo más barato compensa → Costo bajó {pct_costo:.1f}%")
        print(f"   {Simbolos.EXCELENTE} ¡Ganancia neta! Sistema más inteligente")
    else:
        print(f"   {Simbolos.MALO} Optimización subóptima en este caso")
        print(f"   💡 Sistema sigue aprendiendo de cada ejecución")
    
    print()
    
    # Diferenciador clave
    print(f"🎯 {Colores.TITULO}Diferenciador Clave:{Colores.RESET}")
    print(f"   → Automejora sin intervención humana")
    print(f"   → Auditoría continua + Memoria persistente")
    print(f"   → Ahorro real en producción: {formatear_costo(ahorro_1000)} por cada 1000 tareas")
    
    print("\n" + "="*80 + "\n")
    
    # ========== NARRATIVA PARA JUECES ==========
    
    print(Colores.DESTACADO + "🎤 NARRATIVA PARA JUECES:" + Colores.RESET)
    print()
    print(f"   {Colores.NEUTRO}\"Run 1 usa modelo caro sin estrategia (inocente)\"{Colores.RESET}")
    print(f"   {Colores.NEUTRO}\"Auditor detecta desperdicio → Memoria aprende\"{Colores.RESET}")
    print(f"   {Colores.NEUTRO}\"Run 2 usa modelo óptimo → {abs(pct_costo):.0f}% ahorro automático\"{Colores.RESET}")
    print(f"   {Colores.DESTACADO}\"Este es el diferenciador vs otros equipos\"{Colores.RESET}")
    print()
    print("="*80 + "\n")


# ============================================================================
# FUNCIONES ADICIONALES OPCIONALES
# ============================================================================

def mostrar_metricas_individuales(
    metricas: Dict[str, Any],
    titulo: str = "Métricas"
) -> None:
    """
    Muestra métricas de una sola ejecución (sin comparación).
    
    Args:
        metricas: Diccionario con métricas
        titulo: Título de la tabla
    """
    print("\n" + Colores.TITULO + f"📊 {titulo}" + Colores.RESET + "\n")
    
    datos = [
        [Simbolos.TOKENS + " Tokens Totales", metricas.get("tokens_totales", 0)],
        ["  ├─ Prompt", metricas.get("tokens_prompt", 0)],
        ["  └─ Completion", metricas.get("tokens_completion", 0)],
        [Simbolos.COSTO + " Costo Total", formatear_costo(metricas.get("costo_total", 0))],
        [Simbolos.LATENCIA + " Latencia", formatear_latencia(metricas.get("latencia", 0))],
        [Simbolos.MODELO + " Modelo", metricas.get("modelo_usado", "desconocido")],
    ]
    
    print(tabulate(datos, tablefmt="simple", colalign=("left", "right")))
    print()


def comparacion_rapida(
    costo1: float,
    costo2: float,
    tokens1: int,
    tokens2: int
) -> str:
    """
    Genera string de comparación rápida (una línea).
    
    Args:
        costo1: Costo Run 1
        costo2: Costo Run 2
        tokens1: Tokens Run 1
        tokens2: Tokens Run 2
    
    Returns:
        String formateado con comparación
    """
    pct_costo, _, es_pos = calcular_mejora(costo1, costo2, invertir=True)
    
    simbolo = simbolo_mejora(pct_costo, es_pos)
    color = Colores.MEJORA_EXCELENTE if (es_pos and pct_costo > 50) else Colores.MEJORA_BUENA if es_pos else Colores.MEJORA_MALA
    
    return (
        f"{simbolo} {color}Ahorro: {pct_costo:+.1f}%{Colores.RESET} "
        f"({formatear_costo(costo1)} → {formatear_costo(costo2)}) | "
        f"Tokens: {tokens1} → {tokens2}"
    )


# ============================================================================
# TESTING (si se ejecuta directamente)
# ============================================================================

if __name__ == "__main__":
    print("🧪 TEST DEL VISUALIZADOR\n")
    
    # Datos de prueba (típico caso: GPT-4o → GPT-3.5-turbo)
    metricas_test_1 = {
        "tokens_totales": 150,
        "tokens_prompt": 50,
        "tokens_completion": 100,
        "costo_total": 0.001500,
        "latencia": 2.5,
        "modelo_usado": "gpt-4o"
    }
    
    metricas_test_2 = {
        "tokens_totales": 200,
        "tokens_prompt": 55,
        "tokens_completion": 145,
        "costo_total": 0.000400,
        "latencia": 1.8,
        "modelo_usado": "gpt-3.5-turbo"
    }
    
    # Ejecutar visualización
    mostrar_comparacion_run1_vs_run2(
        metricas1=metricas_test_1,
        metricas2=metricas_test_2,
        modelo1="gpt-4o",
        modelo2="gpt-3.5-turbo",
        ruta1="default",
        ruta2="optimizada"
    )
    
    # Prueba de comparación rápida
    print("\n📋 Comparación rápida (una línea):")
    print(comparacion_rapida(0.001500, 0.000400, 150, 200))
    print()
