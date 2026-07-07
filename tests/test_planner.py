from pathlib import Path

from audiobooktools.models import AudioFile
from audiobooktools.planner import Planner


def test_empty_plan():

    planner = Planner()

    plan = planner.create([])

    assert plan.total_volumes == 0


def test_single_volume():

    planner = Planner(hours_per_volume=2)

    files = [
        AudioFile(Path("1.mp3"), duration=1800),
        AudioFile(Path("2.mp3"), duration=1800),
        AudioFile(Path("3.mp3"), duration=1800),
    ]

    plan = planner.create(files)

    assert plan.total_volumes == 1
    assert plan.volumes[0].file_count == 3


def test_split_volume():

    planner = Planner(hours_per_volume=1)

    files = [
        AudioFile(Path("1.mp3"), duration=1800),
        AudioFile(Path("2.mp3"), duration=1800),
        AudioFile(Path("3.mp3"), duration=1800),
    ]

    plan = planner.create(files)

    assert plan.total_volumes == 2

    assert plan.volumes[0].file_count == 2
    assert plan.volumes[1].file_count == 1
