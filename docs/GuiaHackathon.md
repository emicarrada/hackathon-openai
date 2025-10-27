# GUÍA PARA PARTICIPANTES

### Hackathon Kavak x OpenAI: Sistemas de AI Auto-Mejorables

```
23 de octubre de 2025 | Ciudad de México
```
## ¡Bienvenido!

Has sido seleccionado para participar en nuestro hackathon enfocado en una de las
fronteras más emocionantes de AI: **sistemas que pueden mejorarse a sí mismos**.
Esta guía te ayudará a entender qué estamos buscando, cómo prepararte y cómo
maximizar tus posibilidades de éxito el día del evento.

## Entendiendo el Reto

### ¿Qué Estamos Buscando Realmente?

Los sistemas de AI auto-mejorables no se tratan de superinteligencia exponencial y
autónoma. Estamos hablando de **sistemas prácticos con mecanismos robustos
de evaluación** que pueden identificar sus propias debilidades y actuar en base a
ese feedback—ya sea de forma autónoma o semi-automática.

### Los Componentes Centrales

Un sistema auto-mejorable necesita:

1. **Mecanismo de evaluación** - ¿Cómo mide el sistema su propio desempeño?
2. **Ciclo de retroalimentación** - ¿Cómo identifica qué salió mal o qué podría
    mejorar?
3. **Mecanismo de acción** - ¿Cómo implementa mejoras basadas en ese
    feedback?
4. **Mejora medible** - ¿Puedes probar que Run 2 es mejor que Run 1 y
    subsequente?

### Example Project

**Personalized Customer Service AI:**

- **Run 1:** AI agent handles customer query with generic approach
- **Evaluation:** System analyzes conversation quality, customer satisfaction signals, unresolved issues
- **Learning:** Updates customer memory profile, identifies communication patterns that work/don't work, refines orchestration strategy
- **Run 2:** Same customer or similar query → AI uses learned patterns, personalized memory, improved orchestration
- **Result:** Measurably better responses (faster resolution, higher satisfaction, fewer escalations)

This works because:


- Métricas de evaluación claras (tiempo de resolución, satisfacción)
- Mecanismo de feedback concreto (análisis de conversación)
- Mejoras accionables (actualizaciones de memoria, refinamiento de prompts,
    cambios en orquestación)
- Mejora demostrable que puedes mostrar

### ¿Qué hace que los Sistemas se Auto-Mejoren?

Diferentes mecanismos que podrías explorar:
**Ingeniería de Prompts:**

- Sistema analiza outputs fallidos
- Genera prompts mejorados
- Prueba y valida mejoras
**Orquestación Multi-Agente:**
- Agentes evalúan los outputs de otros
- Coordinador aprende qué agentes usar cuándo
- El enrutamiento mejora basado en desempeño pasado
**Sistemas de Memoria:**
- Sistema construye base de conocimiento de interacciones
- Recupera contexto relevante para consultas futuras
- Desempeño mejora conforme crece la memoria
**Evolución de Arquitectura:**
- Sistema identifica cuellos de botella en su propio pipeline
- Propone cambios arquitectónicos
- Implementa y valida mejoras
**Meta-Aprendizaje:**
- Sistema aprende "cómo aprender" de ejemplos
- Identifica patrones en sus errores
- Generaliza estrategias de mejora

### Conceptos Erróneos Comunes

❌ "Debe ser completamente autónomo" → Semi-automatizado está bien. Lo que
importa es que el sistema genere insights y mejoras, incluso si hay validación
humana.
❌ "Más complejo = mejor" → Falso. Un ciclo simple y funcional de auto-mejora
vence a uno complejo y roto cada vez.
❌ "Necesito técnicas novedosas de ML" → No necesitas inventar nuevos
algoritmos. Arquitectura inteligente y evaluación clara ganan.
❌ "El dominio del problema importa más" → La elección del problema importa para
puntos de creatividad, pero el mecanismo de auto-mejora es lo que realmente
juzgamos.


## Rúbrica de Evaluación

```
Filosofía de Evaluación: Este hackathon celebra la creatividad y diversidad de
enfoques. La rúbrica proporciona un marco estructurado pero flexible que permite a
los jueces evaluar proyectos muy diferentes de manera justa.
```
### Principios Fundamentales de Evaluación

