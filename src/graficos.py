"""
src/graficos.py

Módulo que genera un gráfico de barras comparando métricas entre Run 1 y Run 2.
Diseñado para visualizar mejoras en tokens, costo y latencia de forma clara.
"""

from typing import Dict
import os

def generar_grafico_ahorro(metricas_run1: Dict[str, float], metricas_run2: Dict[str, float]) -> None:
    """
    Genera un gráfico de barras comparando Run 1 vs Run 2.

    Parámetros:
        metricas_run1 (Dict[str, float]): Métricas del primer run (tokens, costo, latencia).
        metricas_run2 (Dict[str, float]): Métricas del segundo run (tokens, costo, latencia).

    El gráfico muestra:
        - Tokens consumidos
        - Costo (multiplicado x1000 para mejor visualización)
        - Latencia (segundos)

    Si matplotlib no está disponible, usa plotext para renderizar en terminal.
    Guarda el gráfico como 'comparacion_runs.png'.
    """

    # Datos esperados
    tokens1 = metricas_run1.get("tokens_totales", 0)
    tokens2 = metricas_run2.get("tokens_totales", 0)
    costo1 = metricas_run1.get("costo_usd", 0)
    costo2 = metricas_run2.get("costo_usd", 0)
    latencia1 = metricas_run1.get("latencia", 0)
    latencia2 = metricas_run2.get("latencia", 0)

    # Calcular % de ahorro en costo
    ahorro = 0
    if costo1 > 0:
        ahorro = ((costo1 - costo2) / costo1) * 100

    categorias = ["Tokens", "Costo (x1000)", "Latencia (s)"]
    valores_run1 = [tokens1, costo1 * 1000, latencia1]
    valores_run2 = [tokens2, costo2 * 1000, latencia2]

    try:
        import matplotlib.pyplot as plt

        x = range(len(categorias))
        width = 0.35

        fig, ax = plt.subplots()
        ax.bar([p - width/2 for p in x], valores_run1, width, label='Run 1', color='red')
        ax.bar([p + width/2 for p in x], valores_run2, width, label='Run 2', color='green')

        ax.set_xticks(list(x))
        ax.set_xticklabels(categorias)
        ax.set_ylabel('Valores normalizados')
        ax.set_title(f"Comparación Run 1 vs Run 2 — Ahorro: {ahorro:.1f}%")
        ax.legend()

        plt.tight_layout()
        plt.savefig("comparacion_runs.png", dpi=150)
        plt.close()
        print("📊 Gráfico guardado como 'comparacion_runs.png'")

    except ImportError:
        # Fallback: usar plotext (gráfico en terminal)
        try:
            import plotext as plt

            plt.simple_bar(categorias, valores_run1, label="Run 1", color="red")
            plt.simple_bar(categorias, valores_run2, label="Run 2", color="green")

            plt.title(f"Comparación Run 1 vs Run 2 — Ahorro: {ahorro:.1f}%")
            plt.legend(True)
            plt.show()
        except ImportError:
            print("⚠️  Ni matplotlib ni plotext están instalados. No se puede generar gráfico.")


# -------------------------------------------------------------------
# Ejemplo de uso
# -------------------------------------------------------------------
if __name__ == "__main__":
    metricas_run1 = {
        "tokens_totales": 128,
        "costo_usd": 0.000875,
        "latencia": 1.23
    }

    metricas_run2 = {
        "tokens_totales": 155,
        "costo_usd": 0.000108,
        "latencia": 0.95
    }

    generar_grafico_ahorro(metricas_run1, metricas_run2)
