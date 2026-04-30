"""MediaConverter - Motor de conversión multimedia basado en FFmpeg."""
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class MediaConverter:
    """Conversor multimedia basado en FFmpeg."""

    VIDEO_FORMATS = {"mp4", "avi", "mkv", "mov", "flv", "wmv", "webm"}
    AUDIO_FORMATS = {"mp3", "wav", "flac", "aac", "ogg", "m4a"}
    IMAGE_FORMATS = {"jpg", "jpeg", "png", "gif", "bmp", "webp", "tiff"}

    def __init__(self, ffmpeg_path: Optional[str] = None):
        self.ffmpeg_path = ffmpeg_path or shutil.which("ffmpeg")
        if not self.ffmpeg_path:
            raise RuntimeError("FFmpeg no encontrado. Instálalo o especifica ffmpeg_path.")
        self.ffprobe_path = shutil.which("ffprobe")

    def convert(self, input_path: str, output_path: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Convierte un archivo multimedia."""
        input_file = Path(input_path)
        output_file = Path(output_path)

        if not input_file.exists():
            raise FileNotFoundError(f"Archivo de entrada no encontrado: {input_path}")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        cmd = [self.ffmpeg_path, "-i", str(input_file), "-y"]
        if options:
            for key, value in options.items():
                cmd.extend([f"-{key}", str(value)])
        cmd.append(str(output_file))

        logger.info(f"Ejecutando conversión: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
            if result.returncode != 0:
                raise RuntimeError(f"FFmpeg falló: {result.stderr}")
            output_size = output_file.stat().st_size if output_file.exists() else 0
            return {"success": True, "input": str(input_file), "output": str(output_file), "output_size": output_size, "message": "Conversión completada"}
        except subprocess.TimeoutExpired:
            raise TimeoutError("La conversión tardó demasiado")

    def get_info(self, file_path: str) -> Dict[str, Any]:
        """Obtiene información de un archivo multimedia."""
        if not self.ffprobe_path:
            raise RuntimeError("FFprobe no disponible")
        file = Path(file_path)
        if not file.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        cmd = [self.ffprobe_path, "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(file)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFprobe falló: {result.stderr}")
        import json
        return json.loads(result.stdout)

    def batch_convert(self, input_dir: str, output_dir: str, pattern: str = "*", options: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Convierte múltiples archivos en un directorio."""
        from pathlib import Path
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        files = list(input_path.glob(pattern))
        results = []
        for file in files:
            output_file = output_path / f"{file.stem}_converted{file.suffix}"
            try:
                result = self.convert(str(file), str(output_file), options)
                results.append(result)
            except Exception as e:
                results.append({"success": False, "input": str(file), "error": str(e)})
        return results


__all__ = ["MediaConverter"]
