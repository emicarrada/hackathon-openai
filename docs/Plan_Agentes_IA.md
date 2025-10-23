# Plan de Acción para Usar Agentes de IA en el Hackathon

## Introducción

Durante el hackathon, cada miembro del equipo usará agentes de IA (como GitHub Copilot, ChatGPT o Claude) para acelerar la implementación. El objetivo es generar código de alta calidad sin alucinaciones, enfocándonos en precisión, compatibilidad con LangGraph y cumplimiento de reglas.

## Plan General de Acción

1. **Proporciona Contexto Completo**: Antes de pedir código, pega el pseudocódigo relevante, estructura del proyecto y requisitos (ej: "Implementa basado en este pseudocódigo, usando openai library").

2. **Itera y Valida**: Pide al agente que genere código, luego revísalo manualmente. Si hay errores, pide correcciones específicas (ej: "Arregla el manejo de errores").

3. **Evita Alucinaciones**: Usa prompts específicos, limita scope (ej: "No inventes APIs, usa solo openai oficial"). Pide explicaciones: "¿Por qué este código funciona?".

4. **Mejores Prácticas**:
   - Código modular, comentado.
   - Pruebas unitarias después de cada función.
   - Compatibilidad: Retorna dicts para LangGraph.
   - Seguridad: No hardcode keys; usa os.getenv.

5. **Herramientas Recomendadas**: GitHub Copilot para autocompletado en VS Code; ChatGPT para brainstorming.

6. **Tiempo**: Dedica 10-15 min por prompt. Si el agente falla, implementa manualmente.

## Prompts Específicos por Rol

### Para Brandon Vilchis (Evaluador - Spoke1)

**Prompt Base**:
"Actúa como un desarrollador experto en Python. Implementa la función `evaluar_complejidad(tarea: str) -> dict` basada en este pseudocódigo [pega pseudocódigo]. Usa la biblioteca `openai` para cualquier llamada API, pero en este caso no es necesario. El output debe ser un dict con 'complejidad' ('baja', 'media', 'alta'), 'factores' (longitud, keywords). Asegura que sea compatible con LangGraph. Evita alucinaciones: no inventes funciones inexistentes. Explica cada línea. Código final debe ser ejecutable y sin errores."

**Plan de Acción**:

- Pega el pseudocódigo del setup.
- Pide implementación paso a paso.
- Valida: Prueba con "Hola" (baja) y "Explica relatividad" (alta).
- Si alucina, agrega: "Usa solo lógica condicional simple, no ML avanzado."

### Para Israel Cabrera (Generador/Refinador - Spoke2)

**Prompt Base**:
"Como experto en IA, implementa `generar_refinar(tarea: str, complejidad: str) -> str` usando Self-Refine con un solo LLM. Basado en este pseudocódigo [pega pseudocódigo]. Usa `openai.OpenAI` para llamadas. Modelo: 'gpt-3.5-turbo' si complejidad=='baja', else 'gpt-4'. Limita tokens a 500. Retorna string refinado. Evita alucinaciones: No uses APIs inventadas. Explica el loop de Self-Refine. Código debe manejar errores (try-except) y ser eficiente."

**Plan de Acción**:

- Proporciona contexto de Self-Refine.
- Pide generación inicial + refinamiento.
- Testea: Input "Suma 2+2", output mejorado.
- Corrección: Si alucina, especifica "Usa solo chat completions, no embeddings."

### Para Cristopher Carrada (Validador/Tester - Hub)

**Prompt Base**:
"Experto en testing, implementa `validar_calidad(output_gpt35: str, output_gpt4: str, tarea: str) -> dict` usando un Juez LLM. Pseudocódigo [pega]. Usa `openai` para juicio objetivo. Prompt al juez: 'Compara outputs para [tarea]: GPT-3.5: [output35], GPT-4: [output4]. ¿Cuál mejor? Razón.' Parsea respuesta para 'mejor_modelo'. Agrega métricas simples (ej: len(output)). Compatible con LangGraph. Sin alucinaciones: Solo lógica de comparación. Explica parsing."

**Plan de Acción**:

- Enfócate en Juez LLM primero.
- Luego, integra testing end-to-end.
- Valida: Compara outputs reales, mide mejora.
- Si falla, pide: "Simplifica parsing a string matching."

## Checklist Final

- [ ] Proporciona contexto antes de prompts.
- [ ] Revisa código generado (no copies ciegamente).
- [ ] Prueba en entorno real.
- [ ] Si alucina, refina prompt con más detalles.
- [ ] Comparte código con el hub para integración.

Este plan asegura código de alta calidad y eficiencia. ¡Usen agentes como asistentes, no como reemplazos!
