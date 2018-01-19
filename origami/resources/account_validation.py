"""Account validation resource."""

import json
import logging

import falcon
import jwt

from .sessioned_resource import SessionedResource
from ..db import AuthorizedAccountDao

LOGGER = logging.getLogger("main.administrator")
LOGGER.setLevel(logging.DEBUG)


class Item(SessionedResource):
    """Class representing an origami app authorized player account."""

    def on_get(self, req, resp, account_id):
        """Get a single account item identified by account_id."""
        account = AuthorizedAccountDao.get_by_id(account_id, self.session)

        if account:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(account.as_dict, ensure_ascii=False)
            resp.content_type = falcon.MEDIA_JSON
        else:
            resp.status = falcon.HTTP_404
            resp.body = "Account with id={} not found".format(account_id)


class Collection(SessionedResource):
    """Class to manage REST requests for the Admin collection."""

    def __init__(self, secret_key: str):
        """Contructor

        Parameters
        ----------
        secret_key: str
            key used to encrypt JWT responses for new accounts
        """
        super().__init__()
        self.secret_key = secret_key

    def on_post(self, req, resp):
        """Called when an app wants to authorize a new user."""
        content = json.load(req.bounded_stream)

        try:
            account_name = content["account_name"]
            # save the account only if there is not already an account by that name
            if not AuthorizedAccountDao.get_by_account_name(account_name, self.session):
                new_account = AuthorizedAccountDao(account_name)
                new_account.save(self.session)
                self.session.commit()

            # send back the new token as json
            new_account_token = jwt.encode(
                {"account_name": account_name},
                self.secret_key,
                algorithm='HS256'
            )

            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
            resp.data = new_account_token
        except KeyError:
            resp.status = falcon.HTTP_BAD_REQUEST

    def on_get(self, req, resp):
        """Get all accounts."""
        accounts_orm = AuthorizedAccountDao.get_all(self.session)
        accounts = [account.as_dict for account in accounts_orm]

        if accounts:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(accounts)
            resp.content_type = falcon.MEDIA_JSON
        else:
            resp.status = falcon.HTTP_404
            resp.body = "No authorized accounts created yet."
