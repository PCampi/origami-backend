"""DAO module for the Player class."""

from sqlalchemy import Column, Integer, String

from .meta import Base


class PlayerDao(Base):
    """DAO class for Player objects."""
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
    gender = Column(String(6))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    @property
    def as_dict(self):
        """Returns a dictionary representation of the object."""
        return {
            "name": self.name,
            "age": self.age,
            "gender": self.gender
        }

    def save(self, session):
        """Persist the object."""
        with session.begin():
            session.add(self)

    @classmethod
    def get_list(cls, session):
        """Get a list of instances from the db."""
        models = []

        with session.begin():
            query = session.query(cls)
            models = query.all()

        return models

    def __repr__(self):
        """Return a description of self."""
        return "<Player(id:{}, name:{}, age:{}, gender:{})>".format(self.id, self.name, self.age, self.gender)
