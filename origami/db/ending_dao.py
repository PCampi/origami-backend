"""DAO module for the Ending class."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from .meta import Base
from .base_dao import BaseDao
from .player_history_dao import PlayerHistoryDao

class EndingDao(BaseDao, Base):
    """DAO class for Ending objects."""

    id = Column(Integer, primary_key = True)
    id_player_history = Column(Integer, ForeignKey('player_history.id'))
    text = Column(String(1000))

    def __init__(self, id_player_history, text):
        self.id_player_history = id_player_history
        self.text = text

    @property
    def as_dict(self):
        """Returns a dictionary representation of the object."""
        return {
            "id": self.id,
            "id_player_history": self.id_player_history,
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
        return "<Ending(id:{}, id_player_history:{}, text:{})>".format(
            self.id, self.id_player_history, self.text)
