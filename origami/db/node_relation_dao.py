"""DAO module for the Nodes relations (parent, child)."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from .meta import Base
from .base_dao import BaseDao
from .node_dao import NodeDao

class NodeRelationDao(BaseDao, Base):
    """DAO class for Nodes relations."""

    parent_id = Column(Integer, ForeignKey('node.id'), primary_key = True)
    child_id = Column(Integer, ForeignKey('node.id'), primary_key = True)

    def __init__(self, parent_id, child_id):
        self.parent_id = parent_id
        self.child_id = child_id

    def save(self, session):
        """Persist the object."""
        session.add(self)

    @classmethod
    def get_by_parent(cls, parent_id, session):
        """Get the list of children for a parent identified by id."""
        children = session.query(cls).filter(cls.parent_id == parent_id)
        return children

    @classmethod
    def get_by_child(cls, child_id, session):
        """Get the list of parents for a child identified by id."""
        parents = session.query(cls).filter(cls.child_id == child_id)
        return parents

    @classmethod
    def get_list(cls, session):
        """Get a list of instances from the db."""
        relations = session.query(cls).all()
        return relations

