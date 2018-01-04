"""Main app module."""

import logging

import falcon
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from . import app_logging
from .middleware import SQLAlchemySessionManager
from .resources import player

logger = app_logging.get_logger("main", level=logging.DEBUG)


def get_engine(memory=False):
    """Get the SQLAlchemy engine."""
    if memory:
        logger.info("Creating memory database")
        return create_engine("sqlite:///:memory:", echo=True)
    else:
        logger.info("Creating persistent database with postgres")
        return create_engine(
            "postgres://user:password@localhost:5342/origami-dev"
        )


DB_ENGINE = get_engine(memory=True)
SESSION_FACTORY = sessionmaker(bind=DB_ENGINE)
DBSESSION = scoped_session(SESSION_FACTORY)

API = APPLICATION = falcon.API(middleware=[
    SQLAlchemySessionManager(DBSESSION)
])

API.add_route("/players", player.Collection())
API.add_route("/players/{id}", player.Item())
