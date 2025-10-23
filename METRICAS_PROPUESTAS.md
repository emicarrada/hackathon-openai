# 📊 MÉTRICAS PROPUESTAS PARA SMART OPTIMIZER

## 🔍 ANÁLISIS DE MÉTRICAS ACTUALES

### **Métricas Existentes en el Sistema**

#### 1. **En `contador.py`** (Nivel técnico - API)
```python
{
    "modelo_usado": str,           # Modelo LLM utilizado
    "tokens_prompt": int,          # Tokens de entrada
    "tokens_completion": int,      # Tokens de salida
    "tokens_totales": int,         # Suma total
    "latencia_segundos": float,    # Tiempo de respuesta
    "error": str/None              # Errores de API
}
```

#### 2. **En `validar_calidad.py`** (Nivel comparación)
```python
{
    "mejor": str,                  # Ganador: respuesta/baseline/empate
    "puntaje_respuesta": float,    # Calidad 0-10 respuesta
    "puntaje_baseline": float,     # Calidad 0-10 baseline
    "ahorro_tokens": int,          # Diferencia de tokens
    "mejora_vs_baseline": str,     # Descripción textual
    "justificacion": str           # Explicación del juez
}
```

### **⚠️ LIMITACIONES ACTUALES**

1. **Costo**: Solo se cuentan tokens, no se calcula costo real en USD
2. **Calidad**: Puntajes 0-10 subjetivos del LLM-Juez, sin métricas objetivas
3. **Eficiencia**: No se mide throughput, escalabilidad ni recursos
4. **Usuario**: No se captura satisfacción ni usabilidad
5. **Sistema**: No se trackea memoria, CPU, caché hits
6. **Negocio**: No hay ROI, ahorro acumulado, ni valor generado

---

## 🎯 MÉTRICAS PROPUESTAS (ENFOQUE INTEGRAL)

### **CATEGORÍA 1: ECONÓMICAS (Cost Optimization)**

#### 📌 **1.1 Costos Absolutos**
```python
{
    "costo_prompt_usd": float,       # Costo de tokens de entrada
    "costo_completion_usd": float,   # Costo de tokens de salida
    "costo_total_usd": float,        # Costo total de la llamada
    "costo_baseline_usd": float,     # Costo si se usara siempre GPT-4
    "ahorro_usd": float,             # Diferencia entre baseline y actual
    "ahorro_porcentaje": float       # % de ahorro vs baseline
}
```

**Implementación**:
```python
# Precios por 1M tokens (actualizar según OpenAI)
PRECIOS_MODELOS = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4.1": {"input": 10.00, "output": 30.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50}
}

def calcular_costo(tokens_prompt, tokens_completion, modelo):
    precio = PRECIOS_MODELOS[modelo]
    costo_prompt = (tokens_prompt / 1_000_000) * precio["input"]
    costo_completion = (tokens_completion / 1_000_000) * precio["output"]
    return costo_prompt + costo_completion
```

#### 📌 **1.2 Costos Acumulados (Sesión)**
```python
{
    "costo_acumulado_usd": float,     # Total gastado en sesión
    "ahorro_acumulado_usd": float,    # Total ahorrado vs GPT-4
    "llamadas_totales": int,          # Número de requests
    "costo_promedio_request": float   # Costo medio por llamada
}
```

#### 📌 **1.3 Proyecciones**
```python
{
    "costo_proyectado_dia": float,     # Extrapolación a 24h
    "costo_proyectado_mes": float,     # Extrapolación a 30 días
    "ahorro_proyectado_mes": float     # Ahorro mensual estimado
}
```

---

### **CATEGORÍA 2: RENDIMIENTO (Performance)**

#### 📌 **2.1 Latencia Detallada**
```python
{
    "latencia_total_ms": float,         # Tiempo total en milisegundos
    "latencia_primer_token_ms": float,  # Time To First Token (TTFT)
    "throughput_tokens_seg": float,     # Tokens por segundo
    "latencia_promedio": float,         # Promedio de sesión
    "latencia_p50": float,              # Percentil 50 (mediana)
    "latencia_p95": float,              # Percentil 95
    "latencia_p99": float               # Percentil 99 (outliers)
}
```

**Justificación**: Los percentiles son cruciales para SLAs y experiencia de usuario.

#### 📌 **2.2 Throughput**
```python
{
    "requests_por_segundo": float,      # RPS actual
    "tokens_por_segundo": float,        # Velocidad de generación
    "palabras_por_segundo": float       # Velocidad legible
}
```

