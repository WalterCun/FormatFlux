# GitFlow — FormatFlux

Estrategia de ramificación basada en GitFlow adaptada.

## Estructura de ramas

```
main      — Producción (código estable y desplegado)
qa        — Testing / Release candidate
dev       — Integración continua (rama base de desarrollo)
feature/* — Nuevas funcionalidades
bug/*     — Corrección de errores
issues/*  — Experimentos, pruebas o tareas pendientes
```

## Flujo de trabajo

### 1. Desarrollo de features

```bash
# Crear rama de feature desde dev
git checkout -b feature/nombre-funcionalidad dev

# Trabajar, hacer commit(s) con conventional commits
git commit -m "feat: agregar conversión de imágenes"

# Al terminar: abrir PR feature → dev
```

### 2. Corrección de bugs

```bash
# Si el bug está en producción (main):
git checkout -b bug/nombre-bug main

# Si el bug está en dev (aún no llegó a producción):
git checkout -b bug/nombre-bug dev

# Abrir PR: bug → main (para bugs críticos produccion) o bug → dev
```

### 3. Integración en QA

Una vez que `dev` tiene suficiente funcionalidad:

```bash
# Crear PR: dev → qa
# En QA se aprueba antes de pasar a producción
```

### 4. Release a producción

```bash
# Crear PR: qa → main
# Después de merge, etiquetar release:
git tag v1.0.0
git push origin v1.0.0
```

## Convenciones de nombres

| Tipo | Patrón | Ejemplo |
|------|--------|---------|
| Feature | `feature/<descripción>` | `feature/conversion-audio` |
| Bugfix | `bug/<descripción>` | `bug/crash-al-procesar-gif` |
| Issue/Task | `issues/<número-o-desc>` | `issues/42` |

## Reglas importantes

- **main** y **qa** están protegidas: no se hace push directo
- **dev** es la rama base de integración
- Los features se mergean a `dev` primero
- `qa` recibe desde `dev` solo cuando hay un release candidate
- `main` recibe desde `qa` después de aprobación

---

*Generado automáticamente — Revisar y ajustar según necesidades del equipo.*
