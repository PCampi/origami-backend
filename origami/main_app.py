"""Main app module."""

import logging

import falcon
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from . import app_logging
from .middleware import SQLAlchemySessionManager, get_aut_middleware
from .resources import player, login_admin

logger = app_logging.get_logger("main", level=logging.DEBUG)


def get_engine(memory=False):
    """Get the SQLAlchemy engine."""
    if memory:
        logger.info("Creating memory database")
        return create_engine("sqlite:///:memory:", echo=True)
    else:
        logger.info("Creating engine for postgres")
        db_name = "origami_db"
        db_user = "origami_user"
        db_password = "origami_password"

        url = "postgres://{}:{}@localhost:5432/{}".format(
            db_user, db_password, db_name
        )

        return create_engine(url, echo=True)


def create_app(db_engine, secret_key):
    """Create the app."""
    session_factory = sessionmaker(bind=db_engine)
    db_session = scoped_session(session_factory)

    api = falcon.API(middleware=[
        SQLAlchemySessionManager(db_session)  # ,
        # get_aut_middleware(secret_key, exempt_routes=["/login"])
    ])

    # api.add_route("/login", login_admin.Item())
    api.add_route("/players", player.Collection())
    api.add_route("/players/{player_id}", player.Item())

    return api
