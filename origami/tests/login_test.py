"""Test for login."""

import logging

import falcon

from .base_test_class import OrigamiTestCase


logger = logging.getLogger("main.test_player")
logger.setLevel(logging.DEBUG)


class LoginTestCase(OrigamiTestCase):
    """Class for testing login with JWT."""

    def test_confirm_login(self):
        """Test for the GET at /players."""
        result = self.simulate_get("/players").json
        target = [
            {
                "id": 1,
                "name": "Giovannino",
                "age": 9,
                "gender": "male"
            },
            {
                "id": 2,
                "name": "Andreino",
                "age": 11,
                "gender": "male"
            },
            {
                "id": 3,
                "name": "Viola",
                "age": 8,
                "gender": "female"
            }
        ]

        self.assertEqual(target, result)

    def test_get_player(self):
        """Test for GET at /players/1."""
        result = self.simulate_get("/players/1").json
        target = {
            "id": 1,
            "name": "Giovannino",
            "age": 9,
            "gender": "male"
        }

        self.assertEqual(target, result)

    def test_get_player_nonexistent(self):
        """Try to GET a nonexistent player."""
        result = self.simulate_get("/players/4").status
        target = falcon.HTTP_404

        self.assertEqual(result, target)
