"""
Script para comparar API Keys de OpenAI entre miembros del equipo.

Uso:
    python comparar_api_keys.py

Este script:
1. Verifica tu API key actual (.env)
2. Te permite comparar con otra API key
3. Muestra diferencias en modelos y permisos
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import hashlib

def hash_api_key(api_key: str) -> str:
    """Crea un hash de la API key para comparación segura (sin mostrar la key completa)."""
    return hashlib.sha256(api_key.encode()).hexdigest()[:16]

def analizar_api_key(api_key: str, nombre: str = "API Key") -> dict:
    """
    Analiza una API key y retorna información detallada.
    
    Returns:
        dict con: modelos_gpt, total_modelos, hash, primeros_chars, longitud, tier_estimado
    """
    try:
        print(f"\n{'='*70}")
        print(f"🔍 ANALIZANDO: {nombre}")
        print(f"{'='*70}")
        
        client = OpenAI(api_key=api_key)
        
        # Obtener info básica
        primeros_10 = api_key[:10] + "..."
        longitud = len(api_key)
        key_hash = hash_api_key(api_key)
        
        print(f"   • Primeros caracteres: {primeros_10}")
        print(f"   • Longitud: {longitud} caracteres")
        print(f"   • Hash (identificador): {key_hash}")
        
        # Obtener modelos disponibles
        print(f"\n   🔄 Obteniendo modelos disponibles...")
        models = client.models.list()
        
        # Filtrar solo modelos GPT
        modelos_gpt = sorted([
            m.id for m in models.data 
            if m.id.startswith('gpt')
        ])
        
        total_modelos = len(modelos_gpt)
        
        # Determinar tier estimado basado en modelos disponibles
        tiene_gpt4 = any('gpt-4' in m for m in modelos_gpt)
        tiene_gpt4o = any('gpt-4o' in m for m in modelos_gpt)
        tiene_gpt41 = any('gpt-4.1' in m for m in modelos_gpt)
        
        if tiene_gpt41 or tiene_gpt4o:
            tier_estimado = "Tier 4-5 (Alto)"
        elif tiene_gpt4:
            tier_estimado = "Tier 2-3 (Medio)"
        else:
            tier_estimado = "Tier 1 (Básico)"
        
        print(f"\n   ✅ Análisis completado:")
        print(f"      • Total modelos GPT: {total_modelos}")
        print(f"      • Acceso GPT-4: {'✅ SÍ' if tiene_gpt4 else '❌ NO'}")
        print(f"      • Acceso GPT-4o: {'✅ SÍ' if tiene_gpt4o else '❌ NO'}")
        print(f"      • Acceso GPT-4.1: {'✅ SÍ' if tiene_gpt41 else '❌ NO'}")
        print(f"      • Tier estimado: {tier_estimado}")
        
        return {
            "nombre": nombre,
            "hash": key_hash,
            "primeros_chars": primeros_10,
            "longitud": longitud,
            "total_modelos": total_modelos,
            "modelos_gpt": modelos_gpt,
            "tiene_gpt4": tiene_gpt4,
            "tiene_gpt4o": tiene_gpt4o,
            "tiene_gpt41": tiene_gpt41,
            "tier_estimado": tier_estimado,
            "valida": True
        }
        
    except Exception as e:
        print(f"\n   ❌ Error al analizar: {str(e)}")
        return {
            "nombre": nombre,
            "hash": "ERROR",
            "error": str(e),
            "valida": False
        }

def comparar_api_keys(info1: dict, info2: dict):
    """Compara dos API keys y muestra diferencias."""
    print(f"\n{'='*70}")
    print(f"📊 COMPARACIÓN DE API KEYS")
    print(f"{'='*70}")
    
    # Verificar si son la misma key
    if info1["hash"] == info2["hash"]:
        print(f"\n✅ ¡SON LA MISMA API KEY!")
        print(f"   • Hash: {info1['hash']}")
        print(f"   • Ambos deberían ver los mismos modelos")
        return
    
    print(f"\n⚠️  SON API KEYS DIFERENTES")
    print(f"   • {info1['nombre']}: {info1['hash']}")
    print(f"   • {info2['nombre']}: {info2['hash']}")
    
    # Comparar modelos
    print(f"\n📊 DIFERENCIAS EN MODELOS:")
    print(f"   • {info1['nombre']}: {info1['total_modelos']} modelos")
    print(f"   • {info2['nombre']}: {info2['total_modelos']} modelos")
    
    # Comparar capacidades específicas
    print(f"\n🔍 CAPACIDADES:")
    
    capacidades = [
        ("GPT-4", "tiene_gpt4"),
        ("GPT-4o", "tiene_gpt4o"),
        ("GPT-4.1", "tiene_gpt41"),
    ]
    
    for nombre, campo in capacidades:
        val1 = "✅" if info1.get(campo) else "❌"
        val2 = "✅" if info2.get(campo) else "❌"
        print(f"   • {nombre:12} → {info1['nombre']}: {val1}  |  {info2['nombre']}: {val2}")
    
    # Comparar tiers
    print(f"\n🎯 TIER:")
    print(f"   • {info1['nombre']}: {info1['tier_estimado']}")
    print(f"   • {info2['nombre']}: {info2['tier_estimado']}")
    
    # Modelos exclusivos
    if info1['total_modelos'] != info2['total_modelos']:
        modelos1 = set(info1['modelos_gpt'])
        modelos2 = set(info2['modelos_gpt'])
        
        solo_en_1 = modelos1 - modelos2
        solo_en_2 = modelos2 - modelos1
        
        if solo_en_1:
            print(f"\n📋 MODELOS SOLO EN {info1['nombre']} ({len(solo_en_1)}):")
            for modelo in sorted(solo_en_1)[:10]:  # Mostrar primeros 10
                print(f"      • {modelo}")
            if len(solo_en_1) > 10:
                print(f"      ... y {len(solo_en_1) - 10} más")
        
        if solo_en_2:
            print(f"\n📋 MODELOS SOLO EN {info2['nombre']} ({len(solo_en_2)}):")
            for modelo in sorted(solo_en_2)[:10]:  # Mostrar primeros 10
                print(f"      • {modelo}")
            if len(solo_en_2) > 10:
                print(f"      ... y {len(solo_en_2) - 10} más")
    
    # Recomendación
    print(f"\n{'='*70}")
    print(f"💡 RECOMENDACIÓN:")
    print(f"{'='*70}")
    
    if info1['total_modelos'] > info2['total_modelos']:
        print(f"\n   Para el hackathon, usa la API key de {info1['nombre']}:")
        print(f"   • Tiene más modelos ({info1['total_modelos']} vs {info2['total_modelos']})")
        print(f"   • Mejor tier ({info1['tier_estimado']})")
        print(f"   • Compartir el .env de {info1['nombre']} con todo el equipo")
    elif info2['total_modelos'] > info1['total_modelos']:
        print(f"\n   Para el hackathon, usa la API key de {info2['nombre']}:")
        print(f"   • Tiene más modelos ({info2['total_modelos']} vs {info1['total_modelos']})")
        print(f"   • Mejor tier ({info2['tier_estimado']})")
        print(f"   • Compartir el .env de {info2['nombre']} con todo el equipo")
    else:
        print(f"\n   Ambas API keys son equivalentes")
        print(f"   • Cualquiera puede usarse")
        print(f"   • Recomendado: usar una sola para todo el equipo")

def main():
    """Función principal."""
    print(f"{'='*70}")
    print(f"🔑 COMPARADOR DE API KEYS - HACKATHON OPENAI")
    print(f"{'='*70}")
    
    # Cargar API key del .env actual
    load_dotenv()
    api_key_actual = os.getenv("OPENAI_API_KEY")
    
    if not api_key_actual:
        print("\n❌ Error: No se encontró OPENAI_API_KEY en .env")
        sys.exit(1)
    
    # Analizar tu API key
    info_tuya = analizar_api_key(api_key_actual, "TU API KEY (.env)")
    
    if not info_tuya["valida"]:
        print("\n❌ No se pudo validar tu API key")
        sys.exit(1)
    
    # Preguntar por la otra API key
    print(f"\n{'='*70}")
    print(f"🔄 AHORA ANALIZA LA API KEY DE TU COMPAÑERO")
    print(f"{'='*70}")
    print(f"\nPídele a tu compañero que copie su API key aquí.")
    print(f"(No te preocupes, solo se comparará, no se guardará)")
    print(f"\nEscribe 'salir' para terminar sin comparar.\n")
    
    api_key_otra = input("API Key del compañero: ").strip()
    
    if api_key_otra.lower() == 'salir':
        print("\n👋 Saliendo sin comparar...")
        sys.exit(0)
    
    if not api_key_otra:
        print("\n⚠️  No se proporcionó API key. Mostrando solo tu información.")
        sys.exit(0)
    
    # Analizar la otra API key
    info_otra = analizar_api_key(api_key_otra, "API KEY DEL COMPAÑERO")
    
    if not info_otra["valida"]:
        print("\n❌ No se pudo validar la API key del compañero")
        sys.exit(1)
    
    # Comparar
    comparar_api_keys(info_tuya, info_otra)
    
    print(f"\n{'='*70}")
    print(f"✅ COMPARACIÓN COMPLETADA")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