#### 📌 **2.3 Recursos del Sistema**
```python
{
    "memoria_usada_mb": float,          # RAM consumida
    "cpu_porcentaje": float,            # Uso de CPU
    "tiempo_procesamiento_local_ms": float  # Overhead local
}
```

---

### **CATEGORÍA 3: CALIDAD (Quality Assurance)**

#### 📌 **3.1 Métricas Objetivas de Texto**
```python
{
    "longitud_caracteres": int,         # Tamaño de respuesta
    "longitud_palabras": int,           # Conteo de palabras
    "longitud_oraciones": int,          # Número de oraciones
    "legibilidad_flesch": float,        # Flesch Reading Ease (0-100)
    "legibilidad_gunning_fog": float,   # Gunning Fog Index
    "diversidad_lexica": float,         # Unique words / Total words
    "complejidad_sintactica": float     # Avg words per sentence
}
```

**Implementación (Flesch)**:
```python
import textstat

def calcular_legibilidad(texto):
    return {
        "flesch_ease": textstat.flesch_reading_ease(texto),
        "gunning_fog": textstat.gunning_fog(texto),
        "words_per_sentence": len(texto.split()) / len(texto.split('.'))
    }
```

#### 📌 **3.2 Métricas de Similaridad**
```python
{
    "similaridad_coseno_baseline": float,   # 0-1 vs baseline
    "rouge_1": float,                       # Unigram overlap
    "rouge_2": float,                       # Bigram overlap
    "rouge_l": float,                       # Longest common subsequence
    "bleu_score": float                     # BLEU para comparación
}
```

**Implementación**:
```python
from sklearn.metrics.pairwise import cosine_similarity
from rouge_score import rouge_scorer

def calcular_similaridad(respuesta, baseline):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'])
    scores = scorer.score(respuesta, baseline)
    return {
        "rouge_1": scores['rouge1'].fmeasure,
        "rouge_2": scores['rouge2'].fmeasure,
        "rouge_l": scores['rougeL'].fmeasure
    }
```

#### 📌 **3.3 Métricas del Juez (Ampliadas)**
```python
{
    "puntaje_correccion": float,        # 0-10 (factual accuracy)
    "puntaje_completitud": float,       # 0-10 (covers all aspects)
    "puntaje_claridad": float,          # 0-10 (easy to understand)
    "puntaje_concision": float,         # 0-10 (not too verbose)
    "puntaje_coherencia": float,        # 0-10 (logical flow)
    "puntaje_relevancia": float,        # 0-10 (on-topic)
    "puntaje_total": float,             # Promedio de las 6 dimensiones
    "confianza_juez": float             # 0-1 (confidence del LLM)
}
```

**Prompt mejorado para el juez**:
```python
prompt = f"""
Evalúa estas respuestas en 6 dimensiones (0-10):

1. CORRECCIÓN: ¿Información factualmente correcta?
2. COMPLETITUD: ¿Cubre todos los aspectos de la pregunta?
3. CLARIDAD: ¿Fácil de entender?
4. CONCISIÓN: ¿Sin contenido redundante?
5. COHERENCIA: ¿Flujo lógico?
6. RELEVANCIA: ¿Responde directamente la pregunta?

Formato obligatorio:
CORRECCION_A: [0-10]
COMPLETITUD_A: [0-10]
... (6 dimensiones × 2 respuestas)
GANADOR: [A/B/EMPATE]
CONFIANZA: [0.0-1.0]
JUSTIFICACION: [explicación]
"""
```

---

### **CATEGORÍA 4: EFICIENCIA OPERACIONAL**

#### 📌 **4.1 Tasa de Éxito**
```python
{
    "tasa_exito": float,               # % requests exitosas
    "tasa_error_api": float,           # % errores de API
    "tasa_error_parsing": float,       # % errores de parsing
    "tasa_fallback": float,            # % veces que usó fallback
    "disponibilidad": float            # Uptime %
}
```

#### 📌 **4.2 Caché y Optimización**
```python
{
    "cache_hit_rate": float,           # % hits en caché
    "cache_size_mb": float,            # Tamaño del caché
    "requests_deduplicadas": int,      # Requests idénticas evitadas
    "ahorro_cache_usd": float          # Ahorro por caché
}
```

