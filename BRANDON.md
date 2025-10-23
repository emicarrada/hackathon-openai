# 🎯 BRANDON - TAREAS ESPECÍFICAS HACKATHON

## 📋 TU MISIÓN

**Rol:** Experto en Métricas y Visualización  
**Objetivo:** Mejorar el sistema de métricas y hacer la demo visualmente impactante  
**Tiempo estimado:** 2 horas  
**Rama de trabajo:** `brandon/metricas-viz`

---

## ✅ ANTES DE EMPEZAR

### 1. Rebase con main

```bash
# Guardar tu trabajo actual
git stash

# Actualizar desde main
git checkout main
git pull origin main

# Crear tu rama de trabajo
git checkout -b brandon/metricas-viz

# Recuperar trabajo anterior (si lo necesitas)
git stash pop
```

### 2. Verificar que el sistema funciona

```bash
# Configurar API Key
export OPENAI_API_KEY="tu_api_key_aqui"

# Probar el sistema
python demo_hackathon.py --rapida
```

**Output esperado:** Ver Run 1 vs Run 2 funcionando correctamente.

### 3. Leer documentación

- [ ] `GUIA_COMPLETA_6_NODOS.md` - Entender arquitectura completa
- [ ] `src/nodos/evaluar_contador.py` - Tu nodo principal a mejorar
- [ ] `METRICAS_PROPUESTAS.md` - 30+ ideas de métricas

---

## 🎯 TAREAS PRIORITARIAS (EN ORDEN)

### TAREA 1: Mejorar `evaluar_contador.py` (45 min)

**Archivo:** `src/nodos/evaluar_contador.py`

#### Estado Actual

```python
def evaluar_con_contador(state: dict) -> dict:
    # Solo captura tokens básicos
    metricas_ejecucion = {
        "tokens_totales": usage.total_tokens,
        "tokens_prompt": usage.prompt_tokens,
        "tokens_completion": usage.completion_tokens,
        "modelo_usado": state.get("modelo_a_usar", "desconocido"),
        "latencia": 0.0  # Placeholder
    }
```

#### Lo que DEBES Agregar

**1. Captura de latencia real:**

```python
import time

# En ejecutar_tarea.py, agregar:
state["tiempo_inicio"] = time.time()

# En evaluar_contador.py, calcular:
latencia = time.time() - state.get("tiempo_inicio", 0)
```

**2. Cálculo de costos:**

```python
# Precios por 1M tokens (consultar docs OpenAI)
PRECIOS = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60}
}

def calcular_costo(modelo, tokens_input, tokens_output):
    precios = PRECIOS.get(modelo, {"input": 0, "output": 0})
    costo_input = (tokens_input / 1_000_000) * precios["input"]
    costo_output = (tokens_output / 1_000_000) * precios["output"]
    return costo_input + costo_output
```

**3. Tokens por segundo:**

```python
tokens_por_segundo = tokens_totales / latencia if latencia > 0 else 0
```

**4. Eficiencia (tokens/dólar):**

```python
tokens_por_dolar = tokens_totales / costo_total if costo_total > 0 else 0
```

#### Cómo Usar Copilot para Esto

**Prompt para Copilot:**

```
Mejora la función evaluar_con_contador en src/nodos/evaluar_contador.py para:

1. Calcular latencia real usando time.time() del estado
2. Calcular costo en dólares usando estos precios:
   - GPT-4o: $2.50 input, $10.00 output (por 1M tokens)
   - GPT-3.5-turbo: $0.50 input, $1.50 output
   - GPT-4o-mini: $0.15 input, $0.60 output
3. Calcular tokens_por_segundo
4. Calcular eficiencia (tokens_por_dolar)
5. Mantener la estructura del dict metricas_ejecucion
6. Añadir docstrings y comentarios claros

El código debe ser limpio, usar type hints y manejar errores.
```

#### Resultado Esperado

