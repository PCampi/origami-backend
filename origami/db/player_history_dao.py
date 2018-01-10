"""DAO module for the Player History class."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from .meta import Base
from .base_dao import BaseDao

class PlayerHistoryDao(BaseDao, Base):
    """DAO class for Player History objects."""

    id = Column(Integer, primary_key = True)