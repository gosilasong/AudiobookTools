from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class Book:
    """
    Represents one audiobook.
    """

    path: Path
    name: str

    audio_files: list[Path] = field(default_factory=list)

    ebook: Path | None = None

    cover: Path |None = None

    @property
    def audio_count(self) -> int:
        return len(self.audio_files)
