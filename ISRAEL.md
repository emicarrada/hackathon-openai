# 🎯 ISRAEL - TAREAS ESPECÍFICAS HACKATHON

## 📋 TU MISIÓN

**Rol:** Experto en Prompts y Optimización de IA  
**Objetivo:** Mejorar prompts del sistema y agregar tipos de tarea  
**Tiempo estimado:** 2 horas  
**Rama de trabajo:** `israel/prompts-optimizacion`

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
git checkout -b israel/prompts-optimizacion

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
- [ ] `src/nodos/recibir_tarea.py` - Clasificación de tareas
- [ ] `src/nodos/auditor_feedback.py` - Prompts del auditor
- [ ] `src/nodos/ejecutar_tarea.py` - Ejecución de tareas

---

## 🎯 TAREAS PRIORITARIAS (EN ORDEN)

### TAREA 1: Mejorar Clasificación de Tareas (45 min)

**Archivo:** `src/nodos/recibir_tarea.py`

#### Estado Actual

```python
# Clasificación básica por keywords
if any(word in tarea_lower for word in ["resume", "resumen", "resumir"]):
    tipo_tarea = "resumen"
elif any(word in tarea_lower for word in ["traduce", "traducir", "translate"]):
    tipo_tarea = "traduccion"
# ... solo 5 tipos
```

#### Lo que DEBES Agregar

**1. Más tipos de tarea:**

```python
TIPOS_TAREA = {
    "resumen": ["resume", "resumen", "resumir", "sintetiza", "sinopsis"],
    "traduccion": ["traduce", "traducir", "translate", "translation"],
    "clasificacion": ["clasifica", "categoriza", "classify", "category"],
    "extraccion": ["extrae", "extract", "obtén", "encuentra"],
    "analisis": ["analiza", "analyze", "evalúa", "assess"],  # NUEVO
    "codigo": ["codigo", "code", "programa", "script", "debug"],  # NUEVO
    "creatividad": ["escribe", "crea", "genera", "inventa", "historia"],  # NUEVO
    "qa": ["pregunta", "responde", "question", "answer", "qué es"],  # NUEVO
    "comparacion": ["compara", "compare", "diferencias", "vs"],  # NUEVO
    "general": []  # Fallback
}
```

**2. Clasificación más inteligente:**

En lugar de solo keywords, usar un mini-LLM para clasificar (opcional pero impresionante):

```python
def clasificar_con_llm(tarea: str) -> str:
    """
    Usa GPT-4o-mini (barato) para clasificar tarea con alta precisión.
    """
    prompt = f"""Clasifica esta tarea en UNA de estas categorías:
- resumen
- traduccion
- clasificacion
- extraccion
- analisis
- codigo
- creatividad
- qa
- comparacion
- general

Tarea: "{tarea}"

Responde SOLO con la categoría (una palabra, minúsculas):"""
    
    # Llamar a OpenAI con gpt-4o-mini
    # ...
    return categoria
```

#### Prompt para Copilot

```
Mejora src/nodos/recibir_tarea.py para:

1. Agregar estos nuevos tipos de tarea:
   - analisis: para análisis profundos
   - codigo: para generación/debugging de código
   - creatividad: para escritura creativa
   - qa: para preguntas y respuestas
   - comparacion: para comparar conceptos

2. Ampliar las keywords para cada tipo (mínimo 5 por tipo)

3. OPCIONAL: Agregar función clasificar_con_llm() que:
   - Use gpt-4o-mini para clasificar con IA
   - Solo se active si keywords no dan match claro
   - Tenga fallback a clasificación por keywords
   - Sea eficiente (máximo 50 tokens)

4. Agregar logging para debug:
   print(f"🔍 Clasificando: {tarea[:50]}...")
   print(f"✓ Tipo detectado: {tipo_tarea}")

5. Mantener compatibilidad con código existente

Incluye docstrings, type hints y manejo de errores.
```

#### Resultado Esperado

```python
# Tareas que antes eran "general" ahora se clasifican correctamente
"Genera un script Python" → "codigo"
"Compara Python vs JavaScript" → "comparacion"
"Analiza este dataset" → "analisis"
"Escribe un poema" → "creatividad"
```

---

### TAREA 2: Optimizar Prompt del Auditor (45 min)

**Archivo:** `src/nodos/auditor_feedback.py`

