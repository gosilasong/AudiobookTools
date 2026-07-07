from pathlib import Path

from .models import Book

AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".aac",
    ".flac",
    ".ogg",
}

EBOOK_EXTENSIONS = {
    ".txt",
    ".epub",
    ".mobi",
}

COVER_FILES = {
    "cover.jpg",
    "cover.jpeg",
    "cover.png",
    "folder.jpg",
    "folder.jpeg",
    "folder.png",
}


def scan_book(folder: Path) -> Book:
    """
    Scan one audiobook folder.
    """

    if not folder.exists():
        raise FileNotFoundError(folder)

    if not folder.is_dir():
        raise NotADirectoryError(folder)

    book = Book(
        path=folder,
        name=folder.name,
    )

    for item in folder.iterdir():

        if not item.is_file():
            continue

        suffix = item.suffix.lower()

        if suffix in AUDIO_EXTENSIONS:
            book.audio_files.append(item)
            continue

        if suffix in EBOOK_EXTENSIONS:
            if book.ebook is None:
                book.ebook = item
            continue

        if item.name.lower() in COVER_FILES:
            if book.cover is None:
                book.cover = item

    # alphabetical sort first
    book.audio_files.sort(key=lambda p: p.name.lower())

    return book


def scan_library(root: Path) -> list[Book]:
    """
    Scan the whole audiobook library.
    """

    if not root.exists():
        raise FileNotFoundError(root)

    books: list[Book] = []

    for folder in sorted(root.iterdir()):

        if not folder.is_dir():
            continue

        try:
            book = scan_book(folder)

            if book.audio_count == 0:
                continue

            books.append(book)

        except Exception as ex:
            print(f"Skip {folder.name}: {ex}")

    return books
