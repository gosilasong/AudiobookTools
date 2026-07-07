from pathlib import Path

from audiobooktools.scanner import scan_book


def test_scan_book(tmp_path: Path):

    folder = tmp_path / "MyBook"

    folder.mkdir()

    (folder / "chapter_001.mp3").touch()
    (folder / "chapter_002.mp3").touch()
    (folder / "book.epub").touch()
    (folder / "cover.jpg").touch()

    book = scan_book(folder)

    assert book.name == "MyBook"

    assert book.audio_count == 2

    assert book.ebook is not None

    assert book.cover is not None
