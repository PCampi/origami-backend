"""Main app module."""

import logging

import falcon
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from . import app_logging
from .middleware import SQLAlchemySessionManager, SessionedJWTBackend, SessionedJWTMiddleware
from .resources import player, login_admin, account_validation
from .db import AuthorizedAccountDao

LOGGER = app_logging.get_logger("main", level=logging.DEBUG)


def validate_user(decoded_token: str, session):
    """Function used to validate a user decoded from a JWT token."""


def get_engine(memory=False):
    """Get the SQLAlchemy engine."""
    if memory:
        LOGGER.info("Creating memory database")
        return create_engine("sqlite:///:memory:", echo=True)
    else:
        LOGGER.info("Creating engine for postgres")
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

    auth_backend = SessionedJWTBackend(
        AuthorizedAccountDao.validate,
        secret_key,
        algorithm='HS256',
        auth_header_prefix='jwt',
        leeway=30,
        expiration_delta=24 * 60 * 60,
        audience="it.origami.pmc",
        verify_claims=["exp"],
        required_claims=["exp"]
    )

    auth_middleware = SessionedJWTMiddleware(
        auth_backend,
        exempt_routes=["/login"],
        exempt_methods=["HEAD"]
    )

    api = falcon.API(middleware=[
        SQLAlchemySessionManager(db_session),
        auth_middleware
    ])

    api.add_route("/login", login_admin.Item(secret_key))
    api.add_route("/authorized_accounts",
                  account_validation.Collection(secret_key))
    api.add_route(
        "/authorized_accounts/{account_id}", account_validation.Item())
    api.add_route("/players", player.Collection())
    api.add_route("/players/{player_id}", player.Item())

    return api
