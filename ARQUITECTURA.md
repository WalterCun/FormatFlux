# Arquitectura de Formatflux

Formatflux sigue una arquitectura modular y extensible.

## Diagrama

```
CLI (Typer) → Service Layer → Core Layer (Converter, VideoProc, AudioProc) → FFmpeg/Whisper
```

## Capas

### CLI Layer (Typer)
- Parseo de comandos
- Validación de entradas
- Formateo de salida

### Service Layer
- Orquestación de operaciones
- Pipeline de procesamiento

### Core Layer

#### MediaConverter
- Conversión multimedia via FFmpeg
- Extracción de metadatos
- Batch processing

#### VideoProcessor
- Chroma key
- Subtítulos con IA (Whisper)
- Incrustación de subtítulos
- Extracción de frames

#### AudioProcessor
- Normalización (EBU R128)
- Recorte
- Conversión
- Mezcla

### Infrastructure
- FFmpeg (CLI)
- Whisper (Python)
- OpenCV (Python)

## Patrones
- Facade: MediaConverter simplifica FFmpeg
- Adapter: Capa Core adapta libs externas
- Builder: Construcción de comandos FFmpeg
- Strategy: Procesadores independientes

## Flujo: Conversión
CLI → Typer → MediaConverter.convert() → FFmpeg → Result

## Flujo: Subtítulos IA
CLI → VideoProcessor.generate_subtitles_ai() → Whisper.transcribe() → SRT → Result