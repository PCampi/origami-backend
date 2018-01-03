"""Player resource."""

import json
import falcon

class Player(object):
    """Class representing an origami app player."""

    def __init__(self, name, age, gender):
        """Constructor."""
        self._name = name
        self._age = age
        self._gender = gender

    def on_get(self, req, resp):
        """Get a single player."""
        player = {
            "name": "Giovannino",
            "age": 9,
            "gender": "male"
        }

        resp.data = json.dumps(player)
        resp.status = falcon.HTTP_200
        