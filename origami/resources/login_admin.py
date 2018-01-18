"""Admin login."""

import json
import logging

import falcon
import jwt

from .sessioned_resource import SessionedResource
from ..db import AdministratorDao

logger = logging.getLogger("main.administrator")
logger.setLevel(logging.DEBUG)

class Item(SessionedResource):
    """Class representing an item login."""

    def on_post(self, req, resp, **kwargs):
        doc = json.load(req.bounded_stream)
        admin = AdministratorDao.get_by_email(doc["user"], doc["password"], self.session)
        if admin is None:
            resp.status = falcon.HTTP_403
        else:
            token = jwt.encode({'user': doc["user"]}, 'secret', algorithm='HS256') #TODO
            resp.status = falcon.HTTP_200
            resp.data = token
