"""Player resource."""

import json
import logging

import falcon

logger = logging.getLogger("main.player")
logger.setLevel(logging.DEBUG)


class Item(object):
    """Class representing an origami app player."""

    def on_get(self, req, resp, player_id):
        """Get a single player."""
        logger.info("Got get request")
        player = {
            "id": 1,
            "name": "Giovannino",
            "age": 9,
            "gender": "male"
        }

        resp.body = json.dumps(player, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class Collection(object):
    """Class to manage REST requests for the Player collection."""

    def on_get(self, req, resp):
        """Called on a GET for the collection."""
        players = [
            {
                "id": 1,
                "name": "Giovannino",
                "age": 9,
                "gender": "male"
            },
            {
                "id": 2,
                "name": "Lucia",
                "age": 7,
                "gender": "female"
            }
        ]

        resp.body = json.dumps(players, ensure_ascii=False)
        resp.status = falcon.HTTP_200
