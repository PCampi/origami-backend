"""Main app module."""

import logging

import falcon
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from . import app_logging
from .db import AdministratorDao
from .middleware import (JwtAuthBackend, SessionedAuthMiddleware,
                         SQLAlchemySessionManager)
from .resources import accounts, login_admin, media, node, played_story, player

LOGGER = app_logging.get_logger("main", level=logging.DEBUG)


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


def create_app(db_engine, secret_key, jwt_issuer="pmc-mg.origami.it"):
    """Create the app."""
    session_factory = sessionmaker(bind=db_engine)
    db_session = scoped_session(session_factory)

    auth_backend = JwtAuthBackend(
        secret_key,
        AdministratorDao.validate,
        auth_header_prefix="Bearer",
        issuer=jwt_issuer,
        verify_claims=True
    )

    auth_middleware = SessionedAuthMiddleware(
        auth_backend,
        auth_header_prefix="Bearer",
        exempt_routes=["/login"],
        exempt_methods=["HEAD", "OPTIONS"]
    )

    api = falcon.API(middleware=[
        SQLAlchemySessionManager(db_session),
        auth_middleware
    ])

    api.add_route("/login", login_admin.Item(secret_key, jwt_issuer))
    api.add_route("/authorized_accounts",
                  accounts.Collection(secret_key, jwt_issuer))
    api.add_route(
        "/authorized_accounts/{user_id}", accounts.Item())
    api.add_route("/players", player.Collection())
    api.add_route("/players/{player_id}", player.Item())
    api.add_route("/medias", media.Collection())
    api.add_route("/medias/{media_type}", media.TypeCollection())
    api.add_route("/medias/{media_type}/{media_id}", media.Item())
    api.add_route("/nodes", node.Collection())
    api.add_route("/nodes/{node_id}", node.Item())
    api.add_route("/played_stories", played_story.Collection())
    api.add_route("/played_stories/{story_id}", played_story.StoryCollection())

    return api
