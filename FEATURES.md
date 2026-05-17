# Features — FormatFlux

Estado de funcionalidades del proyecto (v1.0.0).

## ✅ Implementado

### Conversión multimedia
- [x] Conversión de video entre formatos (FFmpeg)
- [x] Conversión de audio entre formatos
- [x] Conversión de imágenes
- [x] Batch processing por directorio
- [x] Obtención de metadatos de archivos

### Procesamiento de video
- [x] Chroma key (pantalla verde/azul)
- [x] Incrustación de subtítulos en video
- [x] Extracción de fotogramas a intervalos personalizados

### Procesamiento de audio
- [x] Normalización de volumen (EBU R128)
- [x] Recorte de segmentos de audio
- [x] Mezcla de múltiples pistas de audio

### Subtítulos con IA
- [x] Transcripción automática con Whisper
- [x] Generación de archivos SRT
- [x] Selección de modelo Whisper (tiny, base, small, medium, large)
- [x] Soporte multi-idioma

### CLI
- [x] 10 comandos Typer
- [x] Validación de archivos de entrada
- [x] Mensajes de progreso y confirmación

---

## 🚧 En progreso / Planeado

### v1.1 — Estabilidad
- [ ] Suite de tests unitarios y de integración
- [ ] GitHub Actions CI/CD
- [ ] Pre-commit hooks (black, ruff, mypy)
- [ ] Manejo de errores más granular

### v1.2 — Funcionalidades adicionales
- [ ] Procesamiento por lotes con colas
- [ ] Presets de conversión predefinidos
- [ ] Logging a archivo con niveles configurables
- [ ] Modo dry-run (previsualizar sin ejecutar)

### v2.0 — GUI e IA
- [ ] Interfaz gráfica PyQt6
- [ ] Pipeline de procesamiento personalizable
- [ ] Procesamiento multi-hilo / asincrónico
- [ ] API REST (FastAPI)
- [ ] Plugin system para procesadores personalizados

---

## 🎯 Idea inicial (backlog)

- Crossfade entre clips de audio
- Extracción de audio de video
- Generación de thumbnails automáticos
- Detección de silencios en video
- Overlay de logos/marcas de agua

---

*Para agregar una feature: crear rama `feature/<nombre>` y abrir PR hacia `dev`.*
