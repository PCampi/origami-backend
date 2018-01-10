"""Superclass for all DAOs classes.
Since there are no Interfaces in Python, it is implemented as a mixin
class using sqlalchemy.
"""

from sqlalchemy.ext.declarative import declared_attr


class BaseDao(object):
    """Class representing a base DAO class.
    It provides the following methods:

    @property
    - as_dict(self):
        returns a dictionary representation of an object

    - save(self, database_session):
        persists this instance to the database

    - __repr__(self):
        returns a string description of self (same as toString() in Java)
    """

    @declared_attr
    def __tablename__(cls):  # pylint: disable=E0213
        """Define table name for all derived classes.
        All derived classed MUST end with 'Dao' suffix.
        """
        return cls.__name__.lower()[:-3]  # pylint: disable=E1101

    @property
    def as_dict(self):
        """Dictionary representation of this instance."""
        raise NotImplementedError("Property as_dict not yet implemented in class {}"
                                  .format(self.__class__.__name__))

    def save(self, session):
        """Persist this instance to database using the provided session.

        Parameters
        ----------
        session: sqlalchemy.orm.session.Session
            the sqlalchemy session used for the transaction
        """
        session.add(self)

    def __repr__(self):
        """Return a string representation of self."""
        raise NotImplementedError("Method __repr__ not yet implemented in class {}"
                                  .format(self.__class__.__name__))
