"""DAO module for the Nodes relations (parent, child)."""

from sqlalchemy import Column, Integer, String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.exc import NoReferenceError

from .meta import Base
from .base_dao import BaseDao
from .node_dao import NodeDao
from .resource_dao import ResourceDao
from .resource_type import ResourceEnum

class NodeMediaDao(BaseDao, Base):
    """DAO class for Nodes media."""

    node_id = Column(Integer, ForeignKey('node.id'), primary_key = True)
    resource_id = Column(Integer, primary_key = True)
    resource_type = Column(String, primary_key = True)
    ForeignKeyConstraint(['resource_id', 'resource_type'], ['resource.id', 'resource.resource_type'])

    def __init__(self, node_id, resource_id, resource_type):
        self.node_id = node_id
        try:
            self.resource_id = resource_id
            self.resource_type = resource_type
        except NoReferenceError:
            raise
    
    @classmethod
    def get_by_node(cls, node_id, session):
        """Get the list of resource associated to the node given by id."""
        resources = session.query(cls).filter(cls.node_id == node_id)
        return resources

    @classmethod
    def get_by_resource(cls, resource_id, resource_type, session):
        """Get the list of resource associated to the node given by id."""
        if resource_type not in ResourceEnum:
            raise ValueError("Value {} not allowed for argument resource_type. See resource_type.py"
                             .format(resource_type))
        nodes = session.query(cls)\
            .filter(cls.resource_id == resource_id and cls.resource_type == resource_type)
        return nodes

    @classmethod
    def get_list(cls, session):
        """Return a list of instances."""
        couples = session.query(cls).all()
        return couples
        
        

            