"""DAO module for the Ending class."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from .meta import Base
from .base_dao import BaseDao
from .played_story_dao import PlayedStoryDao

class EndingDao(BaseDao, Base):
    """DAO class for Ending objects."""

    id = Column(Integer, primary_key = True)
    id_played_story = Column(Integer, ForeignKey('played_story.id'))
    text = Column(String(1000))

    def __init__(self, id_played_story, text):
        self.id_played_story = id_played_story
        self.text = text

    @property
    def as_dict(self):
        """Returns a dictionary representation of the object."""
        return {
            "id": self.id,
            "id_played_story": self.id_played_story,
            "text": self.text
        }

    def save(self, session):
        """Persist the object."""
        session.add(self)

    @classmethod
    def get_by_id(cls, ending_id, session):
        """Get a single instance identified by its id."""
        query = session.query(cls).filter(cls.id == ending_id)
        try:
            ending = query.one()
        except MultipleResultsFound:
            raise
        except NoResultFound:
            return None

        return ending

    @classmethod
    def get_list(cls, session):
        """Get a list of instances from the db."""
        endings = session.query(cls).all()
        return endings

    def __repr__(self):
        """Return a description of self."""
        return "<Ending(id:{}, id_played_story:{}, text:{})>".format(
            self.id, self.id_played_story, self.text)
