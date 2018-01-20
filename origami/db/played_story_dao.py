"""DAO module for the Played Story class."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from .meta import Base
from .base_dao import BaseDao

class PlayedStoryDao(BaseDao, Base):
    """DAO class for Played Story objects."""

    id = Column(Integer, primary_key = True)
    player_id = Column(Integer, ForeignKey('player.id'))

    def __init__(self,  player_id):
        self.player_id = player_id

    @property
    def as_dict(self):
        """Returns a dictionary representation of the object."""
        return {
            "id": self.id,
            "player_id": self.player_id
        }

    def save(self, session):
        """Persist the object."""
        session.add(self)

    @classmethod
    def get_by_id(cls, played_story_id, session):
        """Get a single instance identified by its id."""
        query = session.query(cls).filter(cls.id == played_story_id)
        try:
            played_story = query.one()
        except MultipleResultsFound:
            raise
        except NoResultFound:
            return None

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