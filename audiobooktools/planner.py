"""
Audiobook volume planner.
"""

from __future__ import annotations

from .models import AudioFile, MergePlan, Volume


class Planner:
    """
    Split audio files into volumes based on target duration.
    """

    def __init__(self, hours_per_volume: float = 2.0):
        if hours_per_volume <= 0:
            raise ValueError("hours_per_volume must be greater than zero.")

        self.hours_per_volume = hours_per_volume
        self.target_duration = hours_per_volume * 3600

    def create(self, audio_files: list[AudioFile]) -> MergePlan:
        """
        Create a merge plan.
        """

        plan = MergePlan()

        if not audio_files:
            return plan

        volume = Volume(index=1)

        for audio in audio_files:

            if (
                volume.files
                and volume.duration + audio.duration > self.target_duration
            ):
                plan.volumes.append(volume)
                volume = Volume(index=len(plan.volumes) + 1)

            volume.files.append(audio)

        if volume.files:
            plan.volumes.append(volume)

        return plan