#### Estado Actual

```python
prompt_auditor = f"""Eres un Auditor de Eficiencia de APIs de IA.

Analiza esta ejecución:
- Tipo de tarea: {tipo_tarea}
- Modelo usado: {modelo_usado}
- Tokens consumidos: {tokens_totales}

Contexto de costos:
- GPT-4o: modelo más caro (~10x GPT-3.5-turbo)
- GPT-3.5-turbo: modelo económico, buen rendimiento
- GPT-4o-mini: modelo ultra-económico

Evalúa si el modelo usado fue eficiente para esta tarea.
..."""
```

#### Lo que DEBES Mejorar

**1. Agregar ejemplos de referencia por tipo de tarea:**

```python
BENCHMARKS_POR_TIPO = {
    "resumen": {
        "modelo_optimo": "gpt-3.5-turbo",
        "tokens_esperados": 200,
        "razon": "Tareas de resumen no requieren razonamiento complejo"
    },
    "codigo": {
        "modelo_optimo": "gpt-4o",
        "tokens_esperados": 500,
        "razon": "Generación de código requiere precisión"
    },
    "analisis": {
        "modelo_optimo": "gpt-4o",
        "tokens_esperados": 800,
        "razon": "Análisis profundo requiere capacidad de razonamiento"
    },
    # ... resto de tipos
}
```

**2. Prompt más específico:**

```python
prompt_auditor = f"""Eres un Auditor Senior de Eficiencia en APIs de IA.

CONTEXTO DE LA EJECUCIÓN:
- Tipo de tarea: {tipo_tarea}
- Modelo usado: {modelo_usado}
- Tokens consumidos: {tokens_totales}
- Costo estimado: ${costo_estimado}

BENCHMARK PARA "{tipo_tarea}":
- Modelo óptimo: {benchmark["modelo_optimo"]}
- Tokens esperados: {benchmark["tokens_esperados"]}
- Razón: {benchmark["razon"]}

TABLA DE COSTOS (por 1M tokens):
┌──────────────┬────────┬─────────┐
│ Modelo       │ Input  │ Output  │
├──────────────┼────────┼─────────┤
│ GPT-4o       │ $2.50  │ $10.00  │
│ GPT-3.5      │ $0.50  │ $1.50   │
│ GPT-4o-mini  │ $0.15  │ $0.60   │
└──────────────┴────────┴─────────┘

INSTRUCCIONES:
1. Compara el modelo usado con el benchmark
2. Analiza si hubo desperdicio de recursos
3. Considera calidad vs costo
4. Responde en JSON exacto:

{{
    "requiere_optimizacion": true/false,
    "analisis": "explicación técnica en 1-2 líneas",
    "recomendacion": "modelo_recomendado" o "ninguna"
}}

IMPORTANTE:
- Si modelo usado == modelo óptimo → requiere_optimizacion: false
- Si usaste GPT-4o para tarea simple → requiere_optimizacion: true
- Si usaste GPT-3.5 para tarea compleja → revisar calidad antes
"""
```

#### Prompt para Copilot

```
Mejora src/nodos/auditor_feedback.py para:

1. Crear diccionario BENCHMARKS_POR_TIPO con:
   - Modelo óptimo por tipo de tarea
   - Tokens esperados
   - Razón técnica

2. Mejorar prompt del auditor para que:
   - Compare con benchmark específico
   - Muestre tabla de costos clara
   - Dé análisis más técnico y preciso
   - Use el benchmark en su evaluación

3. Agregar lógica de "zona gris":
   - Si diferencia de costo < 20% → no optimizar (no vale la pena)
   - Si tokens > 2x esperados → investigar por qué

4. Mejor manejo de JSON:
   - Validar que todos los campos existan
   - Defaults sensatos si parsing falla
   - Logging de errores

5. Agregar comentarios explicativos

Mantén compatibilidad con el resto del sistema.
```

#### Resultado Esperado

El auditor ahora da feedback más específico:

```
ANTES:
"El uso de GPT-4o para esta tarea no es eficiente."

DESPUÉS:
"Tarea 'resumen' detectada. Benchmark: gpt-3.5-turbo (200 tokens).
Usaste gpt-4o (128 tokens) = 10x más caro sin beneficio de calidad.
Recomendación: Cambiar a gpt-3.5-turbo para ahorrar 90% en costos."
```

