# 🔧 Instrucciones de Rebase para Brandon (Windows)

## ⚠️ CONTEXTO IMPORTANTE

Tu rama `brandon/evaluador` tiene **conflictos** porque trabajaste sobre una versión antigua de main.

**Tu trabajo YA ESTÁ INTEGRADO en main** con correcciones aplicadas:
- ✅ `src/nodos/evaluar_complejidad.py` - Integrado con modelos corregidos (gpt-4o, gpt-4o-mini)
- ✅ `tests/test_evaluador.py` - Integrado con tests actualizados

**El problema**: Tu rama borró archivos importantes de tus compañeros (-1,385 líneas).

---

## 📝 COMANDOS PARA WINDOWS (Git Bash o PowerShell)

### **Opción 1: Rebase Automático (RECOMENDADO)**

Ejecuta estos comandos **uno por uno** en la raíz del proyecto:

```bash
# 1. Actualizar main local
git checkout main
git pull origin main

# 2. Eliminar tu rama local vieja y recrearla desde main actualizado
git branch -D brandon/evaluador
git checkout -b brandon/evaluador

# 3. Forzar push para sincronizar con origin (tu rama remota)
git push origin brandon/evaluador --force
```

**¿Qué hace esto?**
- Elimina tu rama vieja con conflictos
- Crea una nueva rama `brandon/evaluador` desde main actualizado
- Ahora tienes TODO el trabajo del equipo + tu evaluador ya integrado
- Puedes trabajar sobre esta base limpia

---

### **Opción 2: Rebase Manual (Si quieres aprender)**

Si prefieres hacer rebase tradicional:

```bash
# 1. Actualizar main
git checkout main
git pull origin main

# 2. Ir a tu rama
git checkout brandon/evaluador

# 3. Hacer rebase
git rebase main

# 4. Durante el rebase, cuando aparezcan conflictos:
#    - Acepta SIEMPRE la versión de main para archivos que no son tuyos
#    - Para evaluar_complejidad.py, acepta la versión de main (ya tiene tus cambios corregidos)

# 5. Después de resolver cada conflicto:
git add .
git rebase --continue

# 6. Cuando termine el rebase:
git push origin brandon/evaluador --force-with-lease
```

---

## ❌ ARCHIVOS QUE **NO DEBES ELIMINAR**

Durante el rebase, si Git te pregunta sobre estos archivos, **MANTÉNLOS**:

- `src/juez.py` (Cristopher)
- `src/nodos/validar_calidad.py` (Cristopher)
- `src/prompts.py` (Israel)
- `src/nodos/generar_refinar.py` (Israel)
- `comparar_api_keys.py` (Cristopher)
- `diagnostico_modelos.py` (Cristopher)

---

## ✅ LO QUE YA ESTÁ EN MAIN

Tu evaluador fue integrado con estas **correcciones aplicadas**:

```python
# ANTES (tu versión original):
modelo = "gpt-4"              # Para complejidad alta
modelo = "gpt-3.5-turbo"      # Para complejidad media

# DESPUÉS (versión corregida en main):
modelo = "gpt-4o"             # Para complejidad alta
modelo = "gpt-4o-mini"        # Para complejidad media
```

**Razón**: El equipo usa modelos optimizados: `gpt-4o-mini` (baja/media), `gpt-4o` (alta), `gpt-4.1` (baseline).

---

## 🎯 DESPUÉS DEL REBASE

Una vez que tu rama esté actualizada:

1. **Verifica que tienes todo**:
   ```bash
   git log --oneline -5
   # Deberías ver los commits de integración de Israel y tuyo
   ```

2. **Verifica que no borraste nada**:
   ```bash
   git diff main
   # No debería mostrar eliminaciones, solo cambios menores si los hiciste
   ```

3. **Trabaja sobre esta base limpia**:
   - Ahora tienes los 3 nodos completos
   - Puedes hacer mejoras a tu evaluador
   - Puedes agregar nuevas features

---

## 🆘 SI ALGO SALE MAL

**Abortar el rebase**:
```bash
git rebase --abort
```

**Volver al estado original**:
```bash
git reset --hard origin/brandon/evaluador
```

**Pedir ayuda a Cristopher** 😉

---

## 📊 ESTADO ACTUAL DEL PROYECTO

```
✅ Sistema 100% completo con 3 nodos:
1. Evaluador (Brandon)    → Clasificación de complejidad
2. Generador (Israel)     → Generación con cache + refinamiento  
3. Validador (Cristopher) → Validación de calidad + métricas

✅ Modelos optimizados: gpt-4o-mini, gpt-4o, gpt-4.1
✅ Estrategias JSON actualizadas
✅ Tests para cada nodo
```

---

**Última actualización**: 23 oct 2025  
**Responsable de integración**: Cristopher (Hub/Validador)
