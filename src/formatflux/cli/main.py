"""CLI principal de Formatflux."""
import typer
from pathlib import Path
from formatflux.core.converter import MediaConverter
from formatflux.core.processor import VideoProcessor, AudioProcessor

app = typer.Typer(name="formatflux", help="Formatflux - Procesamiento multimedia", epilog="Ej: formatflux convert video.mp4 video.avi")

try:
    converter = MediaConverter()
    video_proc = VideoProcessor()
    audio_proc = AudioProcessor()
except RuntimeError as e:
    print(f"Advertencia: {e}. Algunas funciones no disponibles.")
    converter = video_proc = audio_proc = None

@app.callback()
def callback(): pass

@app.command("version")
def version():
    from formatflux import __version__
    typer.echo(f"Formatflux v{__version__}")

@app.command("info")
def info_cmd(input_path: Path):
    if not converter or not input_path.exists():
        raise typer.Exit(1)
    try:
        info = converter.get_info(str(input_path))
        typer.echo(f"Archivo: {input_path.name} | Tamaño: {input_path.stat().st_size/1024:.1f}KB")
        if "format" in info:
            f = info["format"]
            typer.echo(f"Formato: {f.get('format_name','N/A')} | Duración: {float(f.get('duration',0)):.1f}s")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

@app.command("convert")
def convert_cmd(input_path: Path, output_path: Path, video_bitrate: str = None, audio_bitrate: str = None):
    if not converter or not input_path.exists():
        raise typer.Exit(1)
    options = {}
    if video_bitrate: options["b:v"] = video_bitrate
    if audio_bitrate: options["b:a"] = audio_bitrate
    try:
        typer.echo(f"Convirtiendo {input_path.name}...")
        result = converter.convert(str(input_path), str(output_path), options)
        typer.echo(f"✓ {result['output_size']/1024:.1f}KB guardado en {result['output']}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

@app.command("batch-convert")
def batch_convert_cmd(input_dir: Path, output_dir: Path, pattern: str = "*"):
    if not converter or not input_dir.exists():
        raise typer.Exit(1)
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        results = converter.batch_convert(str(input_dir), str(output_dir), pattern)
        success = sum(1 for r in results if r["success"])
        typer.echo(f"✓ {success}/{len(results)} convertidos")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

@app.command("chroma-key")
def chroma_key_cmd(input_path: Path, output_path: Path, color: str = "green", similarity: float = 0.3):
    if not video_proc or not input_path.exists():
        raise typer.Exit(1)
    try:
        typer.echo("Aplicando chroma key...")
        result = video_proc.chroma_key(str(input_path), str(output_path), color, similarity)
        typer.echo(f"✓ {result['message']}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

@app.command("subtitles-generate")
def subtitles_generate_cmd(input_path: Path, output_path: Path, language: str = "es", model: str = "small"):
    if not video_proc or not input_path.exists():
        raise typer.Exit(1)
    try:
        typer.echo("Transcribiendo (esto puede tardar)...")
        result = video_proc.generate_subtitles_ai(str(input_path), str(output_path), language, model)
        typer.echo(f"✓ {result['segments']} segmentos guardados en {result['output']}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

@app.command("subtitles-embed")
def subtitles_embed_cmd(input_path: Path, subtitles_path: Path, output_path: Path):
    if not video_proc or not input_path.exists() or not subtitles_path.exists():
        raise typer.Exit(1)
    try:
        result = video_proc.add_subtitles(str(input_path), str(subtitles_path), str(output_path))
        typer.echo(f"✓ Subtítulos incrustados en {result['output']}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

@app.command("audio-normalize")
def audio_normalize_cmd(input_path: Path, output_path: Path, level: float = -16.0):
    if not audio_proc or not input_path.exists():
        raise typer.Exit(1)
    try:
        result = audio_proc.normalize(str(input_path), str(output_path), level)
        typer.echo(f"✓ Audio normalizado: {result['output']}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

@app.command("audio-trim")
def audio_trim_cmd(input_path: Path, output_path: Path, start: float, end: float = None, duration: float = None):
    if not audio_proc or not input_path.exists():
        raise typer.Exit(1)
    try:
        result = audio_proc.trim(str(input_path), str(output_path), start, end, duration)
        typer.echo(f"✓ Audio recortado: {result['output']} ({result['duration']:.1f}s)")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

@app.command("extract-frames")
def extract_frames_cmd(input_path: Path, output_dir: Path, fps: int = 1):
    if not video_proc or not input_path.exists():
        raise typer.Exit(1)
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        result = video_proc.extract_frames(str(input_path), str(output_dir), fps)
        typer.echo(f"✓ {result['frames_extracted']} frames en {result['output_dir']}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

def main(): app()
if __name__ == "__main__": main()