---

### TAREA 3: Mejorar Ejecución de Tareas (30 min)

**Archivo:** `src/nodos/ejecutar_tarea.py`

#### Estado Actual

```python
# Prompt muy genérico
mensaje_sistema = "Eres un asistente útil."
```

#### Lo que DEBES Mejorar

**Prompts especializados por tipo de tarea:**

```python
PROMPTS_SISTEMA = {
    "resumen": """Eres un experto en síntesis de información.
Tu objetivo: resumir contenido de forma clara y concisa.
Estilo: Puntos clave, máximo detalle en mínimas palabras.""",
    
    "codigo": """Eres un programador senior experto.
Tu objetivo: generar código limpio, eficiente y bien documentado.
Estilo: Best practices, type hints, comentarios claros.""",
    
    "analisis": """Eres un analista senior con pensamiento crítico.
Tu objetivo: análisis profundo con insights accionables.
Estilo: Estructurado, basado en datos, conclusiones claras.""",
    
    "creatividad": """Eres un escritor creativo profesional.
Tu objetivo: contenido original, engaging y bien escrito.
Estilo: Narrativo, emotivo, con buen ritmo.""",
    
    # ... resto de tipos
}
```

#### Prompt para Copilot

```
Mejora src/nodos/ejecutar_tarea.py para:

1. Crear diccionario PROMPTS_SISTEMA con pe llamerompts especializados para:
   - resumen
   - traduccion
   - codigo
   - analisis
   - creatividad
   - qa
   - comparacion
   - clasificacion
   - extraccion
   - general (fallback)

2. Seleccionar prompt según tipo_tarea del estado

3. Agregar parámetros óptimos por tipo:
   - resumen: temperature=0.3 (más determinístico)
   - creatividad: temperature=0.9 (más creativo)
   - codigo: temperature=0.2 (muy determinístico)
   - general: temperature=0.7 (balanceado)

4. Mejorar mensajes de usuario:
   - Más contexto
   - Instrucciones claras
   - Formato de salida esperado

5. Mantener max_tokens y estructura actual

Documenta por qué cada prompt es óptimo para su tipo.
```

#### Resultado Esperado

```python
# Antes: mismo prompt genérico para todo
# Después: prompt optimizado por tipo

# Para resumen:
sistema = "Eres un experto en síntesis..."
temperature = 0.3

# Para creatividad:
sistema = "Eres un escritor creativo..."
temperature = 0.9
```

---

## 🧪 TESTING

Crear `tests/test_prompts.py`:

```python
def test_clasificacion_extendida():
    """Verifica nuevos tipos de tarea"""
    from src.nodos.recibir_tarea import recibir_tarea
    
    state = {"tarea_descripcion": "Escribe un poema sobre IA"}
    resultado = recibir_tarea(state)
    assert resultado["tipo_tarea"] == "creatividad"
    
    state = {"tarea_descripcion": "Genera un script Python"}
    resultado = recibir_tarea(state)
    assert resultado["tipo_tarea"] == "codigo"

def test_benchmarks_auditor():
    """Verifica que benchmarks existen"""
    from src.nodos.auditor_feedback import BENCHMARKS_POR_TIPO
    
    assert "resumen" in BENCHMARKS_POR_TIPO
    assert "codigo" in BENCHMARKS_POR_TIPO
    assert "modelo_optimo" in BENCHMARKS_POR_TIPO["resumen"]

def test_prompts_especializados():
    """Verifica prompts por tipo"""
    from src.nodos.ejecutar_tarea import PROMPTS_SISTEMA
    
    assert len(PROMPTS_SISTEMA) >= 9
    assert "resumen" in PROMPTS_SISTEMA
    assert len(PROMPTS_SISTEMA["resumen"]) > 50  # Prompt decente
```

---

## 🎨 BONUS: Demo de Tipos de Tarea

Crear `demo_tipos_tarea.py` para mostrar a los jueces:

