# 📊 ANÁLISIS COMPLETO - VISUALIZADOR

**Fecha:** 23 oct 2025, 15:00  
**Objetivo:** Crear visualizador impresionante para demo Run 1 vs Run 2

---

## 🎯 REQUISITOS IDENTIFICADOS

### 1. INPUT DEL VISUALIZADOR

**Datos disponibles en `demo_run1_vs_run2()`:**

```python
# Run 1
metricas1 = {
    "tokens_totales": 69,
    "tokens_prompt": 30,
    "tokens_completion": 39,
    "latencia": 1.234,           # ✅ Real (ya no 0.0)
    "costo_total": 0.000465,     # ✅ USD (ya implementado)
    "modelo_usado": "gpt-4o"
}
modelo1 = "gpt-4o"
ruta1 = "default"

# Run 2
metricas2 = {
    "tokens_totales": 136,
    "tokens_prompt": 31,
    "tokens_completion": 105,
    "latencia": 0.987,
    "costo_total": 0.000173,
    "modelo_usado": "gpt-3.5-turbo"
}
modelo2 = "gpt-3.5-turbo"
ruta2 = "optimizada"
```

### 2. OUTPUT DESEADO

**Tabla comparativa visual con:**
- ✅ Colores (Run 1 = rojo/amarillo, Run 2 = verde)
- ✅ Símbolos (🔴 caro, 🟢 barato, ⚡ rápido, 🐌 lento)
- ✅ Porcentajes de ahorro destacados
- ✅ Resumen ejecutivo (ahorro total)
- ✅ Fácil de leer en terminal

---

## 🔧 TECNOLOGÍAS DISPONIBLES

### Opción A: `tabulate` ✅ (YA INSTALADO)
```python
from tabulate import tabulate

# Pros:
+ Ya instalado (no requiere pip install)
+ Sencillo y rápido
+ Compatible con todos los terminales
+ Tablas ASCII limpias

# Contras:
- Sin colores nativos (necesita colorama)
- Menos "wow factor"
```

### Opción B: `rich` ❌ (NO INSTALADO)
```python
from rich.console import Console
from rich.table import Table

# Pros:
+ Tablas MUY bonitas con colores
+ Soporte para emojis y estilos
+ Progress bars, panels, etc
+ Muy profesional

# Contras:
- NO está instalado
- Requiere agregar a requirements.txt
- Overhead extra
```

### Opción C: `colorama` ✅ (YA INSTALADO)
```python
from colorama import Fore, Back, Style, init

# Pros:
+ Ya instalado
+ Colores ANSI simples
+ Compatible Windows/Linux/Mac
+ Ligero

# Contras:
- Necesita combinar con tabulate
- Más manual
```

### ✅ DECISIÓN: `tabulate` + `colorama`
**Razón:** Ya instalados, rápido de implementar, suficiente para impresionar

---

## 📐 DISEÑO DE LA TABLA

### Layout Propuesto:

```
╔══════════════════════════════════════════════════════════════╗
║         ⚡ Run 1 vs Run 2 - Automejora Demostrada          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Métrica          │  Run 1 (Inocente)  │  Run 2 (Optimizado)  │  Mejora   ║
║  ────────────────────────────────────────────────────────────║
║  🤖 Modelo        │  gpt-4o           │  gpt-3.5-turbo      │  ✅       ║
║  📦 Tokens        │  69               │  136                │  -97%     ║
║  💰 Costo (USD)   │  $0.000465        │  $0.000173          │  🎉 62.8% ║
║  ⚡ Latencia      │  1.234s           │  0.987s             │  +0.247s  ║
║  🛣️  Ruta          │  default          │  optimizada         │  ✅       ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  🏆 AHORRO TOTAL: 62.8% en costos                           ║
║  💡 Tokens aumentaron pero COSTO bajó → ¡Ganancia neta!    ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🎨 ESQUEMA DE COLORES

### Por Métrica:

```python
COLORES = {
    "run1": Fore.RED,      # Rojo = caro/lento
    "run2": Fore.GREEN,    # Verde = barato/rápido
    "mejora_positiva": Fore.GREEN + Style.BRIGHT,
    "mejora_negativa": Fore.YELLOW,
    "neutro": Fore.CYAN,
    "titulo": Fore.MAGENTA + Style.BRIGHT,
    "reset": Style.RESET_ALL
}
```

### Por Valor:

- **Costo alto (gpt-4o):** 🔴 Rojo
- **Costo bajo (gpt-3.5-turbo):** 🟢 Verde
- **Ahorro >50%:** 🎉 Verde brillante + negrita
- **Ahorro 0-50%:** ✅ Verde normal
- **Aumento (negativo):** ⚠️ Amarillo

---

## 📝 FUNCIONES A IMPLEMENTAR

### Función Principal:

```python
def mostrar_comparacion_run1_vs_run2(
    metricas1: dict,
    metricas2: dict,
    modelo1: str,
    modelo2: str,
    ruta1: str = "default",
    ruta2: str = "optimizada"
) -> None:
    """
    Muestra tabla comparativa visual entre Run 1 y Run 2.
    
    Args:
        metricas1: Diccionario con métricas de Run 1
        metricas2: Diccionario con métricas de Run 2
        modelo1: Modelo usado en Run 1 (ej: "gpt-4o")
        modelo2: Modelo usado en Run 2 (ej: "gpt-3.5-turbo")
        ruta1: Ruta tomada en Run 1 (default)
        ruta2: Ruta tomada en Run 2 (optimizada)
    
    Returns:
        None (imprime en consola)
    """
