# INSTRUCCIONES PARA ISRAEL - DIAGNÓSTICO DE MODELOS

## 🎯 OBJETIVO
Verificar qué modelos GPT tienes disponibles en tu API key y configurar el proyecto correctamente.

---

## 📋 PASO 1: EJECUTAR DIAGNÓSTICO

Abre una terminal en la raíz del proyecto y ejecuta:

```bash
python diagnostico_modelos.py
```

Esto te mostrará:
- ✅ Cuántos modelos GPT tienes disponibles
- ✅ Lista completa de modelos
- ✅ Cuáles modelos funcionan para el proyecto
- ✅ Recomendaciones específicas

---

## 🔍 PASO 2: INTERPRETAR RESULTADOS

### ESCENARIO A: Tienes 61 modelos (igual que Cristopher)
```
📊 TOTAL DE MODELOS GPT ENCONTRADOS: 61
✅ gpt-4o-mini - FUNCIONA
✅ gpt-4o - FUNCIONA
✅ gpt-4.1 - FUNCIONA
```

**ACCIÓN:** ¡Todo bien! Tu configuración ya está correcta. Usa:
- `data/estrategias.json` tal como está

---

### ESCENARIO B: Solo tienes gpt-3.5-turbo (1-2 modelos)
```
📊 TOTAL DE MODELOS GPT ENCONTRADOS: 1-2
✅ gpt-3.5-turbo - FUNCIONA
❌ gpt-4o-mini - NO EXISTE
❌ gpt-4o - NO EXISTE
```

**PROBLEMA:** API key con acceso limitado (free tier o sin créditos)

**SOLUCIÓN RÁPIDA:** Actualiza `data/estrategias.json`:
```json
{
  "estrategias": {
    "baja": "gpt-3.5-turbo",
    "media": "gpt-3.5-turbo",
    "alta": "gpt-3.5-turbo"
  },
  "notas": "Usando gpt-3.5-turbo para todas las complejidades (limitación de API key)"
}
```

**PARA LA DEMO:** El proyecto sigue funcionando, pero:
- No puedes demostrar diferencia entre modelos
- Enfócate en el Self-Refine y validación con Juez
- Menciona que en producción usarías modelos diferentes

---

### ESCENARIO C: Tienes gpt-3.5 y gpt-4 (5-10 modelos)
```
📊 TOTAL DE MODELOS GPT ENCONTRADOS: 5-10
✅ gpt-3.5-turbo - FUNCIONA
✅ gpt-4 - FUNCIONA
❌ gpt-4o-mini - NO EXISTE
```

**ACCIÓN:** Actualiza `data/estrategias.json`:
```json
{
  "estrategias": {
    "baja": "gpt-3.5-turbo",
    "media": "gpt-4",
    "alta": "gpt-4"
  },
  "notas": "Configuración para cuenta con acceso a GPT-4 estándar"
}
```

---

## 🔧 PASO 3: VERIFICAR CAUSA SI TIENES MENOS MODELOS

### Razones comunes:

1. **Free tier de OpenAI**
   - Solo acceso a gpt-3.5-turbo
   - **Solución:** Agregar método de pago en platform.openai.com

2. **Sin créditos**
   - La cuenta no tiene balance
   - **Solución:** Agregar $5-10 USD de créditos

3. **API key antigua**
   - Creada antes de lanzamiento de gpt-4o
   - **Solución:** Generar nueva API key

4. **Restricciones de organización**
   - La org limita acceso a modelos
   - **Solución:** Hablar con admin o crear cuenta personal

---

## 🎯 PASO 4: SOLUCIÓN INMEDIATA PARA EL HACKATHON

### Si NO puedes resolver el acceso a modelos:

**OPCIÓN 1:** Usa la API key de Cristopher (para equipo)
- Actualiza tu `.env` con la misma key

**OPCIÓN 2:** Adapta el código para tu situación
```python
# En src/nodos/evaluar_complejidad.py
def evaluar_complejidad(tarea: str) -> dict:
    # Siempre usa gpt-3.5-turbo
    return {
        "complejidad": "baja",  # Siempre baja
        "modelo": "gpt-3.5-turbo"
    }
```

**OPCIÓN 3:** Mock/Simulación
- Usa respuestas cacheadas para la demo
- Activa `MODO_DEMO = True` en `src/contador.py`

---

## 📞 PASO 5: COMUNICAR RESULTADOS

Después de ejecutar el diagnóstico, comparte con el equipo:

```
🔍 DIAGNÓSTICO - Israel:
- Modelos disponibles: [número]
- Modelos funcionales: [lista]
- Configuración aplicada: [opción A/B/C]
- ¿Necesito ayuda?: [Sí/No]
```

---

## 💡 PREGUNTAS PARA COPILOT (si necesitas más ayuda)

Copia y pega esto en tu Copilot:

```
Ejecuté diagnostico_modelos.py y obtuve:
[PEGA AQUÍ EL OUTPUT COMPLETO]

¿Cuál es el problema y cómo lo resuelvo para el hackathon?
```

---

## ✅ CHECKLIST FINAL

- [ ] Ejecuté `diagnostico_modelos.py`
- [ ] Verifiqué cuántos modelos tengo
- [ ] Actualicé `data/estrategias.json` según mis modelos
- [ ] Probé que mi configuración funciona
- [ ] Comuniqué resultados al equipo

---

**¿Dudas?** Pregunta en el chat del equipo con el output del diagnóstico.
