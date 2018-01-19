"""DAO module for the Resource class."""

from sqlalchemy import Column, Integer, String, and_
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from .meta import Base
from .base_dao import BaseDao
from .resource_type import ResourceEnum


class ResourceDao(BaseDao, Base):
    """DAO class for Resource objects."""

    id = Column(Integer, primary_key=True)
    resource_type = Column(String, primary_key=True)
    resource_name = Column(String)
    url = Column(String(50), nullable=True)
    fs_path = Column(String(50), nullable=True)

    def __init__(self, resource_type, resource_name, url, fs_path):
        if resource_type in ResourceEnum:
            self.resource_type = resource_type
        else:
            raise ValueError("Value {} not allowed for argument resource_type. See resource_type.py"
                             .format(resource_type))
        self.resource_name = resource_name
        self.url = url
        self.fs_path = fs_path

    @property
    def as_dict(self):
        """Returns a dictionary representation of the object."""
        return {
            "id": self.id,
            "resource_type": self.resource_type,
            "resource_name": self.resource_name,
            "url": self.url,
            "fs_path": self.fs_path
        }

    def save(self, session):
        """Persist the object."""
        session.add(self)

    @classmethod
    def get_by_id_and_type(cls, resource_id, resource_type, session):
        """Get a single instance identified by id and type."""
        if resource_type not in ResourceEnum:
            raise ValueError("Value {} not allowed for argument resource_type. See resource_type.py"
                             .format(resource_type))

        query = session.query(cls)\
            .filter(and_(cls.id == resource_id, cls.resource_type == resource_type))
        try:
            resources = query.one()
        except MultipleResultsFound:
            raise
        except NoResultFound:
            return None
        else:
            return resources

    @classmethod
    def get_by_name_and_type(cls, resource_name, resource_type, session):
        """Get a single instance identified by name and type."""
        if resource_type not in ResourceEnum:
            raise ValueError("Value {} not allowed for argument resource_type. See resource_type.py"
                             .format(resource_type))

        query = session.query(cls)\
            .filter(and_(cls.resource_name == resource_name, cls.resource_type == resource_type))
        try:
            resources = query.one()
        except MultipleResultsFound:
            raise
        except NoResultFound:
            return None
        else:
            return resources

    @classmethod
    def get_list(cls, resource_type, session):
        """Return a list of instances."""
        if resource_type not in ResourceEnum:
            raise ValueError("Value {} not allowed for argument resource_type. See resource_type.py"
                             .format(resource_type))
        resources = session.query(cls).all()
        return resources

    def __repr__(self):
        """Return description of self."""
        return "<Resource(id: {}, type: {}, name: {}, url: {}, path: {})>".format(
            self.id, self.resource_type, self.resource_name, self.url, self.fs_path)
