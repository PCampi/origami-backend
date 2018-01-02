"""Media resource."""

import json

import falcon


class Media(object):
    """Class representing a generic media type."""

    def on_get(self, req, resp):
        """Get a single media."""
        media = {
            "id": 1,
            "type": "image",
            "url": "http://lorempixel.com/100/100"
        }

        resp.data = json.dumps(media)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """Post a single media."""
        name = "boh.jpg"
        resp.status = falcon.HTTP_201
        resp.location = "/images/" + name