```python
metricas_ejecucion = {
    "tokens_totales": 128,
    "tokens_prompt": 75,
    "tokens_completion": 53,
    "modelo_usado": "gpt-4o",
    "latencia": 1.23,  # segundos
    "costo_total": 0.000875,  # dólares
    "tokens_por_segundo": 104.0,
    "eficiencia": 146285.7  # tokens/$
}
```

---

### TAREA 2: Crear Visualizador de Comparación (45 min)

**Nuevo archivo:** `src/visualizador.py`

#### Qué Debe Hacer

Crear un módulo que compare Run 1 vs Run 2 visualmente en la terminal.

#### Prompt para Copilot

```
Crea un archivo src/visualizador.py con una clase ComparadorRuns que:

1. Reciba dos diccionarios de métricas (run1 y run2)
2. Tenga un método mostrar_comparacion() que imprima:
   - Tabla comparativa con rich o tabulate
   - Modelo usado en cada run
   - Tokens consumidos (con diferencia)
   - Costo en dólares (con diferencia y % ahorro)
   - Latencia (con diferencia)
   - Eficiencia tokens/$

3. Use colores:
   - Verde para mejoras
   - Rojo para empeoramientos
   - Amarillo para neutral

4. Calcule y muestre % de ahorro total

Usa la librería 'rich' para tablas bonitas.
Si no está instalada, usa print con formato ANSI.

Incluye:
- Type hints completos
- Docstrings
- Ejemplo de uso en __main__
```

#### Ejemplo de Output Esperado

```
╔════════════════════════════════════════════════════════════╗
║           COMPARACIÓN RUN 1 vs RUN 2                      ║
╚════════════════════════════════════════════════════════════╝

┌─────────────────┬──────────────┬──────────────┬─────────────┐
│ Métrica         │ Run 1        │ Run 2        │ Diferencia  │
├─────────────────┼──────────────┼──────────────┼─────────────┤
│ Modelo          │ gpt-4o       │ gpt-3.5-turbo│ ✓ Optimizado│
│ Tokens          │ 128          │ 155          │ +27 (21%)   │
│ Costo           │ $0.000875    │ $0.000108    │ ↓ -87.7%    │
│ Latencia        │ 1.23s        │ 0.95s        │ ↓ -0.28s    │
│ Eficiencia      │ 146K tok/$   │ 1435K tok/$  │ ↑ +882%     │
└─────────────────┴──────────────┴──────────────┴─────────────┘

🏆 AHORRO TOTAL: 87.7% en costos
💡 Sistema aprendió a usar modelo 13x más eficiente
```

#### Integración en demo_hackathon.py

Agregar al final de `demo_run1_vs_run2()`:

```python
from src.visualizador import ComparadorRuns

comparador = ComparadorRuns(metricas1, metricas2)
comparador.mostrar_comparacion()
```

---

### TAREA 3: Gráfico de Ahorro (30 min - OPCIONAL)

**Nuevo archivo:** `src/graficos.py`

#### Qué Debe Hacer

Crear un gráfico de barras comparando Run 1 vs Run 2.

#### Prompt para Copilot

```
Crea src/graficos.py con una función generar_grafico_ahorro() que:

1. Reciba metricas_run1 y metricas_run2
2. Use matplotlib para crear gráfico de barras
3. Muestre comparación de:
   - Tokens consumidos
   - Costo en dólares (multiplicar por 1000 para visualizar)
   - Latencia

4. Use colores distintivos (rojo Run 1, verde Run 2)
5. Incluya título, leyenda y etiquetas
6. Guarde imagen como 'comparacion_runs.png'
7. Muestre el % de ahorro en el título

Si matplotlib no está disponible, usar plotext (terminal).

Incluye ejemplo de uso.
```

#### Integración

En `demo_hackathon.py`, después de la comparación:

```python
from src.graficos import generar_grafico_ahorro

generar_grafico_ahorro(metricas1, metricas2)
print("📊 Gráfico guardado en comparacion_runs.png")
```

