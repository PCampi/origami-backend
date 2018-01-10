"""Type of resources."""

import enum


class ResourceEnum(enum.Enum):
    """Enum for the resource classes."""
    audio = "audio"
    video = "video"
    text = "text"
    image = "image"
