from __future__ import annotations

import subprocess
from pathlib import Path


SUPPORTED_AUDIO = {
    ".mp3",
    ".wav",
    ".m4a",
    ".aac",
    ".flac",
    ".ogg",
}


def is_audio(path: Path) -> bool:
    return path.suffix.lower() in SUPPORTED_AUDIO


def ffprobe(path: Path) -> dict:
    """
    Read audio information using ffprobe.
    """

    cmd = [
        "ffprobe",
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

    import json

    return json.loads(result.stdout)


def codec(path: Path) -> str:
    """
    Return codec name.
    """

    info = ffprobe(path)

    streams = info.get("streams", [])

    if not streams:
        return ""

    return streams[0].get("codec_name", "")


def duration(path: Path) -> float:
    """
    Return duration in seconds.
    """

    info = ffprobe(path)

    fmt = info.get("format", {})

    try:
        return float(fmt.get("duration", 0))
    except Exception:
        return 0.0


def natural_key(path: Path):
    """
    Natural sort.

    part_2.mp3

    part_10.mp3

    =>
    part_2

    part_10
    """

    import re

    return [
        int(t) if t.isdigit() else t.lower()
        for t in re.split(r"(\d+)", path.stem)
    ]


def sort_audio(files: list[Path]) -> list[Path]:
    return sorted(files, key=natural_key)


def total_duration(files: list[Path]) -> float:
    total = 0.0

    for f in files:
        total += duration(f)

    return total


def split_by_duration(
    files: list[Path],
    hours: float = 2,
) -> list[list[Path]]:
    """
    Split audio into groups.

    Default:
        2 hours per volume.
    """

    target = hours * 3600

    result: list[list[Path]] = []

    current: list[Path] = []

    current_duration = 0.0

    for file in sort_audio(files):

        d = duration(file)

        if current and current_duration + d > target:

            result.append(current)

            current = []

            current_duration = 0

        current.append(file)

        current_duration += d

    if current:

        result.append(current)

    return result


def concat(
    files: list[Path],
    output: Path,
):
    """
    Merge audio using ffmpeg concat demuxer.

    Works for:
        MP3
        AAC
        FLAC
        M4A
    """

    output.parent.mkdir(parents=True, exist_ok=True)

    concat_file = output.parent / "concat.txt"

    with concat_file.open(
        "w",
        encoding="utf8",
    ) as fp:

        for f in files:

            fp.write(f"file '{f.resolve()}'\n")

    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "warning",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(output),
        ],
        check=True,
    )