#### 📌 **4.3 Estrategia de Modelo**
```python
{
    "distribucion_modelos": dict,      # {"gpt-4o-mini": 45%, "gpt-4o": 30%, ...}
    "precision_clasificador": float,   # % veces que eligió modelo correcto
    "tasa_downgrade": float,           # % veces que bajó de modelo
    "tasa_upgrade": float              # % veces que subió de modelo
}
```

---

### **CATEGORÍA 5: EXPERIENCIA DE USUARIO**

#### 📌 **5.1 Satisfacción (Post-procesamiento)**
```python
{
    "tiempo_respuesta_percibido": str,  # "Instantáneo/Rápido/Lento"
    "longitud_respuesta_adecuada": bool, # ¿Ni muy corta ni muy larga?
    "requirio_clarificacion": bool,     # ¿Usuario pidió aclaración?
    "tasa_abandono": float              # % usuarios que no esperan
}
```

#### 📌 **5.2 Valor Generado**
```python
{
    "complejidad_pregunta": str,        # "baja/media/alta"
    "valor_informativo": float,         # 0-1 (qué tan útil es)
    "tiempo_ahorrado_usuario": float,   # Minutos que se ahorró el usuario
    "equivalente_trabajo_humano": float # Horas de trabajo equivalente
}
```

---

### **CATEGORÍA 6: MÉTRICAS DE NEGOCIO**

#### 📌 **6.1 ROI (Return on Investment)**
```python
{
    "roi_porcentaje": float,            # (Ahorro - Costo Dev) / Costo Dev * 100
    "break_even_requests": int,         # # requests para recuperar inversión
    "valor_generado_usd": float,        # Valor total para el negocio
    "payback_period_dias": int          # Días para ROI positivo
}
```

#### 📌 **6.2 Escalabilidad**
```python
{
    "requests_maximas_dia": int,        # Capacidad máxima
    "costo_por_mil_usuarios": float,    # Costo de servir 1k usuarios
    "margen_operativo": float           # % de ganancia después de costos
}
```

---

## 📊 ESTRUCTURA DE MÉTRICAS PROPUESTA (JSON)

```json
{
    "timestamp": "2025-10-23T15:30:45Z",
    "request_id": "uuid-123-456",
    "tarea": "Explica machine learning",
    
    "economicas": {
        "costo_prompt_usd": 0.000015,
        "costo_completion_usd": 0.00006,
        "costo_total_usd": 0.000075,
        "costo_baseline_usd": 0.0008,
        "ahorro_usd": 0.000725,
        "ahorro_porcentaje": 90.625,
        "costo_acumulado_sesion": 0.0045,
        "ahorro_acumulado_sesion": 0.0435
    },
    
    "rendimiento": {
        "latencia_total_ms": 1250,
        "latencia_primer_token_ms": 280,
        "throughput_tokens_seg": 48.5,
        "latencia_promedio_sesion": 1180,
        "latencia_p95": 1800,
        "memoria_usada_mb": 85.3,
        "cpu_porcentaje": 12.5
    },
    
    "calidad": {
        "objetivas": {
            "longitud_palabras": 245,
            "legibilidad_flesch": 62.3,
            "diversidad_lexica": 0.68,
            "palabras_por_oracion": 18.5
        },
        "comparativas": {
            "similaridad_coseno_baseline": 0.87,
            "rouge_1": 0.72,
            "rouge_2": 0.58,
            "rouge_l": 0.65
        },
        "juez": {
            "puntaje_correccion": 9.2,
            "puntaje_completitud": 8.8,
            "puntaje_claridad": 9.0,
            "puntaje_concision": 7.5,
            "puntaje_coherencia": 8.9,
            "puntaje_relevancia": 9.1,
            "puntaje_total": 8.75,
            "confianza_juez": 0.92,
            "ganador": "respuesta",
            "justificacion": "Respuesta más concisa sin perder calidad"
        }
    },
    
    "eficiencia": {
        "modelo_usado": "gpt-4o-mini",
        "complejidad_clasificada": "media",
        "precision_clasificador": 0.94,
        "cache_hit": false,
        "tasa_exito_sesion": 0.98,
        "distribucion_modelos": {
            "gpt-4o-mini": 0.60,
            "gpt-4o": 0.30,
            "gpt-4.1": 0.10
        }
    },
    
    "usuario": {
        "tiempo_respuesta_percibido": "Rápido",
        "longitud_adecuada": true,
        "valor_informativo": 0.85,
        "tiempo_ahorrado_min": 15
    },
    
    "negocio": {
        "roi_porcentaje": 850,
        "valor_generado_usd": 2.50,
        "margen_operativo": 0.97
    }
}
```