```
● Flexibilidad con Rigor: Los proyectos pueden demostrar auto-mejora
de múltiples maneras válidas
● Contexto es Clave: Una mejora del 5% en un problema difícil puede
ser más impresionante que 50% en uno trivial
● El Proceso Importa: Un mecanismo inteligente con mejora modesta
vence a resultados no explicados
● Demostración > Promesas: Se juzga lo que funciona, no las
intenciones
● Simple y Funcional > Complejo y Roto: La ejecución cuenta más
que la ambición
```
### Expectativas Mínimas

```
Estos son elementos esperados que facilitan la evaluación, pero su ausencia no
descalifica automáticamente un proyecto:
```
- **Al menos dos iteraciones del sistema**
- **Casos de prueba documentados** (evaluation set de al menos 3-5 casos;
    más es mejor)
- **Alguna forma de medición** (métricas cuantitativas preferidas)
- **Evidencia de aprendizaje** (algún mecanismo que muestre que las versiones
    posteriores incorpora conocimiento de la primera)
_Nota importante: Si un proyecto tiene una innovación excepcional en su enfoque de
auto-mejora pero le falta uno de estos elementos, los jueces pueden usar
discreción. Lo crítico es demostrar mejora convincente de alguna forma._

### Distribución de Puntos (Total: 100)

```
Categoría Puntos Enfoque
```
**1. Demostración de Auto-Mejora** 35 Evidencia + Mecanismo
**2. Funcionalidad y Ejecución** 25 ¿Funciona?
**3. Creatividad e Innovación** 25 Enfoque + Problema
**4. Presentación y Claridad** 15 Comunicación
**TOTAL 100**


### 1. Demostración de Auto-Mejora (35 puntos)

#### A. Evidencia de Mejora (20 puntos)

_¿El sistema demuestra una mejora clara y medible?_
**Puntos Nivel Descripción
18-
Excepcional** Mejora dramática que transforma la capacidad del sistema. Corridas
posteriores resuelven que no podía manejar previamente.
**14-
Fuerte** Mejora clara y sustancial en métricas clave. El sistema es notablemente más
efectivo en Run 2.
**9-
Sólida** Mejora medible y consistente. Run 2 supera a Run 1 de manera observable
y repetible.
**4-8 Marginal** Mejora pequeña o inconsistente. Algunos casos mejoran, otros no.
**0-3 Insuficiente** Sin mejora clara, resultados ambiguos, o Run 2 es peor que Run 1.
**Consideraciones del juez:**

- Dificultad inherente del problema elegido
- Consistencia de mejora a través de los casos de prueba
- Claridad de las métricas

#### B. Sofisticación del Mecanismo (15 puntos)

```
¿Qué tan inteligente y robusto es el proceso de auto-mejora?
Puntos Nivel Descripción
13-
Innovador Mecanismo novedoso. El sistema analiza fallos profundamente,
identifica patrones de error específicos, y genera mejoras dirigidas.
Altamente automatizado.
10-
Sofisticado Feedback loop bien diseñado. Identifica QUÉ falló → POR QUÉ falló
→ CÓMO corregirlo. Buena automatización.
6-9 Funcional^ Feedback^ loop^ básico^ pero^ efectivo.^ Detecta^ errores^ y^ hace^ ajustes^
razonables. Puede requerir intervención humana moderada.
3-
Rudimentario Mejora principalmente manual o basada en prueba-y-error simple.
Poca automatización.
0-
Inexistente No hay mecanismo real de auto-mejora. Cambios aleatorios o
modificaciones manuales sin sistema.
El juez evalúa:
```
- Nivel de automatización (completamente automático > semi-automático >
    principalmente manual)
- Profundidad del análisis de errores (¿entiende POR QUÉ falló, no solo QUE
    falló?)
- Capacidad de generalizar aprendizajes a nuevos casos
- Robustez del mecanismo en diferentes escenarios


### 2. Funcionalidad y Ejecución (25 puntos)

```
¿El sistema funciona de punta a punta de manera confiable?
Puntos Nivel Descripción
22-25 Excepcional
Demo sin errores, el ciclo de auto-mejora funciona completamente
end-to-end, resultados claros y verificables con métricas bien
documentadas.
16-21 Sólido
Funciona con bugs menores, ciclo de mejora completo o casi completo,
resultados visibles y comprensibles.
10-15 Funcional
Funcionalidad básica, algunos componentes del ciclo funcionan, resultados
parciales pero demostrables.
0-9 Limitado
Problemas significativos, ciclo incompleto, resultados poco claros o demo no
funciona.
```
### 3. Creatividad e Innovación (25 puntos)

