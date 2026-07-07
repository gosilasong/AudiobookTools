from pathlib import Path

from audiobooktools.models import Book
from audiobooktools.merger import Merger


def test_create_merger():
    merger = Merger()

    assert merger.hours_per_volume == 2.0


def test_create_empty_book(tmp_path: Path):
    folder = tmp_path / "Book"
    folder.mkdir()

    book = Book(
        path=folder,
        name="Book",
    )

    assert book.name == "Book"
    assert book.audio_count == 0
