# AudiobookTools

AudiobookTools is a professional audiobook processing toolkit written in Python.

The goal of this project is to organize, analyze, and merge large audiobook collections into manageable audiobook volumes.

Unlike many existing tools, AudiobookTools is designed for very large libraries containing thousands of audio files while keeping memory usage low and maintaining high performance.

---

# Features

Current

- Scan audiobook folders
- Support all audio formats recognized by FFmpeg
- Natural filename sorting
- Merge thousands of audio files
- Split output by target duration
- Dry Run mode
- Resume interrupted jobs
- Cross-platform

Planned

- M4B output
- Chapter metadata
- EPUB import
- PDF import
- TTS pipeline
- Podcast RSS generation
- GUI

---

# Design Goals

AudiobookTools is designed around several core principles.

## Fast

Use FFmpeg whenever possible.

Avoid unnecessary audio re-encoding.

## Reliable

Never modify source files.

Support interrupted jobs.

Generate reproducible merge plans.

## Low Memory

Never load an entire audiobook into memory.

Process audio incrementally.

Designed for books containing thousands of files.

## Flexible

Do not assume:

- MP3 input
- Standard filenames
- Chapter naming rules
- Folder structure

---

# Supported Audio Formats

AudiobookTools does not rely on file extensions.

Instead, FFprobe is used to detect whether a file contains audio.

Examples include:

- MP3
- M4A
- AAC
- WAV
- FLAC
- OGG
- OPUS
- M4B
- AIFF
- WMA

Any format supported by FFmpeg should work.

---

# Example

Input

```
Harry Potter/

Disc1/
    chapter001.mp3
    chapter002.mp3

Disc2/
    Track01.m4a
    Track02.flac
```

↓

Output

```
Harry Potter_001.mp3
Harry Potter_002.mp3
Harry Potter_003.mp3
```

Each output volume is approximately two hours long.

No individual audio file is ever split.

---

# Architecture

```
Scanner
    │
    ▼
Planner
    │
    ▼
Merge Plan
    │
    ▼
Merger
    │
    ▼
Output
```

---

# Roadmap

Version 1

- Scanner
- Planner
- Merger
- CLI

Version 2

- M4B
- Chapter Metadata

Version 3

- EPUB
- PDF

Version 4

- TTS Providers

Version 5

- GUI

---

# Requirements

- Python 3.14+
- FFmpeg
- FFprobe

---

# License

MIT License
