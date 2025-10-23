# 🎬 GUÍA DE DEMOS - SMART OPTIMIZER

**Fecha:** 23 oct 2025  
**Para:** Hackathon OpenAI México 2025

---

## 🎯 TIENES 3 TIPOS DE DEMOS

### 1️⃣ DEMO AUTOMÁTICA (Original)
**Archivo:** `demo_hackathon.py`  
**Mejor para:** Presentación principal (5 min)

#### Uso:
```bash
python demo_hackathon.py
```

**Características:**
- ✅ Tarea pre-definida
- ✅ Rápida (30 segundos)
- ✅ Predecible
- ✅ No puede fallar
- ✅ Visualizador completo

**Cuándo usarla:**
- Durante presentación formal de 5 minutos
- Cuando tienes tiempo limitado
- Cuando quieres garantizar que funciona

---

### 2️⃣ DEMO INTERACTIVA COMPLETA (Nueva)
**Archivo:** `demo_interactiva.py`  
**Mejor para:** Sesión de preguntas (Q&A)

#### Uso:
```bash
python demo_interactiva.py
```

**Flujo:**
1. Sistema te pregunta: "💬 Tu tarea:"
2. Tú escribes: "Resume este artículo sobre blockchain"
3. Sistema pide confirmación
4. Ejecuta Run 1 → Aprende → Run 2
5. Muestra visualizador

**Características:**
- ✅ Input libre del usuario
- ✅ Confirmación antes de ejecutar
- ✅ Ejemplos de tareas
- ✅ Colores y símbolos
- ✅ Mensajes amigables
- ✅ Visualizador completo

**Cuándo usarla:**
- Durante Q&A después de presentación
- Cuando jueces quieren probar con su propia tarea
- Para demostrar flexibilidad del sistema

---

### 3️⃣ DEMO RÁPIDA CON INPUT (Nueva)
**Archivo:** `demo_rapida_input.py`  
**Mejor para:** Pruebas rápidas / Demos express

#### Uso opción A (con argumento):
```bash
python demo_rapida_input.py "Resume este artículo sobre IA en 3 puntos"
```

#### Uso opción B (sin argumento):
```bash
python demo_rapida_input.py
# Te pedirá el input interactivamente
```

**Características:**
- ✅ Sin confirmaciones (más rápido)
- ✅ Acepta input como argumento
- ✅ Output simplificado pero claro
- ✅ Visualizador completo

**Cuándo usarla:**
- Cuando necesitas demo rápida (20 segundos)
- Para pruebas durante desarrollo
- Backup si demo interactiva falla

---

## 📊 COMPARACIÓN DE DEMOS

| Característica | Automática | Interactiva | Rápida Input |
|----------------|------------|-------------|--------------|
| **Tiempo** | 30 seg | 45 seg | 20 seg |
| **Input libre** | ❌ | ✅ | ✅ |
| **Confirmación** | ❌ | ✅ | ❌ |
| **Visualizador** | ✅ | ✅ | ✅ |
| **Colores** | ⚠️ | ✅ | ✅ |
| **Mejor para** | Presentación | Q&A | Pruebas |

---

## 🎤 EJEMPLOS DE TAREAS QUE PUEDES USAR

### Resúmenes:
```
"Resume este artículo sobre inteligencia artificial en 3 puntos"
"Resume las últimas noticias de tecnología"
"Haz un resumen ejecutivo de este reporte financiero"
```

### Traducciones:
```
"Traduce 'Hello World' al español y francés"
"Traduce este texto técnico al inglés"
"Convierte este email informal a tono profesional"
```

### Explicaciones:
```
"Explícame qué es machine learning en términos simples"
"Describe cómo funciona blockchain"
"Explica la diferencia entre IA y ML"
```

### Creación de contenido:
```
"Escribe un email profesional de seguimiento a un cliente"
"Genera 5 ideas para un proyecto de Python"
"Crea un plan de marketing para un startup tech"
```

### Análisis:
```
"Analiza este código Python y sugiere mejoras"
"Revisa este texto y corrige errores gramaticales"
"Dame feedback sobre esta propuesta de proyecto"
```

### Creatividad:
```
"Escribe un poema sobre programación"
"Genera nombres creativos para una app de productividad"
"Crea un eslogan para una empresa de IA"
```

---

