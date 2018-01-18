"""DAO module for the Administrator class."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from .meta import Base
from .base_dao import BaseDao


class AdministratorDao(BaseDao, Base):
    """DAO class for Administrator objects."""

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String(50))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    @property
    def as_dict(self):
        """Returns a dictionary representation of the object."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

    def save(self, session):
        """Persist the object."""
        session.add(self)

    @classmethod
    def get_by_id(cls, admin_id, session):
        """Get a single instance identified by its id."""
        query = session.query(cls).filter(cls.id == admin_id)
        try:
            admins = query.one()
        except MultipleResultsFound:
            raise
        except NoResultFound:
            return None
        else:
            return admins

    @classmethod
    def get_by_email_and_password(cls, admin_email, admin_pass, session):
        """Get a single instance identified by its email."""
        query = session.query(cls).filter(
            cls.email == admin_email and cls.password == admin_pass)
        try:
            admins = query.one()
        except MultipleResultsFound:
            raise
        except NoResultFound:
            return None
        else:
            return admins

    @classmethod
    def get_list(cls, session):
        """Get a list of instances from the db."""
        admins = session.query(cls).all()
        return admins

    def __repr__(self):
        """Return a description of self."""
        return "<Admin(id:{}, name:{}, email:{}, password:{})>".format(
            self.id, self.name, self.email, self.password)