#### A. Originalidad del Enfoque Técnico (15 puntos)

```
¿Es el approach técnico único, creativo, o innovador?
Puntos Nivel Descripción
13-
Innovador Técnica o combinación novedosa. Pensamiento lateral que sorprende.
Approach único que no habíamos considerado.
10-
Creativo Twist inteligente en técnicas conocidas. Uso no convencional de
herramientas. Combinación interesante de métodos.
6-
Competente Implementación sólida de técnicas familiares. Bien ejecutado pero no
innovador. Approach esperado.
0-5 Genérico^ Solución^ estándar^ sin^ elementos^ distintivos.^ Lo^ que^ cualquiera^ habría^
intentado.
```
#### B. Elección e Interpretación del Problema (10 puntos)

_¿Es interesante el problema elegido o su planteamiento?_
**Puntos Nivel Descripción
9-
Inspirador** Dominio inesperado o ángulo totalmente fresco en problema conocido. Muestra
entendimiento profundo del dominio.
**7-
Sólido** Problema relevante bien planteado. Buen caso de uso para auto-mejora.
Aplicación clara.
**4-
Estándar** Problema típico de hackathon (chatbot, code gen, Q&A). Funciona pero no
innova en la elección.
**0-3 Poco claro** Problema confuso, trivial, o mal definido. No se entiende por qué eligieron esto.


### 4. Presentación y Claridad (15 puntos)

_¿Podemos entender qué hicieron y por qué importa?_
**Puntos Nivel Descripción
13-15 Excepcional**
Problema cristalino en <1 min, la mejora es obvia y medible, explicación
lógica del mecanismo, documentación impecable.
**10-12 Sólido**
Problema claro, mejora iterativa visible, explicación comprensible del
mecanismo, documentación estructurada.
**6-9 Adecuado** Se^ entiende^ el^ problema,^ mejora^ demostrable,^ explicación^ básica^ del^
proceso, documentación presente.
**0-5 Confuso**
Problema poco claro, mejora difícil de ver, explicación confusa,
documentación escasa o ausente.
**Importa:** Claridad, evidencia, storytelling simple, documentación estructurada
**No importa:** Slides bonitos, UI pulido, marketing speak

## Frameworks de Evaluación

```
Para ayudarte a diseñar sistemas auto-mejorables robustos, aquí presentamos
frameworks de evaluación establecidos que puedes aplicar:
```
### 1. Framework de Evaluación de Agentes de AI

```
Dimensiones de Evaluación:
```
- **Razonamiento y Planificación:** ¿Puede el sistema descomponer tareas
    complejas?
- **Uso de Herramientas:** ¿Selecciona y usa las herramientas correctas?
- **Auto-Reflexión:** ¿Identifica y corrige sus propios errores?
- **Memoria y Contexto:** ¿Retiene información relevante entre interacciones?
- **Generalización:** ¿Funciona en casos no vistos?

### 2. Métricas Cuantitativas Comunes

```
Para Sistemas de Q&A o RAG:
```
- Precisión de respuestas (accuracy)
- Relevancia de documentos recuperados (NDCG, MRR)
- Completitud de respuestas
- Fidelidad (responde basado en fuentes, sin alucinar)
**Para Sistemas de Código:**
- Pass@k (porcentaje de soluciones correctas)
- Cobertura de tests
- Eficiencia del código generado
- Errores de compilación/ejecución
**Para Sistemas Conversacionales:**


- Tasa de resolución de problemas
- Tiempo promedio de resolución
- Satisfacción del usuario (si aplicable)
- Número de turnos conversacionales

### 3. Framework de Evaluación Cualitativa

Cuando las métricas cuantitativas son difíciles, usa evaluación estructurada:

- **Escala Likert:** 1-5 o 1-7 en dimensiones específicas
- **Comparación Pareada:** ¿Output A o B es mejor?
- **Análisis de Errores:** Clasificar tipos de fallos
- **LLM-as-Judge:** Usar otro LLM para evaluar outputs

### 4. Herramientas de Evaluación Recomendadas

- **LangSmith** - Plataforma de observabilidad y evaluación de LangChain
    **Ragas** - Framework de evaluación específico para sistemas RAG
- **DeepEval** - Framework de evaluación de LLM de código abierto
- **Langfuse** - Observabilidad de LLM (tier gratuito)
- **Braintrust** - Plataforma de evaluación de LLM end-to-end
- **Evals Personalizados** - Escribe tus propios casos de prueba y funciones de
    puntuación

