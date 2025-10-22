# Este archivo contiene las respuestas "perfectas"
# que usaremos para la demo final, garantizando
# velocidad y resultados consistentes.

# (Se llenarán con datos reales durante el evento del hackathon)
RESPUESTAS_CACHE = {
    "run_1_caro": {
        "respuesta": "Esta es la respuesta larga y detallada de GPT-4 (demo)...",
        "metricas": {
            "modelo_usado": "gpt-4-turbo",
            "tokens_prompt": 500,
            "tokens_completion": 200,
            "tokens_totales": 700,
            "latencia_segundos": 4.5123,
            "error": None
        }
    },
    "run_2_barato": {
        "respuesta": "Esta es la respuesta corta y eficiente de GPT-3.5 (demo)...",
        "metricas": {
            "modelo_usado": "gpt-3.5-turbo",
            "tokens_prompt": 500,
            "tokens_completion": 50,
            "tokens_totales": 550,
            "latencia_segundos": 0.8123,
            "error": None
        }
    },
    "auditor_feedback": {
        "respuesta": '{"analisis": "Se usó un modelo caro para una tarea simple.", "accion_recomendada": "MEJORAR", "modelo_recomendado": "gpt-3.5-turbo"}',
        "metricas": {
            "modelo_usado": "gpt-3.5-turbo",
            "tokens_prompt": 250,
            "tokens_completion": 40,
            "tokens_totales": 290,
            "latencia_segundos": 0.5123,
            "error": None
        }
    }
}