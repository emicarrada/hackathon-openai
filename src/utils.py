# Cliente OpenAI inicializado y autenticado
from openai import OpenAI
import os

# Inicializar cliente de OpenAI con la API key del entorno
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))