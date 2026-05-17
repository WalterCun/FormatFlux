# Diseño — FormatFlux

Decisiones de diseño y principios arquitectónicos del proyecto.

## Filosofía

**"Herramienta, no framework"** — FormatFlux prioriza la simplicidad y la composibilidad sobre la magia. Cada componente es independiente y puede usarse de forma aislada o encadenada.

## Principios

| Principio | Decision |
|-----------|----------|
| **FFmpeg como motor** | Todo el procesamiento multimedia pasa por FFmpeg. Sin reimplementaciones. |
| **CLI primero** | La interfaz CLI es la API real. La GUI se construye sobre ella. |
| **Sin estado** | Los procesadores no guardan estado entre ejecuciones. |
| **Errores explícitos** | Las excepciones se propagan hasta la CLI, que imprime el mensaje y sale con código != 0. |
| **Extensibilidad** | Nuevos formatos o filtros se agregan sin tocar la capa CLI. |

## Capas (Arquitectura en capas)

```
CLI (Typer)
  └─> Service Layer (futuro)
       └─> Core Layer
            ├─ MediaConverter
            ├─ VideoProcessor
            └─ AudioProcessor
                 └─> FFmpeg / Whisper / OpenCV
```

- **CLI** Solo parsea argumentos e imprime. No contiene lógica de negocio.
- **Service Layer** (pendiente) Orquesta múltiples procesadores en pipelines.
- **Core** Lógica pura, sin dependencia de CLI ni red.
- **Infrastructure** FFmpeg (CLI), Whisper (Python), OpenCV (Python).

## Patrones utilizados

| Patrón | Uso en FormatFlux |
|--------|-------------------|
| **Facade** | `MediaConverter` oculta complejidad de comandos FFmpeg |
| **Builder** | Construcción incremental del comando FFmpeg con `options: dict` |
| **Strategy** | `VideoProcessor`, `AudioProcessor` intercambiables |
| **Template Method** | Flujo común: validar entrada → ejecutar → retornar dict con `success` y `message` |

## Contrato de retorno

Todos los procesadores retornan `dict` con el mismo esquema mínimo:

```python
{
    "success": bool,
    "message": str,          # mensaje humano, apto para CLI
    "input": str,            # ruta de entrada
    "output": str,           # ruta de salida
    # ... campos específicos del procesador
}
```

## Manejo de errores

- `FileNotFoundError` → archivo de entrada no existe.
- `RuntimeError` → FFmpeg/FFprobe/Whisper devolvió error.
- `TimeoutError` → conversión excedió el límite (3600 s por defecto).
- `ValueError` → parámetros inválidos (ej: color de chroma key).

Ningún procesador captura excepciones genéricas silenciosas. Todo error visible en CLI.

## Configuración

- **FFmpeg path**: se detecta automáticamente (`shutil.which("ffmpeg")`) o se pasa por constructor.
- **Modelo Whisper**: parámetro `model` en `generate_subtitles_ai()` (tiny → large).
- **Nivel de normalización audio**: `target_level` en `normalize()` (default: -16.0 LUFS).

---

*Para cambios arquitectónicos mayores, abrir issue con etiqueta `architecture` y discutir en PR.*
