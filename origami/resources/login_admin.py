"""Admin login."""

import json
import logging

import falcon
import jwt

from .sessioned_resource import SessionedResource
from ..db import AdministratorDao

LOGGER = logging.getLogger("main.admin-login")
LOGGER.setLevel(logging.DEBUG)

# pylint: disable=R0903


class Item(SessionedResource):
    """Class representing an item login."""

    def __init__(self, secret_key: str, issuer: str) -> None:
        """Constructor

        Parameters
        ----------
        secret_key: str
            secret key used to encode the jwt token
        """
        super().__init__()
        self.secret_key = secret_key
        self.issuer = issuer

    def on_post(self, req, resp):
        """Login endpoint for admins."""
        doc = json.load(req.bounded_stream)
        email = doc["email"]
        password = doc["password"]

        admin = AdministratorDao.get_by_email_and_password(
            email, password, self.session)

        if admin is None:
            resp.status = falcon.HTTP_403
        else:
            token = jwt.encode(
                {"email": doc["email"], "iss": self.issuer},
                self.secret_key, algorithm="HS256")  # type: bytes
            resp.status = falcon.HTTP_200
            resp.data = token
