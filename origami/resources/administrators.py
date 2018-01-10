"""Admin resource."""

import json
import logging

import falcon

from .sessioned_resource import SessionedResource
from ..db import AdministratorDao

logger = logging.getLogger("main.administrator")
logger.setLevel(logging.DEBUG)

class Item(SessionedResource):
    """Class representing an origami app admin."""

    def on_get(self, req, resp, admin_id):
        """Get a single admin."""
        admin_orm = AdministratorDao.get_by_id(admin_id, self.session)

        if admin_orm:
            admin = admin_orm.as_dict

            resp.body = json.dumps(admin, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404

class Collection(SessionedResource):
    """Class to manage REST requests for the Admin collection."""

    def on_get(self, req, resp):
        """Called on a GET for the collection."""
        admin_orm = AdministratorDao.get_list(self.session)
        admins = [admin.as_dict for admin in admin_orm]

        resp.body = json.dumps(admins, ensure_ascii=False)
        resp.status = falcon.HTTP_200