```python
"""
Demo de clasificación inteligente de tareas.
Muestra cómo el sistema detecta diferentes tipos.
"""

from src.agente import SmartOptimizerAgent

tareas_ejemplo = [
    "Resume este artículo sobre IA",
    "Traduce al inglés: Hola mundo",
    "Escribe un poema sobre Python",
    "Genera un script que ordene una lista",
    "Compara Python vs JavaScript",
    "Analiza el impacto de la IA en empleos",
]

agente = SmartOptimizerAgent()

print("🎯 DEMO: Clasificación Inteligente de Tareas\n")

for i, tarea in enumerate(tareas_ejemplo, 1):
    print(f"{i}. Tarea: {tarea}")
    resultado = agente.ejecutar(tarea)
    tipo = resultado.get("tipo_tarea", "?")
    modelo = resultado.get("metricas_ejecucion", {}).get("modelo_usado", "?")
    print(f"   → Tipo: {tipo}")
    print(f"   → Modelo: {modelo}")
    print()
```

---

## 📤 SUBIR TU TRABAJO

```bash
# 1. Verificar cambios
git status

# 2. Agregar archivos
git add src/nodos/recibir_tarea.py
git add src/nodos/auditor_feedback.py
git add src/nodos/ejecutar_tarea.py
git add tests/test_prompts.py
git add demo_tipos_tarea.py  # si lo hiciste

# 3. Commit
git commit -m "Optimizar prompts y clasificación de tareas

- Agregar 5 nuevos tipos de tarea (código, análisis, etc.)
- Mejorar clasificación con más keywords
- Crear benchmarks por tipo de tarea en auditor
- Prompts especializados por tipo en ejecutar_tarea
- Temperature óptimo por tipo de tarea
- Tests de clasificación y prompts"

# 4. Push a tu rama
git push origin israel/prompts-optimizacion

# 5. Avisar a Carrada en Discord/Slack
```

---

## 🎤 NARRATIVA PARA TU PARTE

Cuando expliques en la presentación:

> **"Optimicé el sistema de prompts para que cada tipo de tarea use el prompt más efectivo. Por ejemplo, para código usamos temperature 0.2 (determinístico) y prompts de 'programador senior', mientras que para creatividad usamos 0.9 y prompts de 'escritor profesional'. El auditor ahora compara contra benchmarks específicos por tipo de tarea, haciendo recomendaciones mucho más precisas."**

---

## 🆘 SI TIENES PROBLEMAS

### Problema: No sé qué prompts usar

**Solución:**
1. Lee ejemplos en ChatGPT best practices: https://platform.openai.com/docs/guides/prompt-engineering
2. Mira prompts exitosos en `src/nodos/auditor_feedback.py` (ya funciona bien)
3. Pide a Copilot: "Dame 3 variaciones de prompt para [tipo_tarea]"

### Problema: Clasificación falla con algunas tareas

**Solución:**
```python
# Agregar logging para debug
print(f"DEBUG: tarea = {tarea}")
print(f"DEBUG: keywords encontradas = {keywords_match}")
print(f"DEBUG: tipo final = {tipo_tarea}")
```

### Problema: Auditor no da buenas recomendaciones

**Solución:**
1. Verifica que BENCHMARKS_POR_TIPO tenga valores sensatos
2. Prueba manualmente con diferentes tipos
3. Ajusta los benchmarks basándote en resultados reales

---

## ⏰ CHECKLIST FINAL

Antes de hacer push, verifica:

- [ ] `recibir_tarea.py` tiene mínimo 9 tipos de tarea
- [ ] Cada tipo tiene 5+ keywords
- [ ] `auditor_feedback.py` tiene benchmarks para todos los tipos
- [ ] Prompt del auditor es claro y específico
- [ ] `ejecutar_tarea.py` tiene prompts especializados
- [ ] Temperatures configurados por tipo
- [ ] Tests pasan: `pytest tests/test_prompts.py`
- [ ] Demo funciona: `python demo_hackathon.py`
- [ ] Código documentado con docstrings

---

## 🏆 IMPACTO DE TU TRABAJO

Tu implementación permite:
- ✅ **Clasificación inteligente** de 9+ tipos de tarea
- ✅ **Prompts optimizados** por tipo (mejor calidad)
- ✅ **Auditoría precisa** con benchmarks específicos
- ✅ **Sistema más profesional** y robusto

**¡Tu parte hace el sistema 10x más inteligente!** 🚀

---

## 📚 RECURSOS

- **Prompt Engineering:** https://platform.openai.com/docs/guides/prompt-engineering
- **Best Practices:** https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering
- **Temperature Guide:** https://platform.openai.com/docs/guides/text-generation

¡Éxito Israel! 💪
