"""DAO module for the Ending class."""

from sqlalchemy import Column, Integer, String, ForeignKey

from .meta import Base
from .base_dao import BaseDao


class EndingDao(BaseDao, Base):
    """DAO class for Ending objects."""

    id = Column(Integer, primary_key=True)
    played_story_id = Column(Integer, ForeignKey('playedstory.id'))
    text = Column(String(1000))

    def __init__(self, played_story_id: int, text: str) -> None:
        self.played_story_id = played_story_id
        self.text = text

    @property
    def as_dict(self):
        """Returns a dictionary representation of the object."""
        return {
            "id": self.id,
            "played_story_id": self.played_story_id,
            "text": self.text
        }

    @classmethod
    def get_by_id(cls, ending_id: int, session):
        """Get a single instance identified by its id."""
        query = session.query(cls).filter(cls.id == ending_id)
        ending = cls.get_one(query)
        return ending

    @classmethod
    def get_by_played_story_id(cls, story_id: int, session):
        """Get a single instance identified by its played story id."""
        query = session.query(cls).filter(cls.played_story_id == story_id)
        story = cls.get_one(query)
        return story

    @classmethod
    def get_list(cls, session):
        """Get a list of instances from the db."""
        endings = session.query(cls).all()
        return endings

    def __repr__(self):
        """Return a description of self."""
        return "<Ending(id:{}, played_story_id:{}, text:{})>".format(
            self.id, self.played_story_id, self.text)