## 🎯 ESTRATEGIA RECOMENDADA PARA HACKATHON

### Durante Presentación (5 minutos):

1. **Introducción (1 min):**
   - Explicar el problema (desperdicio en APIs)
   - Mencionar solución (automejora)

2. **Demo Automática (3 min):**
   ```bash
   python demo_hackathon.py
   ```
   - Narrar mientras corre
   - Destacar: "Run 1 caro → Aprende → Run 2 barato"
   - Mostrar visualizador: "90% ahorro"

3. **Cierre (1 min):**
   - Recap: "Único sistema que aprende"
   - Impacto: "$1.26 ahorro por cada 1000 runs"

### Durante Q&A (5-10 minutos):

**Si juez pregunta:**
> "¿Funciona con otros tipos de tareas?"

**Tú respondes:**
> "¡Claro! Déjame mostrarte..."

```bash
python demo_interactiva.py
# Juez ingresa su tarea
# Sistema demuestra flexibilidad
```

**Si juez pregunta:**
> "¿Qué tan rápido es?"

**Tú respondes:**
> "Menos de 30 segundos. Mira..."

```bash
python demo_rapida_input.py "Traduce este texto"
```

---

## 💡 TIPS PARA LA DEMO

### ✅ HACER:

1. **Antes de la demo:**
   - Probar todas las demos 2-3 veces
   - Tener terminal abierta y lista
   - Verificar API key funciona
   - Limpiar output anterior

2. **Durante la demo:**
   - Hablar mientras ejecuta (no quedarse callado)
   - Narrar lo que está pasando
   - Destacar visualizador al final
   - Mostrar emoción/entusiasmo

3. **Después de la demo:**
   - Ofrecer probar con tarea del juez
   - Responder preguntas técnicas
   - Mencionar código en GitHub

### ❌ EVITAR:

1. No ejecutar demo sin probar antes
2. No usar tareas muy largas (tardan más)
3. No quedarse callado mientras corre
4. No ignorar errores si ocurren
5. No olvidar mencionar el diferenciador clave

---

## 🚀 COMANDOS RÁPIDOS

### Probar demo automática:
```bash
python demo_hackathon.py
```

### Probar demo interactiva:
```bash
python demo_interactiva.py
```

### Probar con tu propia tarea:
```bash
python demo_rapida_input.py "Tu tarea aquí"
```

### Sin argumento (te pedirá input):
```bash
python demo_rapida_input.py
```

---

## 🎬 SCRIPT EJEMPLO PARA PRESENTACIÓN

**Tú hablas mientras ejecutas `python demo_hackathon.py`:**

```
[Ejecutar demo]

"Vean esto... Run 1 usa GPT-4o sin estrategia → Caro

[Esperar 10 seg mientras ejecuta]

Ahora el auditor detecta el desperdicio...
Memoria se actualiza con modelo optimizado...

[Esperar 10 seg]

Run 2 usa GPT-3.5-turbo → Más barato

[Visualizador aparece]

¡Miren! 90% de ahorro automático.
Esto es lo que nos diferencia: 
El sistema APRENDE sin intervención humana.

En producción, esto significa $1.26 de ahorro 
por cada 1000 tareas.

Ningún otro equipo tiene esto."
```

---

## 📞 TROUBLESHOOTING

### Error: "OPENAI_API_KEY no encontrada"
**Solución:**
```bash
export $(cat .env | xargs)
```

### Error: "Module not found"
**Solución:**
```bash
pip install -r requirements.txt
```

### Demo muy lenta
**Solución:**
- Usar tareas más cortas
- Verificar conexión internet
- Usar `demo_rapida_input.py`

### Quiero limpiar memoria manualmente
**Solución:**
```bash
echo "{}" > data/estrategias.json
```

---

## ✅ CHECKLIST ANTES DE PRESENTAR

- [ ] Probé `demo_hackathon.py` → Funciona
- [ ] Probé `demo_interactiva.py` → Funciona
- [ ] Probé `demo_rapida_input.py` → Funciona
- [ ] API key configurada
- [ ] Terminal lista y limpia
- [ ] Script de presentación memorizado
- [ ] Respuestas a FAQ preparadas
- [ ] Laptop cargada
- [ ] Plan B (screenshots/video) listo

---

**¡SUERTE EN EL HACKATHON!** 🚀🏆