---

## 🛠️ IMPLEMENTACIÓN RECOMENDADA

### **Paso 1: Extender `contador.py`**

```python
# Nuevo archivo: src/metricas_avanzadas.py

import time
import psutil
import textstat
from typing import Dict, Any

class MetricasIntegrales:
    """Clase para capturar métricas comprehensivas."""
    
    PRECIOS_MODELOS = {
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4.1": {"input": 10.00, "output": 30.00}
    }
    
    def __init__(self):
        self.sesion = {
            "costo_acumulado": 0.0,
            "ahorro_acumulado": 0.0,
            "llamadas_totales": 0,
            "latencias": [],
            "distribucion_modelos": {}
        }
    
    def calcular_economicas(self, tokens_prompt, tokens_completion, modelo):
        """Calcula métricas económicas."""
        precio = self.PRECIOS_MODELOS.get(modelo, {"input": 0, "output": 0})
        costo_prompt = (tokens_prompt / 1_000_000) * precio["input"]
        costo_completion = (tokens_completion / 1_000_000) * precio["output"]
        costo_total = costo_prompt + costo_completion
        
        # Calcular baseline (siempre GPT-4.1)
        precio_baseline = self.PRECIOS_MODELOS["gpt-4.1"]
        costo_baseline = (
            (tokens_prompt / 1_000_000) * precio_baseline["input"] +
            (tokens_completion / 1_000_000) * precio_baseline["output"]
        )
        
        ahorro = costo_baseline - costo_total
        ahorro_pct = (ahorro / costo_baseline * 100) if costo_baseline > 0 else 0
        
        # Actualizar sesión
        self.sesion["costo_acumulado"] += costo_total
        self.sesion["ahorro_acumulado"] += ahorro
        self.sesion["llamadas_totales"] += 1
        
        return {
            "costo_prompt_usd": round(costo_prompt, 6),
            "costo_completion_usd": round(costo_completion, 6),
            "costo_total_usd": round(costo_total, 6),
            "costo_baseline_usd": round(costo_baseline, 6),
            "ahorro_usd": round(ahorro, 6),
            "ahorro_porcentaje": round(ahorro_pct, 2),
            "costo_acumulado_sesion": round(self.sesion["costo_acumulado"], 6),
            "ahorro_acumulado_sesion": round(self.sesion["ahorro_acumulado"], 6)
        }
    
    def calcular_rendimiento(self, latencia_seg, tokens_totales):
        """Calcula métricas de rendimiento."""
        self.sesion["latencias"].append(latencia_seg * 1000)  # a ms
        
        return {
            "latencia_total_ms": round(latencia_seg * 1000, 2),
            "throughput_tokens_seg": round(tokens_totales / latencia_seg, 2),
            "latencia_promedio_sesion": round(sum(self.sesion["latencias"]) / len(self.sesion["latencias"]), 2),
            "memoria_usada_mb": round(psutil.Process().memory_info().rss / 1024 / 1024, 2),
            "cpu_porcentaje": round(psutil.cpu_percent(interval=0.1), 2)
        }
    
    def calcular_calidad_objetiva(self, texto: str):
        """Calcula métricas objetivas de texto."""
        palabras = texto.split()
        oraciones = texto.split('.')
        
        return {
            "longitud_caracteres": len(texto),
            "longitud_palabras": len(palabras),
            "longitud_oraciones": len(oraciones),
            "legibilidad_flesch": round(textstat.flesch_reading_ease(texto), 2),
            "diversidad_lexica": round(len(set(palabras)) / len(palabras), 3),
            "palabras_por_oracion": round(len(palabras) / max(len(oraciones), 1), 2)
        }
    
    def calcular_eficiencia(self, modelo: str, complejidad: str):
        """Trackea distribución de modelos."""
        if modelo not in self.sesion["distribucion_modelos"]:
            self.sesion["distribucion_modelos"][modelo] = 0
        self.sesion["distribucion_modelos"][modelo] += 1
        
        total = sum(self.sesion["distribucion_modelos"].values())
        distribucion = {
            k: round(v / total, 3) 
            for k, v in self.sesion["distribucion_modelos"].items()
        }
        
        return {
            "modelo_usado": modelo,
            "complejidad_clasificada": complejidad,
            "distribucion_modelos": distribucion
        }
```

