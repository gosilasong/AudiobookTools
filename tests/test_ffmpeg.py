from pathlib import Path

from audiobooktools.ffmpeg import FFmpeg


def test_ffmpeg_exists():
    assert FFmpeg.ffmpeg()


def test_ffprobe_exists():
    assert FFmpeg.ffprobe()
