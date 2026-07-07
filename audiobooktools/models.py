"""
Core data models for AudiobookTools.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class AudioFile:
    """
    Represents one audio file.
    """

    path: Path
    duration: float = 0.0
    size: int = 0

    codec: str = ""
    bitrate: int = 0
    sample_rate: int = 0
    channels: int = 0

    @property
    def extension(self) -> str:
        return self.path.suffix.lower()

    @property
    def filename(self) -> str:
        return self.path.name


@dataclass(slots=True)
class Book:
    """
    Represents one audiobook.
    """

    path: Path
    name: str

    # Keep compatibility with existing scanner
    audio_files: list = field(default_factory=list)

    ebook: Path | None = None
    cover: Path | None = None

    @property
    def audio_count(self) -> int:
        return len(self.audio_files)


@dataclass(slots=True)
class Volume:
    index: int
    files: list[AudioFile] = field(default_factory=list)

    @property
    def duration(self) -> float:
        return sum(f.duration for f in self.files)

    @property
    def file_count(self) -> int:
        return len(self.files)


@dataclass(slots=True)
class MergePlan:
    volumes: list[Volume] = field(default_factory=list)

    @property
    def total_volumes(self) -> int:
        return len(self.volumes)

    @property
    def total_duration(self) -> float:
        return sum(v.duration for v in self.volumes)
