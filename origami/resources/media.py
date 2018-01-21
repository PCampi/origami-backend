"""Media resource."""

import json

import falcon

from .sessioned_resource import SessionedResource
from ..db import MediaDao


class Item(SessionedResource):
    """Class to manage REST requests for the Media item."""

    def on_get(self, req, resp, media_type, media_id):
        """Get a single media."""
        media_orm = MediaDao.get_by_id_and_type(
            media_id, media_type, self.session)

        if media_orm:
            media = media_orm.as_dict

            resp.body = json.dumps(media, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404


class TypeCollection(SessionedResource):
    """Class to manage REST requests for the Media type collection."""

    def on_get(self, req, resp, media_type):
        """Called on a GET for the collection."""
        medias_orm = MediaDao.get_list_by_type(media_type, self.session)
        medias = [media.as_dict for media in medias_orm]

        resp.body = json.dumps(medias, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class Collection(SessionedResource):
    """Class to manage REST requests for the Media collection."""

    def on_get(self, req, resp):
        """Called on a GET for the collection."""
        medias_orm = MediaDao.get_all(self.session)
        medias = [media.as_dict for media in medias_orm]

        resp.body = json.dumps(medias, ensure_ascii=False)
        resp.status = falcon.HTTP_200
