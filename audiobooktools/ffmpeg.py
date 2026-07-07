"""
FFmpeg / FFprobe wrapper for AudiobookTools.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from .models import AudioFile


class FFmpegError(RuntimeError):
    """Raised when FFmpeg or FFprobe fails."""


class FFmpeg:
    """
    Wrapper around FFmpeg / FFprobe.
    """

    @staticmethod
    def ffmpeg() -> str:
        exe = shutil.which("ffmpeg")
        if exe is None:
            raise FFmpegError("ffmpeg not found in PATH.")
        return exe

    @staticmethod
    def ffprobe() -> str:
        exe = shutil.which("ffprobe")
        if exe is None:
            raise FFmpegError("ffprobe not found in PATH.")
        return exe

    @staticmethod
    def probe(path: Path) -> AudioFile:
        """
        Read audio metadata using ffprobe.
        """

        if not path.exists():
            raise FileNotFoundError(path)

        cmd = [
            FFmpeg.ffprobe(),
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )

        data = json.loads(result.stdout)

        audio_stream = None

        for stream in data.get("streams", []):
            if stream.get("codec_type") == "audio":
                audio_stream = stream
                break

        if audio_stream is None:
            raise FFmpegError(f"No audio stream found: {path}")

        fmt = data.get("format", {})

        duration = float(fmt.get("duration", 0))

        bitrate = int(fmt.get("bit_rate", 0)) if fmt.get("bit_rate") else 0

        sample_rate = (
            int(audio_stream.get("sample_rate", 0))
            if audio_stream.get("sample_rate")
            else 0
        )

        channels = audio_stream.get("channels", 0)

        codec = audio_stream.get("codec_name", "")

        return AudioFile(
            path=path,
            duration=duration,
            size=path.stat().st_size,
            codec=codec,
            bitrate=bitrate,
            sample_rate=sample_rate,
            channels=channels,
        )
