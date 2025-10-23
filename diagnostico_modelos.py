"""
Script de diagnóstico para verificar modelos GPT disponibles
Usar: python diagnostico_modelos.py
"""

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import os

# Verificar que la API key esté configurada
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY no está configurada en .env")
    exit(1)

print(f"✅ API Key encontrada (primeros 10 chars): {api_key[:10]}...")
print(f"✅ API Key longitud: {len(api_key)} caracteres\n")

# Inicializar cliente
try:
    client = OpenAI(api_key=api_key)
    print("✅ Cliente OpenAI inicializado correctamente\n")
except Exception as e:
    print(f"❌ ERROR al inicializar cliente: {e}")
    exit(1)

# Obtener todos los modelos
print("🔍 Obteniendo lista completa de modelos...\n")
print("=" * 70)

try:
    modelos = client.models.list()
    
    # Filtrar modelos GPT
    modelos_gpt = []
    for modelo in modelos.data:
        if 'gpt' in modelo.id.lower():
            modelos_gpt.append(modelo.id)
    
    modelos_gpt.sort()
    
    print(f"📊 TOTAL DE MODELOS GPT ENCONTRADOS: {len(modelos_gpt)}\n")
    
    if len(modelos_gpt) == 0:
        print("❌ NO SE ENCONTRARON MODELOS GPT")
        print("   Esto puede indicar un problema con la API key o permisos")
    else:
        print("📋 LISTA DE MODELOS GPT DISPONIBLES:")
        print("-" * 70)
        for i, modelo in enumerate(modelos_gpt, 1):
            print(f"{i:3}. {modelo}")
    
    print("\n" + "=" * 70)
    
    # Probar modelos clave
    print("\n🧪 PROBANDO MODELOS CLAVE PARA EL PROYECTO...\n")
    
    modelos_probar = [
        'gpt-3.5-turbo',
        'gpt-4o-mini',
        'gpt-4o',
        'gpt-4.1',
        'gpt-4',
        'gpt-4-turbo'
    ]
    
    modelos_funcionan = []
    
    for modelo in modelos_probar:
        try:
            response = client.chat.completions.create(
                model=modelo,
                messages=[{'role': 'user', 'content': 'Di hola'}],
                max_tokens=5
            )
            tokens = response.usage.total_tokens
            print(f"✅ {modelo:20} - FUNCIONA ({tokens} tokens)")
            modelos_funcionan.append(modelo)
        except Exception as e:
            error_msg = str(e)
            if "does not exist" in error_msg or "not found" in error_msg:
                print(f"❌ {modelo:20} - NO EXISTE")
            elif "permission" in error_msg.lower():
                print(f"⚠️  {modelo:20} - SIN PERMISOS")
            else:
                print(f"❌ {modelo:20} - ERROR: {error_msg[:40]}...")
    
    print("\n" + "=" * 70)
    print(f"\n📊 RESUMEN:")
    print(f"   Total modelos GPT disponibles: {len(modelos_gpt)}")
    print(f"   Modelos probados que funcionan: {len(modelos_funcionan)}")
    print(f"   Modelos funcionales: {', '.join(modelos_funcionan) if modelos_funcionan else 'Ninguno'}")
    
    # Recomendaciones
    print("\n💡 RECOMENDACIONES PARA EL PROYECTO:")
    print("-" * 70)
    
    if 'gpt-4o-mini' in modelos_funcionan:
        print("✅ Usar gpt-4o-mini para complejidad BAJA (mejor que 3.5)")
    elif 'gpt-3.5-turbo' in modelos_funcionan:
        print("⚠️  Usar gpt-3.5-turbo para complejidad BAJA (gpt-4o-mini no disponible)")
    
    if 'gpt-4o' in modelos_funcionan:
        print("✅ Usar gpt-4o para complejidad MEDIA")
    elif 'gpt-4-turbo' in modelos_funcionan:
        print("⚠️  Usar gpt-4-turbo para complejidad MEDIA (gpt-4o no disponible)")
    
    if 'gpt-4.1' in modelos_funcionan:
        print("✅ Usar gpt-4.1 para complejidad ALTA")
    elif 'gpt-4o' in modelos_funcionan:
        print("⚠️  Usar gpt-4o para complejidad ALTA (gpt-4.1 no disponible)")
    elif 'gpt-4' in modelos_funcionan:
        print("⚠️  Usar gpt-4 para complejidad ALTA")
    
    print("\n" + "=" * 70)
    
except Exception as e:
    print(f"❌ ERROR al obtener modelos: {e}")
    print("\nPosibles causas:")
    print("1. API key inválida o expirada")
    print("2. Problemas de conexión a internet")
    print("3. Límite de rate excedido")
    print("4. Cuenta OpenAI sin créditos")

print("\n✅ Diagnóstico completado")
print("\nSi ves diferencias con otro equipo, compara:")
print("- La API key que están usando")
print("- El tipo de cuenta OpenAI (free tier vs paid)")
print("- La región/organización de la cuenta")
