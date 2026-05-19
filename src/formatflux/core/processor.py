"""Processors - Procesadores de video y audio."""
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging
import tempfile

logger = logging.getLogger(__name__)


class VideoProcessor:
    """Procesador de archivos de video."""

    def __init__(self, ffmpeg_path: Optional[str] = None):
        self.ffmpeg_path = ffmpeg_path or shutil.which("ffmpeg")
        if not self.ffmpeg_path:
            raise RuntimeError("FFmpeg no encontrado.")

    def chroma_key(self, input_path: str, output_path: str, color: str = "green", similarity: float = 0.3, blend: float = 0.0) -> Dict[str, Any]:
        """Aplica chroma key (pantalla verde/azul) a un video."""
        input_file, output_file = Path(input_path), Path(output_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Video no encontrado: {input_path}")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        if color.lower() == "green":
            chroma_filter = f"colorkey=0x00ff00:{similarity}:{blend}"
        elif color.lower() == "blue":
            chroma_filter = f"colorkey=0x0000ff:{similarity}:{blend}"
        else:
            raise ValueError("Color debe ser 'green' o 'blue'")
        cmd = [self.ffmpeg_path, "-i", str(input_file), "-filter_complex", f"[0:v]{chroma_filter}[v]", "-map", "[v]", "-map", "0:a?", "-c:a", "copy", "-y", str(output_file)]
        logger.info(f"Aplicando chroma key")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Chroma key falló: {result.stderr}")
        return {"success": True, "input": str(input_file), "output": str(output_file), "color": color, "message": "Chroma key aplicado correctamente"}

    def add_subtitles(self, input_path: str, subtitles_path: str, output_path: str, language: str = "es") -> Dict[str, Any]:
        """Incrusta subtítulos en un video."""
        input_file, subs_file, output_file = Path(input_path), Path(subtitles_path), Path(output_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Video no encontrado: {input_path}")
        if not subs_file.exists():
            raise FileNotFoundError(f"Subtítulos no encontrados: {subtitles_path}")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        cmd = [self.ffmpeg_path, "-i", str(input_file), "-vf", f"subtitles={str(subs_file)}", "-c:a", "copy", "-y", str(output_file)]
        logger.info(f"Incrustando subtítulos")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Incrustar subtítulos falló: {result.stderr}")
        return {"success": True, "input": str(input_file), "output": str(output_file), "subtitles": str(subs_file), "language": language, "message": "Subtítulos incrustados"}

    def generate_subtitles_ai(self, input_path: str, output_path: str, language: str = "es", model: str = "small") -> Dict[str, Any]:
        """Genera subtítulos automáticamente usando Whisper IA."""
        try:
            import whisper
        except ImportError:
            raise ImportError("Whisper no instalado. Instálalo con: pip install openai-whisper")
        input_file, output_file = Path(input_path), Path(output_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Video no encontrado: {input_path}")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Transcribiendo audio con Whisper (modelo: {model})")
        model_whisper = whisper.load_model(model)
        result_whisper = model_whisper.transcribe(str(input_file), language=language, verbose=False)
        with open(output_file, "w", encoding="utf-8") as f:
            for segment in result_whisper["segments"]:
                start = self._format_timestamp(segment["start"])
                end = self._format_timestamp(segment["end"])
                text = segment["text"].strip()
                f.write(f"{segment['id'] + 1}\n{start} --> {end}\n{text}\n\n")
        return {"success": True, "input": str(input_file), "output": str(output_file), "language": language, "model": model, "segments": len(result_whisper["segments"]), "duration": result_whisper["segments"][-1]["end"] if result_whisper["segments"] else 0, "message": "Subtítulos generados correctamente"}

    def extract_frames(self, input_path: str, output_dir: str, fps: int = 1, format: str = "jpg") -> Dict[str, Any]:
        """Extrae fotogramas de un video."""
        input_file, output_path = Path(input_path), Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        if not input_file.exists():
            raise FileNotFoundError(f"Video no encontrado: {input_path}")
        pattern = output_path / f"frame_%06d.{format}"
        cmd = [self.ffmpeg_path, "-i", str(input_file), "-vf", f"fps={fps}", "-q:v", "2", str(pattern), "-y"]
        logger.info(f"Extrayendo frames a {fps} FPS")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Extracción de frames falló: {result.stderr}")
        frames = len(list(output_path.glob(f"*.{format}")))
        return {"success": True, "input": str(input_file), "output_dir": str(output_path), "fps": fps, "frames_extracted": frames, "message": f"{frames} frames extraídos"}

    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        """Formatea segundos a timestamp SRT."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


class AudioProcessor:
    """Procesador de archivos de audio."""

    def __init__(self, ffmpeg_path: Optional[str] = None):
        self.ffmpeg_path = ffmpeg_path or shutil.which("ffmpeg")
        if not self.ffmpeg_path:
            raise RuntimeError("FFmpeg no encontrado.")

    def normalize(self, input_path: str, output_path: str, target_level: float = -16.0) -> Dict[str, Any]:
        """Normaliza el volumen de un archivo de audio."""
        input_file, output_file = Path(input_path), Path(output_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Audio no encontrado: {input_path}")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        cmd = [self.ffmpeg_path, "-i", str(input_file), "-af", f"loudnorm=I={target_level}:TP=-1.5:LRA=11", "-y", str(output_file)]
        logger.info(f"Normalizando audio a {target_level} LUFS")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Normalización falló: {result.stderr}")
        return {"success": True, "input": str(input_file), "output": str(output_file), "target_level": target_level, "message": "Audio normalizado correctamente"}

    def trim(self, input_path: str, output_path: str, start: float, end: Optional[float] = None, duration: Optional[float] = None) -> Dict[str, Any]:
        """Recorta un archivo de audio."""
        input_file, output_file = Path(input_path), Path(output_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Audio no encontrado: {input_path}")
        if end is None and duration is None:
            raise ValueError("Se debe especificar 'end' o 'duration'")
        if duration is not None:
            end = start + duration
        output_file.parent.mkdir(parents=True, exist_ok=True)
        cmd = [self.ffmpeg_path, "-i", str(input_file), "-ss", str(start), "-to", str(end), "-c", "copy", "-y", str(output_file)]
        logger.info(f"Recortando audio: {start}s - {end}s")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Recorte falló: {result.stderr}")
        return {"success": True, "input": str(input_file), "output": str(output_file), "start": start, "end": end, "duration": end - start, "message": "Audio recortado correctamente"}

    def convert(self, input_path: str, output_path: str, bitrate: str = "192k") -> Dict[str, Any]:
        """Convierte el formato de un archivo de audio."""
        input_file, output_file = Path(input_path), Path(output_file)
        if not input_file.exists():
            raise FileNotFoundError(f"Audio no encontrado: {input_path}")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        cmd = [self.ffmpeg_path, "-i", str(input_file), "-b:a", bitrate, "-y", str(output_file)]
        logger.info(f"Convirtiendo audio a {bitrate}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Conversión falló: {result.stderr}")
        return {"success": True, "input": str(input_file), "output": str(output_file), "bitrate": bitrate, "message": "Audio convertido correctamente"}

    def merge(self, input_paths: List[str], output_path: str) -> Dict[str, Any]:
        """Mezcla múltiples archivos de audio."""
        input_files = [Path(p) for p in input_paths]
        output_file = Path(output_path)
        for f in input_files:
            if not f.exists():
                raise FileNotFoundError(f"Audio no encontrado: {f}")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
            for f in input_files:
                tmp.write(f"file '{f.absolute()}'\n")
            tmp_path = tmp.name
        try:
            cmd = [self.ffmpeg_path, "-f", "concat", "-safe", "0", "-i", tmp_path, "-c", "copy", "-y", str(output_file)]
            logger.info(f"Mezclando {len(input_files)} archivos de audio")
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"Mezcla falló: {result.stderr}")
            return {"success": True, "inputs": [str(f) for f in input_files], "output": str(output_file), "message": f"{len(input_files)} audios mezclados"}
        finally:
            Path(tmp_path).unlink(missing_ok=True)


__all__ = ["VideoProcessor", "AudioProcessor"]
