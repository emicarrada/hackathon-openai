"""
Sistema de Memoria

Almacena estrategias aprendidas en formato JSON para mejorar decisiones futuras.

PRE-EVENTO: Stub vacío. Implementar lógica en evento.
"""

import json
import os

class Memoria:
    """
    Maneja el almacenamiento y recuperación de estrategias.
    """

    def __init__(self, archivo: str = "data/estrategias.json"):
        self.archivo = archivo
        self.datos = self.cargar()

    def cargar(self) -> dict:
        """Carga datos desde archivo JSON."""
        # STUB: Implementar en evento
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r') as f:
                return json.load(f)
        return {}

    def guardar(self):
        """Guarda datos en archivo JSON."""
        # STUB: Implementar en evento
        with open(self.archivo, 'w') as f:
            json.dump(self.datos, f, indent=4)

    def agregar_estrategia(self, tarea: str, estrategia: dict):
        """Agrega nueva estrategia aprendida."""
        # STUB: Implementar en evento
        self.datos[tarea] = estrategia
        self.guardar()