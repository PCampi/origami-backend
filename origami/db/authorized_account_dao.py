"""Dao for the authentication tokens."""

from sqlalchemy import Column, Integer, String

from .base_dao import BaseDao
from .meta import Base


class InvalidAccountException(Exception):
    """Custom exception raised when the account is not found
    in the database."""
    pass


class AuthorizedAccountDao(BaseDao, Base):
    """DAO class for Administrator objects."""

    id = Column(Integer, primary_key=True, nullable=False)
    account_name = Column(String(50), nullable=False)

    def __init__(self, account_name):
        self.account_name = account_name

    @property
    def as_dict(self):
        """Returns a dictionary representation of the object."""
        return {
            "id": self.id,
            "account_name": self.account_name
        }

    @classmethod
    def get_by_account_name(cls, account_name, session):
        """Get an account by its account_name."""
        query = session.query(cls).filter(cls.account_name == account_name)
        account = cls.get_one(query)
        return account

    @classmethod
    def get_by_id(cls, account_id, session):
        """Get an account by its id."""
        query = session.query(cls).filter(cls.id == account_id)
        account = cls.get_one(query)
        return account

    @classmethod
    def validate(cls, account_name, session):
        """Validate an account."""
        query = session.query(cls).filter(cls.account_name == account_name)
        account = cls.get_one(query)

        if account is None:
            raise InvalidAccountException(
                "Account with name={} not found in authorized accounts".format(account_name))

        return account

    def __repr__(self):
        """Return a description of self."""
        return "<AuthorizedAccount(account_name: {})>".format(self.account_name)
