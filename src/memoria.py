"""
Sistema de Memoria Estratégica

Almacena estrategias aprendidas en formato JSON para optimización de modelos.
Implementado durante el Hackathon OpenAI (23 oct 2025).
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime


class Memoria:
    """
    Maneja el almacenamiento y recuperación de estrategias aprendidas.
    """

    def __init__(self, archivo: str = "data/estrategias.json"):
        self.archivo = archivo
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(archivo), exist_ok=True)
        self.datos = self.cargar()

    def cargar(self) -> dict:
        """
        Carga estrategias desde archivo JSON.
        
        Returns:
            dict: Estrategias almacenadas o dict vacío si no existe.
        """
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️ Error cargando memoria: {e}")
                return {}
        return {}

    def guardar(self):
        """Guarda estrategias en archivo JSON."""
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(self.datos, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"❌ Error guardando memoria: {e}")

    def consultar_estrategia(self, tipo_tarea: str) -> Optional[Dict[str, Any]]:
        """
        Consulta si existe estrategia para un tipo de tarea.
        
        Args:
            tipo_tarea (str): Tipo de tarea (ej: "resumen", "traduccion").
            
        Returns:
            dict | None: Estrategia encontrada o None.
        """
        return self.datos.get(tipo_tarea)

    def agregar_estrategia(self, tipo_tarea: str, modelo: str, 
                          tokens: Optional[int] = None, 
                          latencia: Optional[float] = None):
        """
        Agrega o actualiza estrategia aprendida.
        
        Args:
            tipo_tarea (str): Tipo de tarea.
            modelo (str): Modelo recomendado (ej: "gpt-3.5-turbo").
            tokens (int, optional): Tokens usados.
            latencia (float, optional): Latencia en segundos.
        """
        # Si ya existe, actualizar con promedios
        if tipo_tarea in self.datos:
            estrategia = self.datos[tipo_tarea]
            
            if tokens is not None:
                tokens_ant = estrategia.get("tokens_promedio", tokens)
                estrategia["tokens_promedio"] = (tokens_ant + tokens) // 2
            
            if latencia is not None:
                lat_ant = estrategia.get("latencia_promedio", latencia)
                estrategia["latencia_promedio"] = round((lat_ant + latencia) / 2, 2)
            
            estrategia["modelo"] = modelo
            estrategia["ultima_actualizacion"] = datetime.now().isoformat()
        else:
            # Crear nueva
            self.datos[tipo_tarea] = {
                "modelo": modelo,
                "tokens_promedio": tokens or 0,
                "latencia_promedio": latencia or 0.0,
                "ultima_actualizacion": datetime.now().isoformat()
            }
        
        self.guardar()

    def limpiar(self):
        """Limpia todas las estrategias (útil para demos)."""
        self.datos = {}
        self.guardar()

    def estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de las estrategias.
        
        Returns:
            dict: Total, tipos de tarea, modelos usados, promedios.
        """
        if not self.datos:
            return {"total": 0, "tipos": []}
        
        modelos = set()
        tokens_total = 0
        latencia_total = 0.0
        
        for est in self.datos.values():
            modelos.add(est.get("modelo", "desconocido"))
            tokens_total += est.get("tokens_promedio", 0)
            latencia_total += est.get("latencia_promedio", 0.0)
        
        return {
            "total": len(self.datos),
            "tipos": list(self.datos.keys()),
            "modelos": list(modelos),
            "tokens_promedio": tokens_total // len(self.datos),
            "latencia_promedio": round(latencia_total / len(self.datos), 2)
        }