```

### Funciones Auxiliares:

```python
def calcular_mejora(valor1: float, valor2: float) -> tuple:
    """
    Calcula mejora porcentual y absoluta.
    
    Returns:
        (mejora_porcentual, mejora_absoluta, es_positivo)
    """

def formatear_costo(costo: float) -> str:
    """Formatea costo en USD con 6 decimales."""

def formatear_latencia(latencia: float) -> str:
    """Formatea latencia en segundos con 3 decimales."""

def simbolo_mejora(porcentaje: float, invertir: bool = False) -> str:
    """
    Retorna símbolo según mejora:
    - > 50%: 🎉
    - > 0%: ✅
    - < 0%: ⚠️
    """

def colorear_texto(texto: str, color: str) -> str:
    """Aplica color ANSI al texto."""
```

---

## 🔌 INTEGRACIÓN CON SISTEMA ACTUAL

### Ubicación en el código:

**Archivo:** `src/agente.py`  
**Método:** `demo_run1_vs_run2()`  
**Línea:** ~260 (después de calcular ahorros)

### Cambio necesario:

```python
# ANTES (líneas 254-266):
print(f"\n🎯 Impacto de la automejora:")
print(f"   Run 1 (inocente): {tokens1} tokens, ${costo1:.6f}, {latencia1:.3f}s con {modelo1}")
print(f"   Run 2 (optimizado): {tokens2} tokens, ${costo2:.6f}, {latencia2:.3f}s con {modelo2}")
print(f"\n   💰 Ahorro en COSTOS: ${ahorro_costo:.6f} ({porcentaje_ahorro_costo:.1f}%)")
print(f"   📦 Ahorro en tokens: {ahorro_tokens} ({porcentaje_ahorro_tokens:.1f}%)")
print(f"   ⚡ Diferencia latencia: {ahorro_latencia:.3f}s")

# DESPUÉS:
from src.visualizador import mostrar_comparacion_run1_vs_run2

mostrar_comparacion_run1_vs_run2(
    metricas1=metricas1,
    metricas2=metricas2,
    modelo1=modelo1,
    modelo2=modelo2,
    ruta1=resultado1.get('ruta', 'default'),
    ruta2=resultado2.get('ruta', 'optimizada')
)
```

---

## 📦 ESTRUCTURA DE ARCHIVOS

```
src/
├── visualizador.py  ← NUEVO archivo
│   ├── mostrar_comparacion_run1_vs_run2()
│   ├── calcular_mejora()
│   ├── formatear_costo()
│   ├── formatear_latencia()
│   ├── simbolo_mejora()
│   └── colorear_texto()
│
├── agente.py  ← MODIFICAR (importar + llamar visualizador)
└── ...
```

---

## 🧪 CASOS DE PRUEBA

### Caso 1: Ahorro positivo (típico)
```python
metricas1 = {
    "tokens_totales": 150,
    "costo_total": 0.001500,
    "latencia": 2.0,
    "modelo_usado": "gpt-4o"
}

metricas2 = {
    "tokens_totales": 200,
    "costo_total": 0.000400,
    "latencia": 1.5,
    "modelo_usado": "gpt-3.5-turbo"
}

# Esperado:
# - Costo: ✅ 73.3% ahorro (verde)
# - Tokens: ⚠️ -33% (amarillo - aumentó)
# - Latencia: ✅ +0.5s (verde - más rápido)
```

### Caso 2: Ahorro negativo (edge case)
```python
metricas1 = {
    "tokens_totales": 100,
    "costo_total": 0.000100,
    "latencia": 1.0,
    "modelo_usado": "gpt-3.5-turbo"
}

metricas2 = {
    "tokens_totales": 150,
    "costo_total": 0.000150,
    "latencia": 1.2,
    "modelo_usado": "gpt-4o"
}

