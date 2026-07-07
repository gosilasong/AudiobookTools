from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class AudioFile:
    """
    一個音訊檔
    """

    path: Path

    duration: float = 0.0

    codec: str = ""

    size: int = 0


@dataclass
class Volume:
    """
    合併後的一卷
    """

    index: int

    files: List[AudioFile] = field(default_factory=list)

    duration: float = 0.0

    output: Optional[Path] = None


@dataclass
class Book:
    """
    一本書
    """

    path: Path

    name: str

    ebook: Optional[Path] = None

    cover: Optional[Path] = None

    audio_files: List[AudioFile] = field(default_factory=list)

    volumes: List[Volume] = field(default_factory=list)

    total_duration: float = 0.0

    codec: str = ""

    merged_dir: Optional[Path] = None

    metadata: dict = field(default_factory=dict)

    def add_audio(self, audio: AudioFile):

        self.audio_files.append(audio)

        self.total_duration += audio.duration

    @property
    def audio_count(self):

        return len(self.audio_files)

    @property
    def merged_count(self):

        return len(self.volumes)
