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


def create_app(db_mode_memory=False):
    """Create the app."""
    db_engine = get_engine(memory=db_mode_memory)
    session_factory = sessionmaker(bind=db_engine)
    db_session = scoped_session(session_factory)

    api = falcon.API(middleware=[
        SQLAlchemySessionManager(db_session)
    ])

    api.add_route("/players", player.Collection())
    api.add_route("/players/{id}", player.Item())

    return api
