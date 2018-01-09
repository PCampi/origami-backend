"""Module for a sessioned resource."""

from abc import ABCMeta


class SessionedResource:
    """Base abstract class for a resource with a session."""
    __metaclass__ = ABCMeta

    def __init__(self):
        self.session = None