### Escenarios de Evaluación Comunes

**Escenario 1: Mejora Pequeña, Mecanismo Sofisticado**
Un equipo muestra una mejora del 8% pero con análisis profundo de errores,
categorización de fallos, y mejoras específicas basadas en patrones identificados.
_Evaluación:_ Puntos altos en Sofisticación del Mecanismo (12-15/15), puntos
medios-altos en Evidencia de Mejora (10-14/20) dependiendo de la consistencia.
**Escenario 2: Mejora Grande, Mecanismo Simple**
Un equipo muestra una mejora del 40% pero el mecanismo es básico: compara
outputs, identifica el peor, lo reemplaza manualmente.
_Evaluación:_ Puntos altos en Evidencia de Mejora (15-18/20), puntos bajos-medios
en Sofisticación (4-8/15).
**Escenario 3: Enfoque Innovador, Ejecución Parcial**
Un equipo tiene una idea brillante para auto-mejora que nadie ha visto, pero solo
funciona en el 60% de los casos.
_Evaluación:_ Puntos altos en Creatividad (22-25/25), puntos medios en Funcionalidad
(12-18/25) y Evidencia de Mejora (8-14/20) dependiendo de qué tan bien funciona.
**Principio guía:** Los tres proyectos anteriores podrían competir por el primer lugar
dependiendo de la calidad de ejecución y documentación. No hay una fórmula única
para ganar.


### Señales de Alerta (Red Flags)

- **Sin evidencia de mejora:** Afirman que mejoró pero no muestran métricas ni
    ejemplos
- **Mejora manual disfrazada:** El "sistema" es solo cambios manuales entre
    corridas
- **Cherry-picking:** Solo muestran casos donde funcionó, ocultan casos donde
    falló
- **Documentación inexistente:** Código sin comentarios, sin README,
    imposible entender qué hace
- **Demo no funciona:** Errores críticos, no completa el ciclo

## Recursos Técnicos

### Acceso a Plataforma OpenAI

Tendrás acceso completo a la plataforma OpenAI:

- Documentos de API OpenAI: https://platform.openai.com/docs
- Referencia de API: https://platform.openai.com/docs/api-reference
- Guía de Ingeniería de Prompts:
    https://platform.openai.com/docs/guides/prompt-engineering

### Frameworks Recomendados

**LangChain / LangGraph** - Altamente recomendado para construir sistemas
complejos de AI:

- Documentos de LangChain:
    https://python.langchain.com/docs/get_started/introduction
- LangGraph para Agentes: https://langchain-ai.github.io/langgraph/
- Excelente para orquestación, memoria y cadenas de evaluación
**LangChain Academy (Cursos GRATIS - ¡Altamente Recomendados!):**
- Introducción a LangGraph:
https://academy.langchain.com/courses/intro-to-langgraph
- Agentes Ambientales con LangGraph:
https://academy.langchain.com/courses/ambient-agents
- Investigación Profunda con LangGraph:
https://academy.langchain.com/courses/deep-research-with-langgraph
- Fundamentos de LangSmith: https://academy.langchain.com/

### Papers de Investigación 2025

**Lectura Obligatoria:**

**1. Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents
(Mayo 2025)**
    - arXiv: 2505.22954 https://arxiv.org/abs/2505.
    - Paper revolucionario sobre sistemas de AI que reescriben su propio código
    - Demuestra mejora de 20% → 50% en SWE-bench


- Por qué importa: Primer sistema práctico mostrando verdadera auto-mejora
    mediante modificación de código
**2. Survey on Evaluation of LLM-based Agents (Marzo 2025)**
- arXiv: 2503.16416 https://arxiv.org/abs/2503.
- Panorama comprensivo de metodologías de evaluación de agentes
- Por qué importa: Establece estándares para evaluar sistemas
auto-mejorables
3. **Agentic Context Engineering: Evolving Contexts for Self-Improving
Language Models**
● https://arxiv.org/html/2510.04618v
**Papers Clásicos (Aún Relevantes):**
- Self-Refine (2023) - arXiv:2303.17651 https://arxiv.org/abs/2303.
- Reflexion (2023) - arXiv:2303.1 1366 https://arxiv.org/abs/2303.1 1366

### Boilerplate y Configuración

**Opciones de Inicio Rápido:**

- Usa Python con paquetes openai, langchain, y langgraph
- Configura variables de entorno para llaves API
- Crea una prueba simple para verificar acceso a API

## Entregables y Métodos de Envío

