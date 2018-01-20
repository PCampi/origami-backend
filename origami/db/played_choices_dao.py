"""DAO module for the Played Choices class."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from .meta import Base
from .base_dao import BaseDao

class PlayedChoicesDao(BaseDao, Base):
    """DAO class for Played Choices instances."""

    story_id = Column(Integer, ForeignKey('playedstory.id'), primary_key=True)
    choice_number = Column(Integer, autoincrement=False)
    node_id = Column(Integer, ForeignKey('node.id'), primary_key=True)

    def __init__(self, story_id, choice_number, node_id):
        self.story_id = story_id
        self.choice_number = choice_number
        self.node_id = node_id

    @property
    def as_dict(self):
        """Returns a dictionary representation of the object."""
        return {
            "story_id": self.story_id,
            "choice_number": self.choice_number,
            "node_id": self.node_id
        }

    def save(self, session):
        """Persist the object."""
        session.add(self)

    @classmethod
    def get_by_id(cls, story_id, session):
        """Get multiple istances identified by a story id."""
        story = session.query(cls).filter(cls.story_id == story_id)
        return story

    @classmethod
    def get_list(cls, session):
        """Get a list of instances from the db."""
        stories = session.query(cls).all()
        return stories

    def __repr__(self):
        """Return a description of self."""
        return "<PlayedChoices(story_id:{}, choice_number:{}, player_id:{})>".format(
            self.story_id, self.choice_number, self.player_id)