# Esperado:
# - Costo: ⚠️ -50% (rojo - empeoró)
# - Tokens: ⚠️ -50% (amarillo)
# - Latencia: ⚠️ -0.2s (amarillo - más lento)
```

### Caso 3: Latencia muy baja (<1ms)
```python
metricas1 = {"latencia": 0.0, ...}
metricas2 = {"latencia": 0.0, ...}

# Esperado:
# - Latencia: "0.000s" (gris - no medido/muy rápido)
```

---

## ⚡ OPTIMIZACIONES

### Opcional: Gráfico ASCII de barras

```python
def generar_barra_ahorro(porcentaje: float, ancho: int = 30) -> str:
    """
    Genera barra de progreso ASCII.
    
    Ejemplo:
    73.3% → [████████████████░░░░░░░░] 73.3%
    """
    lleno = int((porcentaje / 100) * ancho)
    vacio = ancho - lleno
    barra = "█" * lleno + "░" * vacio
    return f"[{barra}] {porcentaje:.1f}%"
```

### Opcional: Resumen ejecutivo

```python
def mostrar_resumen_ejecutivo(ahorro_costo: float, ahorro_tokens: float):
    """
    Muestra resumen con recomendación para jueces.
    
    Ejemplo:
    ╔════════════════════════════════════╗
    ║  🏆 RESUMEN EJECUTIVO             ║
    ╠════════════════════════════════════╣
    ║  Ahorro en costos:  62.8%         ║
    ║  Modelo optimizado: ✅            ║
    ║  Narrativa:                       ║
    ║  "Sistema aprende y se optimiza   ║
    ║   automáticamente → 62% ahorro"   ║
    ╚════════════════════════════════════╝
    """
```

---

## 🎬 EJEMPLO DE OUTPUT FINAL

```bash
$ python demo_hackathon.py

# ... (runs anteriores) ...

╔══════════════════════════════════════════════════════════════════╗
║            ⚡ COMPARACIÓN: Run 1 vs Run 2                        ║
║               Automejora del Sistema Demostrada                  ║
╠══════════════════════════════════════════════════════════════════╣

┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Métrica      ┃ Run 1 (Inocente) ┃ Run 2 (Optimizado)┃ Mejora    ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ 🤖 Modelo    │ gpt-4o           │ gpt-3.5-turbo     │ ✅        │
│ 📦 Tokens    │ 69               │ 136               │ ⚠️ -97%   │
│ 💰 Costo     │ $0.000465        │ $0.000173         │ 🎉 62.8%  │
│ ⚡ Latencia  │ 1.234s           │ 0.987s            │ ✅ +0.247s│
│ 🛣️ Ruta      │ default          │ optimizada        │ ✅        │
└──────────────┴───────────────────┴───────────────────┴───────────┘

╔══════════════════════════════════════════════════════════════════╗
║  🏆 RESULTADO FINAL                                              ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Ahorro en costos:  [████████████████░░░░] 62.8%               ║
║                                                                  ║
║  💡 Explicación:                                                ║
║  Tokens aumentaron de 69 a 136 (-97%) PERO...                  ║
║  Modelo más barato (gpt-3.5-turbo) → Costo bajó 62.8%         ║
║  ✅ GANANCIA NETA: Sistema más inteligente                     ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

🎤 NARRATIVA PARA JUECES:
   "Run 1 usó modelo caro sin estrategia"
   "Auditor detectó desperdicio → Memoria aprendió"
   "Run 2 usó modelo óptimo → 62.8% ahorro automático"
   "Este es el diferenciador vs otros equipos"
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### Fase 1: Core (30 min)
- [ ] Crear `src/visualizador.py`
- [ ] Implementar `mostrar_comparacion_run1_vs_run2()`
- [ ] Implementar funciones auxiliares
- [ ] Agregar imports en `src/agente.py`
- [ ] Reemplazar prints por llamada a visualizador

### Fase 2: Estilo (15 min)
- [ ] Agregar colores con colorama
- [ ] Agregar símbolos (🎉✅⚠️)
- [ ] Formatear números correctamente
- [ ] Probar en terminal

### Fase 3: Extras (15 min - Opcional)
- [ ] Barra de progreso ASCII
- [ ] Resumen ejecutivo
- [ ] Manejo de edge cases
- [ ] Tests

---

## 🚀 SIGUIENTE PASO

**CREAR:** `src/visualizador.py` con todas las funciones
**MODIFICAR:** `src/agente.py` para usar el visualizador
**PROBAR:** `python demo_hackathon.py`

**Tiempo estimado:** 45-60 minutos

---

**¿Proceder con implementación?** ✅
