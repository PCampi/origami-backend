"""DAO module for the Media class."""

from sqlalchemy import Column, Integer, String, and_
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from .meta import Base
from .base_dao import BaseDao
from .media_type import MediaEnum


class MediaDao(BaseDao, Base):
    """DAO class for Media objects."""

    id = Column(Integer, primary_key=True)
    media_type = Column(String(5), primary_key=True)
    media_name = Column(String(50))
    url = Column(String(50), nullable=True)
    fs_path = Column(String(50), nullable=True)

    def __init__(self, media_type, media_name, url, fs_path):
        if media_type in MediaEnum:
            self.media_type = media_type
        else:
            raise ValueError("Value {} not allowed for argument media_type. See media_type.py"
                             .format(media_type))
        self.media_name = media_name
        self.url = url
        self.fs_path = fs_path

    @property
    def as_dict(self):
        """Returns a dictionary representation of the object."""
        return {
            "id": self.id,
            "media_type": self.media_type,
            "media_name": self.media_name,
            "url": self.url,
            "fs_path": self.fs_path
        }

    def save(self, session):
        """Persist the object."""
        session.add(self)

    @classmethod
    def get_by_id_and_type(cls, media_id, media_type, session):
        """Get a single instance identified by id and type."""
        if media_type not in MediaEnum:
            raise ValueError("Value {} not allowed for argument media_type. See media_type.py"
                             .format(media_type))

        query = session.query(cls)\
            .filter(and_(cls.id == media_id, cls.media_type == media_type))
        try:
            medias = query.one()
        except MultipleResultsFound:
            raise
        except NoResultFound:
            return None
        else:
            return medias

    @classmethod
    def get_by_name_and_type(cls, media_name, media_type, session):
        """Get a single instance identified by name and type."""
        if media_type not in MediaEnum:
            raise ValueError("Value {} not allowed for argument media_type. See media_type.py"
                             .format(media_type))

        query = session.query(cls)\
            .filter(and_(cls.media_name == media_name, cls.media_type == media_type))
        try:
            medias = query.one()
        except MultipleResultsFound:
            raise
        except NoResultFound:
            return None
        else:
            return medias

    @classmethod
    def get_list(cls, media_type, session):
        """Return a list of instances."""
        if media_type not in MediaEnum:
            raise ValueError("Value {} not allowed for argument media_type. See media_type.py"
                             .format(media_type))
        medias = session.query(cls).all()
        return medias

    def __repr__(self):
        """Return description of self."""
        return "<Media(id: {}, type: {}, name: {}, url: {}, path: {})>".format(
            self.id, self.media_type, self.media_name, self.url, self.fs_path)
