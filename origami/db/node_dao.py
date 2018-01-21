"""DAO module for the Node class."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from .meta import Base
from .base_dao import BaseDao

class NodeDao(BaseDao, Base):
    """DAO class for Node objects."""

    id = Column(Integer, primary_key=True)
    name = Column(String(25))


    def __init__(self, name):
        self.name = name

    @property
    def as_dict(self):
        """Returns a dictionary representation of the object."""
        return {
            "id": self.id,
            "name": self.name,
        }

    def save(self, session):
        """Persist the object."""
        session.add(self)

    @classmethod
    def get_by_id(cls, node_id, session):
        """Get a single instance identified by its id."""
        query = session.query(cls).filter(cls.id == node_id)
        try:
            node = query.one()
        except MultipleResultsFound:
            raise
        except NoResultFound:
            return None

        return node

    @classmethod
    def get_list(cls, session):
        """Get a list of instances from the db."""
        nodes = session.query(cls).all()
        return nodes

    def __repr__(self):
        """Return a description of self."""
        return "<Node(id:{}, name:{})>".format(
            self.id, self.name)

