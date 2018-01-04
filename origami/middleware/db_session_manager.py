"""Middleware which creates a scoped session for each request."""

import logging

logger = logging.getLogger("main.db_mw")


class SQLAlchemySessionManager(object):
    """Create a scoped session for every request and closes it."""

    def __init__(self, session):
        self.session = session

    def process_resource(self, req, resp, resource, params):
        """Set up a session for this request."""
        resource.session = self.session()
        logger.debug("Started session %(session)s",
                     {"session": resource.session})

    def process_response(self, req, resp, resource, req_succeeded):
        """Close the session."""
        if hasattr(resource, "session"):
            if not req_succeeded:
                resource.session.rollback()
                logger.debug("Rollbacked session %(session)s", {"session": resource.session})
            self.session.remove()
            logger.debug("Removed session %(session)s", {"session": resource.session})
