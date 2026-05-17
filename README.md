# Formatflux

**Formatflux** es un sistema de procesamiento multimedia completo que combina una potente CLI con capacidades de conversión, procesamiento de video/audio, y generación automática de subtítulos mediante IA.

## Características Principales

- 🎬 **Conversión multimedia**: Video, audio e imágenes entre múltiples formatos
- 🎯 **Chroma Key**: Eliminación de fondo verde/azul en videos
- 📝 **Subtítulos automáticos**: Generación con Whisper IA
- 🔊 **Procesamiento de audio**: Normalización, recorte, mezcla
- 🖼️ **Extracción de frames**: Captura de fotogramas a intervalos personalizados
- ⚡ **Batch processing**: Procesamiento por lotes eficiente

## Stack Tecnológico

- **Python 3.12+** - Lenguaje principal
- **PyQt6 6.11.0** - GUI (en desarrollo)
- **FFmpeg** - Motor de procesamiento multimedia
- **OpenCV** - Procesamiento visual
- **Whisper** - Subtítulos con IA
- **Typer** - Interfaz CLI

## Instalación

### Requisitos Previos

```bash
sudo apt install ffmpeg  # Ubuntu/Debian
```

### Instalación del Proyecto

```bash
cd /home/wcun/.hermes/workspace/FormatFlux
uv pip install -e ".[dev]"
```

## Uso

### CLI Básico

```bash
formatflux version
formatflux info video.mp4
formatflux convert input.mp4 output.avi
formatflux chroma-key input.mp4 output.mp4 --color green
formatflux subtitles-generate video.mp4 subtitles.srt --language es
formatflux audio-normalize audio.mp3 output.mp3
formatflux extract-frames video.mp4 ./frames --fps 1
```

## Componentes Principales

### MediaConverter
Maneja la conversión entre formatos multimedia utilizando FFmpeg.

### VideoProcessor
Procesamiento avanzado de video:
- Chroma key (color key)
- Generación de subtítulos con IA (Whisper)
- Incrustación de subtítulos
- Extracción de fotogramas

### AudioProcessor
Manipulación de audio:
- Normalización de volumen (EBU R128)
- Recorte preciso
- Conversión de formatos
- Mezcla de múltiples pistas

## Estructura del Proyecto

```
formatflux/
├── README.md
├── ARQUITECTURA.md
├── CONTRIBUTING.md
├── pyproject.toml
├── .gitignore
└── src/
    └── formatflux/
        ├── __init__.py
        ├── cli/
        │   ├── __init__.py
        │   └── main.py
        └── core/
            ├── __init__.py
            ├── converter.py
            └── processor.py
```

## Contribución

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

## Arquitectura

Ver [ARQUITECTURA.md](ARQUITECTURA.md) para más detalles sobre el diseño del sistema.