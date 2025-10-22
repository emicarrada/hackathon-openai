# Infraestructura Pre-Evento: Smart Optimizer para Hackathon OpenAI

## Resumen Ejecutivo
Este documento detalla la infraestructura preparada pre-evento para el proyecto **Smart Optimizer**, un agente que demuestra "IA que piensa antes de gastar" mediante Self-Refine, selección contextual de modelos, y validación con LLM-Judge. Todo el trabajo pre-evento se limita a stubs, boilerplate e infraestructura, cumpliendo estrictamente las reglas 5.4 y 5.5.

## Arquitectura Preparada
### Estructura del Proyecto
- **src/**: Código fuente con stubs de nodos y utilidades.
  - `agente.py`: Clase SmartOptimizerAgent con métodos stubs para los 3 nodos.
  - `nodos/`: Stubs para evaluar_complejidad, generar_refinar, validar_calidad.
  - `utils.py`: Inicialización segura de OpenAI client.
  - `contador.py`: Métricas de llamadas con modo demo.
  - `memoria.py`: Gestión de estrategias en JSON.
  - `juez.py`: Wrapper para LLM-Judge.
- **data/**: `estrategias.json` con estrategias iniciales hardcodeadas.
- **tests/**: Tests básicos para validar stubs.
- **notebooks/**: (Pendiente) Notebook para pruebas de flujo.
- **docs/**: Esta documentación.

### Componentes Clave
- **LangGraph**: Preparado para orquestar los 3 nodos (evaluación, generación/refinamiento, validación).
- **Self-Refine**: Stub para un solo LLM manejando generación, feedback y refinamiento.
- **Selección Contextual**: Basada en complejidad (baja/media/alta) para elegir GPT-3.5 o GPT-4.
- **LLM-Judge**: Stub para comparación de calidad.

## Cumplimiento de Reglas
### Regla 5.4: Solo Infraestructura Pre-Evento
- **Implementado**: Stubs, boilerplate, plantillas y datos iniciales.
- **No Implementado**: Lógica de auto-mejora, aprendizaje automático o llamadas reales a OpenAI (excepto en modo demo controlado).
- **Ejemplos**:
  - Nodos retornan valores fijos (e.g., complejidad "baja").
  - Estrategias en JSON son placeholders.
  - Tests verifican existencia de funciones, no funcionalidad.

### Regla 5.5: Lógica Durante el Evento
- Toda la lógica de auto-mejora (aprendizaje de estrategias, refinamiento iterativo, validación) se implementará en vivo durante el hackathon.
- Pre-evento: Solo preparación para que el código sea ejecutable y extensible.

## Plan de Acción por Roles
### Rol 1: Líder de Infraestructura y Contador - Brandon Vilchis (Diseño y Soporte Técnico)
- **Qué hizo**: Diseñó y robusteció la infraestructura base (utils.py para inicialización de OpenAI, contador.py para métricas con manejo de errores). Integró activamente con Rol 2 para asegurar compatibilidad en agente.py. Creó documentación de API interna y verificó contratos de datos con Rol 3.
- **Cómo lo hizo**: Implementó manejo de excepciones específicas de OpenAI (AuthenticationError, RateLimitError, etc.) en contador.py. Aseguró que funciones retornen siempre métricas válidas. Colaboró en pruebas de integración para que el grafo funcione sin errores.
- **Acciones en Evento**: Monitorear métricas en tiempo real durante el hackathon. Ajustar contador.py para logging avanzado. Apoyar debugging de llamadas a API.

### Rol 2: Líder de Arquitectura y LangGraph - Cristopher Carrada (Implementación y Orquestación)
- **Qué hizo**: Construyó la arquitectura del agente con LangGraph (agente.py con 3 nodos: evaluación, generación/refinamiento, validación). Integró llamadas reales a contador.py en nodos. Creó notebooks de prueba para flujo end-to-end.
- **Cómo lo hizo**: Usó LangGraph para definir el grafo de nodos stubs. Hardcodeó selecciones de modelo para pruebas de integración (siguiendo reglas). Actualizó nodos para llamar funciones de infraestructura sin implementar lógica de auto-mejora.
- **Acciones en Evento**: Implementar lógica real en nodos (evaluación contextual, Self-Refine iterativo, validación con LLM-Judge). Gestionar el flujo del grafo durante el evento. Optimizar orquestación para eficiencia.

### Rol 3: Líder de Prompts y Memoria - Israel Cabrera (Prompts y Memoria)
- **Qué hizo**: Creó módulos de memoria (memoria.py para estrategias en JSON) y prompts dinámicos (juez.py como wrapper para LLM-Judge). Diseñó plantillas de prompts para auditor y juez. Verificó integración con Rol 2.
- **Cómo lo hizo**: Implementó funciones para leer/escribir estrategias.json de forma robusta. Creó wrappers para prompts que aceptan métricas y generan texto formateado. Aseguró contratos de datos alineados con otros roles.
- **Acciones en Evento**: Desarrollar prompts reales para Self-Refine y validación. Implementar aprendizaje de estrategias en memoria.py. Ejecutar validaciones de calidad con juez.py durante el evento.

## Próximos Pasos Inmediatos
1. Completar notebook de pruebas.
2. Verificar memoria.py y juez.py.
3. Integrar LangGraph en agente.py.
4. Verificación final: Instalar dependencias y configurar .env.

## Notas Finales
- Todo pre-evento es compliant: Solo infraestructura, sin violaciones.
- Enfoque: Maximizar preparación para ejecutar lógica en evento y ganar.
- Contacto: Equipo listo para hackathon el 23 de octubre de 2025.