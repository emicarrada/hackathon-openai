import time
from src.utils import client  # Importamos el cliente ya inicializado
from openai import OpenAI
import openai  # Importar la biblioteca base para los tipos de error
from .demo_cache import RESPUESTAS_CACHE  # Importar el cache

# --- INTERRUPTOR GLOBAL PARA MODO DEMO ---
# El jueves, para la demo final, pondremos esto en True.
# Durante el desarrollo, lo dejamos en False para usar llamadas reales.
MODO_DEMO = False

from typing import Tuple

def medir_llamada_llm(modelo: str, mensajes: list, cache_key: str = None) -> Tuple[str, dict]:
    """
    Realiza una llamada a la API de OpenAI, mide la latencia,
    captura el uso de tokens y MANEJA ERRORES.

    Args:
        modelo (str): El ID del modelo a usar (ej. "gpt-4-turbo")
        mensajes (list): La lista de mensajes en formato OpenAI
        cache_key (str, optional): Clave para usar datos del cache en modo demo

    Retorna:
        (str/None, dict): El contenido de la respuesta o None si hay error,
                         y un diccionario con las métricas de ejecución
    """
    # --- LÓGICA DEL MODO DEMO ---
    if MODO_DEMO and cache_key:
        print(f"\n*** MODO DEMO ACTIVADO (Usando cache: {cache_key}) ***\n")
        if cache_key in RESPUESTAS_CACHE:
            data = RESPUESTAS_CACHE[cache_key]
            # Simular una pequeña pausa para que se vea realista
            time.sleep(0.5)
            return data["respuesta"], data["metricas"]
        else:
            print(f"Error de Cache: Clave '{cache_key}' no encontrada.")
            return "Error: Clave de cache no encontrada", {"error": "Cache key inválida"}

    if not client:
        error_msg = "Cliente de OpenAI no inicializado."
        return None, {"error": error_msg, "tokens_totales": 0, "latencia_segundos": 0}

    metricas_base = {
        "modelo_usado": modelo,
        "tokens_prompt": 0,
        "tokens_completion": 0,
        "tokens_totales": 0,
        "latencia_segundos": 0,
        "error": None
    }

    try:
        start_time = time.time()

        respuesta = client.chat.completions.create(
            model=modelo,
            messages=mensajes
        )

        end_time = time.time()

        # Llenar métricas en caso de éxito
        metricas_base["latencia_segundos"] = round(end_time - start_time, 4)
        metricas_base["tokens_prompt"] = respuesta.usage.prompt_tokens
        metricas_base["tokens_completion"] = respuesta.usage.completion_tokens
        metricas_base["tokens_totales"] = respuesta.usage.total_tokens

        contenido_respuesta = respuesta.choices[0].message.content

        return contenido_respuesta, metricas_base

    # ---- MANEJO DE ERRORES ESPECÍFICOS ----
    except openai.AuthenticationError as e:
        print(f"ERROR: API Key inválida o faltante. {e}")
        metricas_base["error"] = "AuthenticationError"
        return None, metricas_base

    except openai.RateLimitError as e:
        print(f"ERROR: Límite de tasa de API alcanzado. {e}")
        metricas_base["error"] = "RateLimitError"
        return None, metricas_base

    except openai.APIConnectionError as e:
        print(f"ERROR: No se pudo conectar a OpenAI. {e}")
        metricas_base["error"] = "APIConnectionError"
        return None, metricas_base

    except Exception as e:
        print(f"ERROR: Error inesperado en la llamada a la API: {e}")
        metricas_base["error"] = str(e)
        return None, metricas_base