### **Paso 2: Integrar en `validar_calidad.py`**

```python
from src.metricas_avanzadas import MetricasIntegrales

# Crear instancia global
metricas_tracker = MetricasIntegrales()

def validar_calidad(respuesta, baseline, tarea):
    # ... código existente ...
    
    # AGREGAR métricas integrales
    metricas_economicas = metricas_tracker.calcular_economicas(
        tokens_respuesta, tokens_baseline, modelo_usado
    )
    
    metricas_rendimiento = metricas_tracker.calcular_rendimiento(
        latencia, tokens_respuesta
    )
    
    metricas_calidad = metricas_tracker.calcular_calidad_objetiva(respuesta)
    
    resultado["metricas_integrales"] = {
        "economicas": metricas_economicas,
        "rendimiento": metricas_rendimiento,
        "calidad": metricas_calidad
    }
    
    return resultado
```

---

## 📈 DASHBOARD PROPUESTO

### **Vista 1: Resumen Ejecutivo**
```
┌──────────────────────────────────────────────────────────────┐
│  SMART OPTIMIZER - DASHBOARD EN TIEMPO REAL                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  💰 AHORRO HOY:        $12.45  (↑ 87% vs GPT-4)            │
│  ⚡ LATENCIA AVG:      1.2s    (↓ 15% vs ayer)             │
│  ✅ CALIDAD AVG:       8.7/10  (↑ 0.3 vs semana pasada)    │
│  📊 REQUESTS:          156     (↑ 23% vs ayer)             │
│                                                              │
│  Modelo más usado:     gpt-4o-mini (62%)                    │
│  Tasa de éxito:        98.7%                                │
│  ROI acumulado:        $487 (3,800% ROI)                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### **Vista 2: Distribución de Modelos**
```
gpt-4o-mini ████████████████████████████████ 62%  $3.20
gpt-4o      ████████████████                 28%  $8.90
gpt-4.1     ████                             10%  $15.20
```

### **Vista 3: Calidad vs Costo**
```
      Calidad
10 │         ●
 9 │       ●   ●
 8 │     ●   ●
 7 │   ●
 6 │ ●
   └──────────────── Costo
     $0  $5  $10 $15
     
● = Request individual
Zona verde = Alto valor (alta calidad, bajo costo)
```

---

## 🎯 PRIORIZACIÓN (Qué implementar primero)

### **FASE 1 (DEMO HACKATHON)** ⭐⭐⭐
1. ✅ Costos en USD (económicas básicas)
2. ✅ Ahorro porcentual vs baseline
3. ✅ Métricas de calidad objetivas (longitud, legibilidad)
4. ✅ Dashboard visual simple

**Impacto**: Alto - Demuestra valor del sistema claramente

### **FASE 2 (POST-HACKATHON)** ⭐⭐
5. Latencias percentiladas (p50, p95, p99)
6. Distribución de modelos en sesión
7. ROI y proyecciones
8. Métricas de similaridad (ROUGE, BLEU)

**Impacto**: Medio - Mejora análisis técnico

### **FASE 3 (PRODUCCIÓN)** ⭐
9. Recursos del sistema (CPU, RAM)
10. Caché y optimizaciones
11. Métricas de usuario (satisfacción)
12. Escalabilidad y throughput

**Impacto**: Bajo pero necesario para producción

---

## ✅ RESUMEN: CÓMO ESTO MEJORA EL PROYECTO

| Aspecto | Antes | Después (Integral) |
|---------|-------|-------------------|
| **Costo** | Solo tokens | USD reales + proyecciones + ROI |
| **Calidad** | Puntaje subjetivo 0-10 | 6 dimensiones + métricas objetivas + ROUGE |
| **Rendimiento** | Latencia simple | Percentiles + throughput + recursos |
| **Valor** | No medido | Ahorro acumulado + valor generado + ROI |
| **Decisiones** | Intuición | Data-driven con 30+ métricas |
| **Demo** | "Funciona" | "Ahorra 87% con 98% de calidad" |

---

## 🔥 SIGUIENTE PASO INMEDIATO

**Crear archivo `src/metricas_avanzadas.py` con las 3 funciones principales**:
1. `calcular_economicas()` - Costos en USD
2. `calcular_rendimiento()` - Latencias y throughput
3. `calcular_calidad_objetiva()` - Métricas de texto

**¿Quieres que implemente esto ahora?**
