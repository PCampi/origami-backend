"""Unittest."""

import logging

import falcon

from .base_test import OrigamiTestCase


LOGGER = logging.getLogger("main.test_player")
LOGGER.setLevel(logging.DEBUG)


class PlayersTestCase(OrigamiTestCase):
    """Class for testing players."""

    def test_get_players_list(self):
        """Test for the GET at /players."""
        result = self.simulate_get(
            "/players", headers={"Authorization": "Bearer " + self.token}).json
        target = [
            {
                "id": 1,
                "name": "Gianni",
                "age": 9,
                "gender": "male"
            },
            {
                "id": 2,
                "name": "Federica",
                "age": 8,
                "gender": "female"
            },
            {
                "id": 3,
                "name": "Josh",
                "age": 6,
                "gender": "male"
            }
        ]

        self.assertEqual(target, result)

    def test_get_player(self):
        """Test for GET at /players/1."""
        result = self.simulate_get(
            "/players/1", headers={"Authorization": "Bearer " + self.token}).json
        target = {
            "id": 1,
            "name": "Gianni",
            "age": 9,
            "gender": "male"
        }

        self.assertEqual(target, result)

    def test_get_player_nonexistent(self):
        """Try to GET a nonexistent player."""
        result = self.simulate_get(
            "/players/4", headers={"Authorization": "Bearer " + self.token}).status
        target = falcon.HTTP_404

        self.assertEqual(result, target)
