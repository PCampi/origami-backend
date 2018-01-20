"""Ending resource."""

import json

import falcon

from .sessioned_resource import SessionedResource
from ..db import EndingDao


class Item(SessionedResource):
    """Class to manage REST requests for the Ending item."""

    def on_get(self, req, resp, ending_id):
        """Get a single ending."""
        ending_orm = EndingDao.get_by_id(ending_id, self.session)

        if ending_orm:
            ending = ending_orm.as_dict

            resp.body = json.dumps(ending, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404


class Collection(SessionedResource):
    """Class to manage REST requests for the Ending collection."""

    def on_get(self, req, resp):
        """Called on a GET for the collection."""
        endings_orm = EndingDao.get_list(self.session)
        endings = [ending.as_dict for ending in endings_orm]

        resp.body = json.dumps(endings, ensure_ascii=False)
        resp.status = falcon.HTTP_200
