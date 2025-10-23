# 🔑 Cómo Comparar API Keys del Equipo

## 🎯 Propósito

Este script te permite verificar si tú e Israel (o Brandon) tienen:
- La misma API key o diferentes
- Los mismos modelos disponibles
- Los mismos permisos (GPT-4, GPT-4o, etc.)

## 📋 Cómo Usarlo

### Paso 1: Ejecutar el script

```bash
python comparar_api_keys.py
```

### Paso 2: Ver tu información

El script analizará tu API key del `.env` y mostrará:
- Hash único (identificador seguro)
- Total de modelos GPT disponibles
- Acceso a GPT-4, GPT-4o, GPT-4.1
- Tier estimado de tu cuenta

### Paso 3: Pedir API key al compañero

Pídele a Israel (o Brandon) que:
1. Abra su `.env`
2. Copie su `OPENAI_API_KEY=...`
3. Te la envíe por Slack/WhatsApp

### Paso 4: Pegar la API key

Cuando el script te pregunte:
```
API Key del compañero:
```

Pega la API key completa de tu compañero.

### Paso 5: Ver la comparación

El script te mostrará:

✅ **Si son la misma key:**
```
✅ ¡SON LA MISMA API KEY!
   • Hash: 6f9d70d07f43df91
   • Ambos deberían ver los mismos modelos
```

⚠️ **Si son diferentes:**
```
⚠️  SON API KEYS DIFERENTES
   • TU API KEY: 6f9d70d07f43df91
   • API KEY DEL COMPAÑERO: a3b2c1d4e5f6g7h8

📊 DIFERENCIAS EN MODELOS:
   • TU API KEY: 61 modelos
   • API KEY DEL COMPAÑERO: 3 modelos

🔍 CAPACIDADES:
   • GPT-4       → TU API KEY: ✅  |  COMPAÑERO: ❌
   • GPT-4o      → TU API KEY: ✅  |  COMPAÑERO: ❌
   • GPT-4.1     → TU API KEY: ✅  |  COMPAÑERO: ❌

💡 RECOMENDACIÓN:
   Para el hackathon, usa TU API KEY:
   • Tiene más modelos (61 vs 3)
   • Mejor tier (Tier 4-5 (Alto))
   • Compartir tu .env con todo el equipo
```

## 🎯 Casos de Uso

### Caso 1: Verificar si Israel usa tu misma key

Si Israel ya tiene tu `.env`, deberían ver:
- ✅ Mismo hash
- ✅ Mismos 61 modelos
- ✅ Mismo tier

### Caso 2: Israel tiene su propia key diferente

Si tiene una key diferente:
- ⚠️ Diferentes hashes
- ⚠️ Probablemente menos modelos (3 vs 61)
- ⚠️ Sin acceso a GPT-4

**Solución:** Compartir tu `.env` con él.

### Caso 3: Brandon tiene otra key

Mismo proceso, puedes comparar con cualquier miembro del equipo.

## 🔒 Seguridad

- El script NO guarda las API keys
- Solo las usa para comparar
- Muestra hashes en vez de keys completas
- Seguro para compartir resultados

## 💡 Recomendación Final

**Para el hackathon:**
1. Ejecuta `python comparar_api_keys.py` con cada miembro
2. Identifica quién tiene la mejor API key (más modelos)
3. Comparte ese `.env` con todo el equipo
4. Así todos tienen acceso a los mismos modelos
5. Las demos serán más consistentes y de mejor calidad

## 📞 Ejemplo de Mensaje para el Equipo

```
Hey @israel @brandon,

Por favor ejecuten:
  python comparar_api_keys.py

Y cuando les pida, peguen su OPENAI_API_KEY para comparar.
Así verificamos que todos tenemos los mismos modelos disponibles.

Pueden también solo enviarme su API key por DM y yo hago la comparación.
```

---

**Autor:** Cristopher (Hub)  
**Fecha:** 23 oct 2025  
**Hackathon:** OpenAI Smart Optimizer
