#!/usr/bin/env python3

from pathlib import Path

from config import LIBRARY, TARGET_SECONDS, BITRATE
from audio_utils import (
    get_duration,
    concat,
    natural_sort,
)


def merge_book(book: Path):

    print(f"\n📚 {book.name}")

    mp3s = natural_sort(list(book.glob("part_*.mp3")))

    if not mp3s:
        print("   No audio found.")
        return

    merged = book / "merged"
    merged.mkdir(exist_ok=True)

    volume = 1
    current = []
    total = 0

    for mp3 in mp3s:

        d = get_duration(mp3)

        if total + d > TARGET_SECONDS and current:

            outfile = merged / f"{book.name}_{volume:03d}.mp3"

            if outfile.exists():

                print(f"   Skip {outfile.name}")

            else:

                print(f"   Create {outfile.name}")

                concat(
                    current,
                    outfile,
                    bitrate=BITRATE
                )

            volume += 1
            current = []
            total = 0

        current.append(mp3)
        total += d

    if current:

        outfile = merged / f"{book.name}_{volume:03d}.mp3"

        if outfile.exists():

            print(f"   Skip {outfile.name}")

        else:

            print(f"   Create {outfile.name}")

            concat(
                current,
                outfile,
                bitrate=BITRATE
            )


def main():

    books = sorted([x for x in LIBRARY.iterdir() if x.is_dir()])

    print(f"\nFound {len(books)} books\n")

    for book in books:

        try:

            merge_book(book)

        except Exception as e:

            print(f"\n❌ {book.name}")

            print(e)

            continue

    print("\n✅ Finished")


if __name__ == "__main__":
    main()