---

## 🧪 TESTING

Crear `tests/test_metricas.py`:

```python
def test_calcular_costo():
    """Verifica cálculo de costos"""
    costo = calcular_costo("gpt-4o", 1000, 500)
    assert costo > 0
    # gpt-4o: (1000/1M * 2.5) + (500/1M * 10) = 0.0075

def test_comparador():
    """Verifica comparador funciona"""
    from src.visualizador import ComparadorRuns
    
    run1 = {"tokens_totales": 100, "costo_total": 0.001}
    run2 = {"tokens_totales": 50, "costo_total": 0.0005}
    
    comp = ComparadorRuns(run1, run2)
    comp.mostrar_comparacion()  # No debe crashear
```

---

## 📤 SUBIR TU TRABAJO

```bash
# 1. Verificar cambios
git status

# 2. Agregar archivos
git add src/nodos/evaluar_contador.py
git add src/visualizador.py
git add src/graficos.py  # si lo hiciste
git add tests/test_metricas.py

# 3. Commit
git commit -m "Mejorar métricas: latencia, costos, visualización

- Calcular latencia real en evaluar_contador.py
- Agregar cálculo de costos por modelo
- Crear visualizador de comparación Run 1 vs Run 2
- Gráficos matplotlib para presentación
- Tests de métricas"

# 4. Push a tu rama
git push origin brandon/metricas-viz

# 5. Avisar a Carrada en Discord/Slack
```

---

## 🎤 NARRATIVA PARA TU PARTE

Cuando expliques en la presentación:

> **"Implementé un sistema de métricas completo que no solo cuenta tokens, sino que calcula costos reales en dólares, latencia y eficiencia. La visualización muestra claramente cómo el sistema pasa de gastar $0.000875 en Run 1 a solo $0.000108 en Run 2, un ahorro del 87.7%. Esto escalado a millones de requests significa ahorros masivos."**

---

## 🆘 SI TIENES PROBLEMAS

### Problema: Copilot no genera código correcto

**Solución:** 
1. Lee primero `GUIA_COMPLETA_6_NODOS.md` (Sección Nodo 4)
2. Mira el código actual en `src/nodos/evaluar_contador.py`
3. Pide a Copilot que "mejore el código existente" en vez de "crear desde cero"

### Problema: No entiendo el flujo

**Solución:**
1. Ejecuta `python demo_hackathon.py --rapida`
2. Lee el output paso a paso
3. Abre `src/agente.py` línea 87-95 (flujo de nodos)

### Problema: Tests fallan

**Solución:**
```bash
# Ver qué falla exactamente
pytest tests/test_metricas.py -v

# Ejecutar solo un test
pytest tests/test_metricas.py::test_calcular_costo -v
```

---

## ⏰ CHECKLIST FINAL

Antes de hacer push, verifica:

- [ ] `evaluar_contador.py` tiene latencia real
- [ ] Costos calculados correctamente para 3 modelos
- [ ] `visualizador.py` muestra tabla comparativa bonita
- [ ] Tests pasan: `pytest tests/test_metricas.py`
- [ ] Demo funciona: `python demo_hackathon.py`
- [ ] Código tiene docstrings y type hints
- [ ] Commit message es descriptivo

---

## 🏆 IMPACTO DE TU TRABAJO

Tu implementación permite:
- ✅ **Demostrar ahorro real en $$$** (no solo tokens)
- ✅ **Visualización profesional** para jueces
- ✅ **Métricas completas** para análisis técnico
- ✅ **Presentación impactante** con gráficos

**¡Tu parte es CLAVE para ganar!** 🚀

---

## 📚 RECURSOS

- **Pricing OpenAI:** https://openai.com/api/pricing/
- **Rich (tablas):** https://rich.readthedocs.io/
- **Matplotlib:** https://matplotlib.org/stable/gallery/

¡Éxito Brandon! 💪
