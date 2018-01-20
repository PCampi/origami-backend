"""Admin resource."""

import json
import logging

import falcon
import jwt

from .sessioned_resource import SessionedResource
from ..db import AdministratorDao

LOGGER = logging.getLogger("main.administrator")
LOGGER.setLevel(logging.DEBUG)


class Item(SessionedResource):
    """Class representing an origami app admin and authorized player account."""

    def on_get(self, req, resp, user_id):
        """Get a single admin identified by user_id."""
        admin_orm = AdministratorDao.get_by_id(user_id, self.session)

        if admin_orm:
            admin = admin_orm.as_safe_dict

            resp.body = json.dumps(admin, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404


class Collection(SessionedResource):
    """Class to manage REST requests for the Admin collection."""

    def __init__(self, secret_key: str, issuer: str) -> None:
        """Contructor

        Parameters
        ----------
        secret_key: str
            key used to encrypt JWT responses for new accounts
        """
        super().__init__()
        self.secret_key = secret_key
        self.issuer = issuer

    def on_get(self, req, resp):
        """Called on a GET for the collection."""
        admin_orm = AdministratorDao.get_all(self.session)
        admins = [admin.as_safe_dict for admin in admin_orm]

        resp.body = json.dumps(admins, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """Called when an app wants to authorize a new user."""
        content = json.load(req.bounded_stream)

        try:
            email = content["email"]
            name = content["user_name"]
            password = content["password"]
            # save the account only if there is not already an account by that email and password
            if not AdministratorDao.get_by_email_and_password(email, password, self.session):
                if not AdministratorDao.validate(email, self.session):
                    new_admin = AdministratorDao(name, email, password)
                    new_admin.save(self.session)
                    self.session.commit()

            # send back the new token as json
            new_account_token = jwt.encode(
                {"email": email, "iss": self.issuer},
                self.secret_key,
                algorithm='HS256'
            )

            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.data = new_account_token
        except KeyError:
            resp.status = falcon.HTTP_BAD_REQUEST
