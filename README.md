# Hackathon OpenAI

## Descripción
Proyecto para Hackathon Kavak x OpenAI México 2025: Agente que evalúa la complejidad de tareas y selecciona el modelo LLM más eficiente (GPT-3.5 vs GPT-4), refinando respuestas con un solo LLM y validando calidad con un Juez LLM. Demuestra "IA que piensa antes de gastar".

## Instalación

1. Clona el repositorio
2. Instala dependencias: `pip install -r requirements.txt`
3. Configura variables de entorno: `cp env.template .env`

## Estructura del Proyecto

- `src/`: Código fuente
- `data/`: Datos persistentes
- `docs/`: Documentación
- `notebooks/`: Notebooks de desarrollo
- `tests/`: Tests unitarios

## Arquitectura Simplificada (3 Nodos)

- **Nodo 1: Evaluación Contextual** (`src/nodos/evaluar_complejidad.py`): Analiza complejidad de la tarea.
- **Nodo 2: Generación y Refinamiento** (`src/nodos/generar_refinar.py`): Genera y refina con un solo LLM.
- **Nodo 3: Validación de Calidad** (`src/nodos/validar_calidad.py`): Valida con LLM-Juez.

## Separación de Trabajo (Compliant con Reglas 5.4/5.5)

### Preparado Pre-Evento (22 oct)

- ✅ Infraestructura: Cliente OpenAI, métricas, cache demo.
- ✅ Arquitectura: Stubs en `src/agente.py`, `src/nodos/`, `src/memoria.py`, `src/juez.py`.
- ✅ Documentación: Este README y análisis de reglas.
- ✅ Boilerplate: Estructura de proyecto, dependencias.

### Implementado en Evento (23 oct)

- 🔄 Lógica de Evaluación: Análisis de complejidad (longitud, keywords).
- 🔄 Generación/Refinamiento: Prompts para auto-feedback con un solo LLM.
- 🔄 Validación: Juez LLM para comparación objetiva.
- 🔄 Demos: Casos mixtos (GPT-3.5 gana en simple, GPT-4 en complejo).
- 🔄 Testing: Validación end-to-end y métricas de ahorro.

**Nota:** Nada de funcionalidad completa pre-evento. Todo preparado es stubs o soporte.

## Estado del Proyecto

Repositorio limpio con solo trabajo compliant. Proyecto rediseñado para simplicidad y máxima chance de ganar.