### COMPONENTES REQUERIDOS:

### 1. Código Fuente (elige el formato más conveniente):

```
● Repositorio GitHub o GitLab
● Link de Replit / CodeSandbox / StackBlitz (código ejecutable en línea)
● Aplicación web deployada (Vercel, Netlify, Railway) + link al código
```
### 2. Documentación (OBLIGATORIA):

Tu proyecto debe incluir un **README.md** (en tu repositorio):
**Contenido mínimo requerido:**
● **Descripción del problema** que resuelves
● **Arquitectura del sistema** (diagrama opcional pero recomendado)
● **Instrucciones de ejecución** (cómo correr tu proyecto)
● **Explicación del ciclo de auto-mejora**
● **Métricas de mejora:** Evidencia cuantificable (ej: accuracy subió de 65% a 82%)


### 3. Demostración (elige UNO de los siguientes):

**Opción A - Video Pregrabado:**
● Formato: MP4, MOV, o AVI
● Duración: **Máximo 5 minutos**
● Contenido: Muestra tu sistema funcionando, el ciclo completo de mejora
● Sube a: **Google Drive, YouTube (no listado), Loom**
● Incluye el link en el formulario de entrega
**Opción B - Demo en Vivo:**
● Sistema **ejecutable directamente** por los jueces
● Puede ser: Replit ejecutable, app web funcionando, Jupyter Notebook con
instrucciones claras
● Los jueces deben poder ver el ciclo de mejora sin configuración compleja
**Opción C - Screen Recording:**
● Link de **Loom, Google Drive, o plataforma similar**
● Máximo 5 minutos
● Narración opcional pero recomendada

### 4. Presentación (Opcional pero Recomendada):

● Máximo **5 slides en PDF**
● Útil para los finalistas en la ronda final
● Incluye: problema, solución, resultados, demostración de mejora
**MÉTODO DE ENTREGA:
Primario - Google Form:**
● Link del form: Form
● Campos a completar:
● Nombre del equipo
● Integrantes (nombres y emails)
● Link al código (GitHub/Replit/Drive/etc.)
● Link al README o documentación
● Link al video/demo
● Link a slides (opcional)
● Comentarios adicionales
**REQUISITOS PARA SER EVALUADO:**
● Código accesible y ejecutable (o claramente documentado)
● README con las secciones mínimas requeridas
● Demo (video O ejecutable en vivo) que muestre el ciclo de mejora


## Estrategia de Preparación

**Para los equipos:**

- Decidan canales de comunicación (WhatsApp, Discord, etc.)
- Empiecen a investigar mecanismos de auto-mejora

### Errores Comunes a Evitar

❌ **Sobre-Ingeniería
Problema:** Construir un sistema multi-agente complejo con 7 componentes que
nunca funciona end-to-end.
**Solución:** Empieza simple. Un agente que mejora sus propios prompts es suficiente
si funciona bien.
❌ **Métricas Poco Claras
Problema:** "El sistema mejoró" sin ningún número.
**Solución:** Elige 1-2 métricas claras. Rastréalas. Muestra la mejora.
❌ **Sin Mejora Real
Problema:** Run 2 se desempeña igual que Run 1, o peor.
**Solución:** Si tu mecanismo de mejora no está funcionando, debuggea o simplifica tu
enfoque.

## Reflexiones Finales

### Qué Gana Hackathons

```
Demos funcionales - Funcionalidad vence ambición
Mejora clara - Muéstranos los números
Buena narrativa - Ayúdanos a entender por qué tu proyecto importa
Gestión del tiempo - Termina temprano, pule, envía con confianza
Coordinación de equipo - Trabajo dividido = progreso más rápido
```
### Recuerda

Este es un **sprint, no un maratón**. Tienes tiempo limitado para construir algo
increíble. Mantenlo simple, mantenlo funcionando, mantenlo medible.

- Entienden el reto profundamente
- Ejecutan eficientemente
- Muestran resultados claros
- Comunican efectivamente


**¿Preguntas antes del evento?** Email: hackathon@kavak.com
Logística y Transporte Estacionamiento: Capital Reforma ofrece servicio de valet parking con costo
de $110 MXN por día. También hay opciones de estacionamiento público en las cercanías. Te
recomendamos llegar con tiempo suficiente para encontrar estacionamiento y registrarte antes de las
8:45 AM.

#### ¡Nos vemos el 23 de octubre! 🚀

```
Hackathon Kavak x OpenAI 2025
```
