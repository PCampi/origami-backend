"""Type of media."""

import enum


class MediaEnum(enum.Enum):
    """Enum for the media classes."""
    audio = "audio"
    video = "video"
    text = "text"
    image = "image"
