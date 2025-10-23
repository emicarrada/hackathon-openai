"""
src/visualizador.py
--------------------

Módulo para comparar visualmente las métricas de dos ejecuciones (Run 1 vs Run 2).

Usa la librería `rich` (si está disponible) para mostrar una tabla colorida y profesional
en la terminal. Si no está instalada, utiliza formato ANSI simple.

Autor: Brandon 🚀
Hackathon OpenAI Economist Clone
"""

from typing import Dict, Any
import math

try:
    from rich.console import Console
    from rich.table import Table
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class ComparadorRuns:
    """
    Clase encargada de comparar dos ejecuciones (Run 1 y Run 2)
    y mostrar sus diferencias visualmente en la terminal.
    """

    def __init__(self, run1: Dict[str, Any], run2: Dict[str, Any]):
        """
        Inicializa el comparador con los resultados de dos ejecuciones.

        Args:
            run1 (Dict[str, Any]): Métricas del primer run.
            run2 (Dict[str, Any]): Métricas del segundo run.
        """
        self.run1 = run1
        self.run2 = run2
        self.console = Console() if RICH_AVAILABLE else None

    def _color_text(self, text: str, color: str) -> str:
        """Devuelve texto coloreado (funciona con o sin rich)."""
        if RICH_AVAILABLE:
            return f"[{color}]{text}[/{color}]"
        # fallback ANSI simple
        ANSI_COLORS = {
            "green": "\033[92m",
            "red": "\033[91m",
            "yellow": "\033[93m",
            "reset": "\033[0m",
        }
        return f"{ANSI_COLORS.get(color, '')}{text}{ANSI_COLORS['reset']}"

    def _formato_diferencia(self, valor1: float, valor2: float, inverso: bool = False) -> str:
        """
        Calcula la diferencia porcentual entre Run 1 y Run 2.

        Args:
            valor1 (float): Valor del Run 1.
            valor2 (float): Valor del Run 2.
            inverso (bool): Si True, valores menores son mejores (ej. costo, latencia).

        Returns:
            str: Texto formateado con color y flecha.
        """
        if valor1 == 0 and valor2 == 0:
            return self._color_text("= 0%", "yellow")

        try:
            diff_abs = valor2 - valor1
            diff_pct = (diff_abs / valor1 * 100) if valor1 != 0 else 0
        except ZeroDivisionError:
            diff_pct = 0
            diff_abs = 0

        flecha = "↑" if diff_abs > 0 else "↓" if diff_abs < 0 else "→"
        color = "green" if (diff_abs < 0 and inverso) or (diff_abs > 0 and not inverso) else \
                "red" if diff_abs != 0 else "yellow"

        signo = "+" if diff_abs > 0 else ""
        return self._color_text(f"{flecha} {signo}{diff_abs:.2f} ({signo}{diff_pct:.1f}%)", color)

    def mostrar_comparacion(self) -> None:
        """
        Muestra la comparación entre Run 1 y Run 2 en una tabla visual.
        """
        if not self.run1 or not self.run2:
            print("⚠️ No hay datos suficientes para comparar.")
            return

        modelo1 = self.run1.get("modelo_usado", "desconocido")
        modelo2 = self.run2.get("modelo_usado", "desconocido")
        tokens1 = float(self.run1.get("tokens_totales", 0))
        tokens2 = float(self.run2.get("tokens_totales", 0))
        costo1 = float(self.run1.get("costo_total", 0))
        costo2 = float(self.run2.get("costo_total", 0))
        latencia1 = float(self.run1.get("latencia", 0))
        latencia2 = float(self.run2.get("latencia", 0))
        efic1 = float(self.run1.get("eficiencia", 0))
        efic2 = float(self.run2.get("eficiencia", 0))

        ahorro_pct = ((costo1 - costo2) / costo1 * 100) if costo1 > 0 else 0
        eficiencia_rel = (efic2 / efic1) if efic1 > 0 else 0

        if RICH_AVAILABLE:
            table = Table(
                title="COMPARACIÓN RUN 1 vs RUN 2",
                title_style="bold cyan",
                box=box.SIMPLE_HEAVY,
                header_style="bold white"
            )
            table.add_column("Métrica", justify="left")
            table.add_column("Run 1", justify="center")
            table.add_column("Run 2", justify="center")
            table.add_column("Diferencia", justify="center")

            table.add_row("Modelo", modelo1, modelo2,
                          self._color_text("✓ Optimizado" if modelo1 != modelo2 else "Igual", "green" if modelo1 != modelo2 else "yellow"))

            table.add_row("Tokens",
                          f"{tokens1:.0f}",
                          f"{tokens2:.0f}",
                          self._formato_diferencia(tokens1, tokens2))

            table.add_row("Costo ($)",
                          f"${costo1:.6f}",
                          f"${costo2:.6f}",
                          self._formato_diferencia(costo1, costo2, inverso=True))

            table.add_row("Latencia (s)",
                          f"{latencia1:.2f}",
                          f"{latencia2:.2f}",
                          self._formato_diferencia(latencia1, latencia2, inverso=True))

            table.add_row("Eficiencia (tok/$)",
                          f"{efic1:,.0f}",
                          f"{efic2:,.0f}",
                          self._formato_diferencia(efic1, efic2))

            self.console.print("\n")
            self.console.print(table)
            self.console.print("\n🏆 [bold green]Ahorro total:[/] {:.1f}% en costos".format(ahorro_pct))
            self.console.print("💡 [bold cyan]Sistema más eficiente:[/] x{:.1f}".format(eficiencia_rel))
            self.console.print("\n")

        else:
            # Fallback simple sin rich
            print("\n╔════════════════════════════════════════════════════════════╗")
            print("║           COMPARACIÓN RUN 1 vs RUN 2                       ║")
            print("╚════════════════════════════════════════════════════════════╝\n")

            print(f"{'Métrica':<15} | {'Run 1':<12} | {'Run 2':<12} | Diferencia")
            print("-" * 60)
            print(f"{'Modelo':<15} | {modelo1:<12} | {modelo2:<12} | ✓ Optimizado" if modelo1 != modelo2 else "Igual")
            print(f"{'Tokens':<15} | {tokens1:<12.0f} | {tokens2:<12.0f} | {tokens2 - tokens1:+.0f}")
            print(f"{'Costo ($)':<15} | {costo1:<12.6f} | {costo2:<12.6f} | {costo2 - costo1:+.6f}")
            print(f"{'Latencia (s)':<15} | {latencia1:<12.2f} | {latencia2:<12.2f} | {latencia2 - latencia1:+.2f}")
            print(f"{'Eficiencia':<15} | {efic1:<12.0f} | {efic2:<12.0f} | {efic2 - efic1:+.0f}")
            print("\n🏆 Ahorro total: {:.1f}% en costos".format(ahorro_pct))
            print("💡 Sistema más eficiente: x{:.1f}".format(eficiencia_rel))


# ----------------------------------------------------------------------
# Ejemplo de uso directo
# ----------------------------------------------------------------------
if __name__ == "__main__":
    run1 = {
        "modelo_usado": "gpt-4o",
        "tokens_totales": 128,
        "costo_total": 0.000875,
        "latencia": 1.23,
        "eficiencia": 146_000,
    }

    run2 = {
        "modelo_usado": "gpt-3.5-turbo",
        "tokens_totales": 155,
        "costo_total": 0.000108,
        "latencia": 0.95,
        "eficiencia": 1_435_000,
    }

    comparador = ComparadorRuns(run1, run2)
    comparador.mostrar_comparacion()
