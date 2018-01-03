"""Main app module."""

import falcon
from werkzeug.serving import run_simple

from .db.meta import Session as DBSESSION
from .middleware.db_session_manager import SQLAlchemySessionManager

API = APPLICATION = falcon.API(middleware=[
    SQLAlchemySessionManager(DBSESSION)
])


if __name__ == "__main__":
    run_simple("localhost", 5000, APPLICATION)
