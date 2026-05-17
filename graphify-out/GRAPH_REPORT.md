# Graph Report - FormatFlux  (2026-05-17)

## Corpus Check
- Corpus is ~2,337 words - fits in a single context window. You may not need a graph.

## Summary
- 57 nodes · 52 edges · 8 communities (3 shown, 5 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]

## God Nodes (most connected - your core abstractions)
1. `VideoProcessor` - 7 edges
2. `AudioProcessor` - 7 edges
3. `MediaConverter` - 6 edges
4. `_format_timestamp()` - 2 edges
5. `Formatflux - Sistema de procesamiento multimedia.` - 1 edges
6. `CLI module for Formatflux.` - 1 edges
7. `CLI principal de Formatflux.` - 1 edges
8. `Core processing modules for Formatflux.` - 1 edges
9. `MediaConverter - Motor de conversión multimedia basado en FFmpeg.` - 1 edges
10. `Conversor multimedia basado en FFmpeg.` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (8 total, 5 thin omitted)

### Community 1 - "Community 1"
Cohesion: 0.15
Nodes (8): _format_timestamp(), Processors - Procesadores de video y audio., Procesador de archivos de video., Aplica chroma key (pantalla verde/azul) a un video., Incrusta subtítulos en un video., Genera subtítulos automáticamente usando Whisper IA., Extrae fotogramas de un video., VideoProcessor

### Community 2 - "Community 2"
Cohesion: 0.2
Nodes (6): MediaConverter, MediaConverter - Motor de conversión multimedia basado en FFmpeg., Conversor multimedia basado en FFmpeg., Convierte un archivo multimedia., Obtiene información de un archivo multimedia., Convierte múltiples archivos en un directorio.

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (6): AudioProcessor, Procesador de archivos de audio., Normaliza el volumen de un archivo de audio., Recorta un archivo de audio., Convierte el formato de un archivo de audio., Mezcla múltiples archivos de audio.

## Knowledge Gaps
- **21 isolated node(s):** `Formatflux - Sistema de procesamiento multimedia.`, `CLI module for Formatflux.`, `CLI principal de Formatflux.`, `Core processing modules for Formatflux.`, `MediaConverter - Motor de conversión multimedia basado en FFmpeg.` (+16 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AudioProcessor` connect `Community 3` to `Community 1`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **What connects `Formatflux - Sistema de procesamiento multimedia.`, `CLI module for Formatflux.`, `CLI principal de Formatflux.` to the rest of the system?**
  _21 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._