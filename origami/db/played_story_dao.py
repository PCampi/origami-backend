"""DAO module for the Played Story class."""

from sqlalchemy import Column, ForeignKey, Integer

from .base_dao import BaseDao
from .meta import Base


class PlayedStoryDao(BaseDao, Base):
    """DAO class for Played Story objects."""

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.id'))

    def __init__(self, player_id: int) -> None:
        self.player_id = player_id

    @property
    def as_dict(self):
        """Returns a dictionary representation of the object."""
        return {
            "id": self.id,
            "player_id": self.player_id
        }

    @classmethod
    def get_by_id(cls, played_story_id: str, session):
        """Get a single instance identified by its id."""
        query = session.query(cls).filter(cls.id == played_story_id)
        played_story = cls.get_one(query)
        return played_story

    @classmethod
    def get_list(cls, session):
        """Get a list of instances from the db."""
        played_stories = session.query(cls).all()
        return played_stories

    def __repr__(self):
        """Return a description of self."""
        return "<PlayedStory(id:{}, player_id:{})>".format(
            self.id, self.player_id)
