# Smart Optimizer - Hackathon OpenAI 2025

## 🎯 Descripción
**Sistema con AUTOMEJORA REAL** para Hackathon Kavak x OpenAI México 2025.

Diferenciador clave: **Único sistema que aprende de cada ejecución**
- Run 1: Usa modelo caro (GPT-4o) → Auditor detecta desperdicio
- Memoria se actualiza con estrategia optimizada
- Run 2: Usa modelo barato (GPT-3.5-turbo) → **87% de ahorro**

## 🚀 Instalación Rápida

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd hackathon-openai

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar API Key
cp env.template .env
# Editar .env y añadir tu OPENAI_API_KEY

# 4. Ejecutar demo
export $(cat .env | xargs)
python demo_hackathon.py
```

## 🏗️ Arquitectura - 6 Nodos con Automejora

Sistema completo con feedback loop persistente:

```
1. recibir_tarea      → Clasifica tipo de tarea (resumen, traducción, etc.)
2. consultar_memoria  → Busca estrategia aprendida en JSON
3. ejecutar_tarea     → Ejecuta con modelo seleccionado
4. evaluar_contador   → Captura métricas (tokens, latencia)
5. auditor_feedback   → LLM-Crítico analiza eficiencia
6. actualizar_memoria → Guarda estrategia optimizada
```

### Flujo de Automejora

```
RUN 1 (Inocente):
  Usuario: "Resume este artículo"
  → Sin estrategia → Usa GPT-4o (default caro)
  → 128 tokens consumidos
  → Auditor detecta: "Tarea simple no necesita GPT-4o"
  → Memoria actualizada: {resumen: gpt-3.5-turbo}

RUN 2 (Inteligente):
  Usuario: "Resume este otro artículo"
  → Estrategia encontrada → Usa GPT-3.5-turbo
  → 155 tokens pero modelo 10x más barato
  → Ahorro real en costos de API
```

## 📁 Estructura del Proyecto

```
hackathon-openai/
├── src/
│   ├── agente.py              # Orquestador LangGraph (6 nodos)
│   ├── memoria.py             # Persistencia de estrategias
│   ├── utils.py               # Utilidades generales
│   └── nodos/
│       ├── recibir_tarea.py
│       ├── consultar_memoria.py
│       ├── ejecutar_tarea.py
│       ├── evaluar_contador.py
│       ├── auditor_feedback.py
│       └── actualizar_memoria.py
├── data/
│   └── estrategias.json       # Memoria persistente (JSON)
├── docs/
│   ├── AUTOMEJORA_Y_RUBRICA.md    # Explicación técnica
│   └── Diagrama_Sistema_Completo.tex  # Diagrama LaTeX
├── tests/
│   ├── test_nodos.py
│   ├── test_contador.py
│   └── test_utils.py
├── demo_hackathon.py          # Script de presentación
└── requirements.txt
```

## 🎬 Demo para Presentación

```bash
# Demo completa (2-3 minutos)
python demo_hackathon.py

# Demo rápida (30 segundos)
python demo_hackathon.py --rapida
```

### Salida Esperada

```
🎬 DEMO PARA HACKATHON: Run 1 vs Run 2
======================================================================

▶️  RUN 1 - SISTEMA INOCENTE (Sin estrategia)
   Modelo usado: gpt-4o
   Tokens consumidos: 128
   🔍 Auditor detectó ineficiencia
   💾 Memoria actualizada

▶️  RUN 2 - SISTEMA INTELIGENTE (Con estrategia aprendida)
   Modelo usado: gpt-3.5-turbo
   Tokens consumidos: 155
   
🎯 Ahorro conseguido:
   - Modelo 10x más barato
   - Escalable a millones de requests
   - Sin pérdida de calidad
```

## 🏆 Puntos Clave para Jueces

### ✅ INNOVACIÓN (30 pts)
- **Único sistema con automejora REAL** en el hackathon
- Arquitectura 6 nodos con feedback loop persistente
- Auditor LLM que evalúa eficiencia automáticamente

### ✅ IMPACTO (25 pts)
- 87% de ahorro en costos de API demostrado en vivo
- Escalable a millones de solicitudes (ahorro masivo)
- Aplicable a cualquier industria que use LLMs

### ✅ EJECUCIÓN (25 pts)
- Sistema funcional end-to-end
- LangGraph + OpenAI + Memoria persistente (JSON)
- Tests automatizados y documentación completa

### ✅ PRESENTACIÓN (20 pts)
- Demo clara y visual (Run 1 vs Run 2)
- Narrativa fuerte: "Sistema que aprende de sus errores"
- Diagrama LaTeX profesional del flujo

**� TOTAL: 100/100 puntos posibles**

## 🔧 Stack Técnico

- **LangGraph 0.0.40+**: Orquestación de nodos con StateGraph
- **OpenAI API**: GPT-4o, GPT-3.5-turbo, GPT-4o-mini
- **Python 3.10+**: Asyncio, typing, dataclasses
- **JSON**: Persistencia de memoria (data/estrategias.json)

## 📚 Documentación Adicional

- **`docs/AUTOMEJORA_Y_RUBRICA.md`**: Explicación técnica completa + mapeo a rúbrica
- **`docs/Diagrama_Sistema_Completo.tex`**: Diagrama LaTeX para presentación
- **`METRICAS_PROPUESTAS.md`**: 30+ métricas avanzadas para extensiones futuras

## 👥 Equipo

- **Brandon**: Nodo Evaluador + Tests
- **Israel**: Nodo Generador + Integración
- **Cristopher**: Nodo Validador + Memoria
- **Emiliano (Carrada)**: Arquitectura + Orquestación

## 📄 Licencia

Proyecto para Hackathon OpenAI 2025 - Kavak x OpenAI México
