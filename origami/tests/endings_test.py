"""Unittest."""

import logging

import falcon

from .base_test_class import OrigamiTestCase


logger = logging.getLogger("main.test_ending")
logger.setLevel(logging.DEBUG)

class EndingsTestCase(OrigamiTestCase):
    """Class for testing endings."""

    def test_get_endings_list(self):
        """Test for the GET at /endings."""
        result = self.simulate_get("/endings").json
        target = [
            {
                "id": 1,
                "played_story_id": 1,
                "text": "La storia finisce bene."
            },
            {
                "id": 2,
                "played_story_id": 2,
                "text": "La storia finisce male."
            },
            {
                "id": 3,
                "played_story_id": 3,
                "text": "La storia finisce malissimo."
            },
            {
                "id": 4,
                "played_story_id": 4,
                "text": "La storia finisce così così."
            }
        ]

        self.assertEqual(target, result)

    def test_get_ending(self):
        """Test for GET at /endings/1."""
        result = self.simulate_get("/endings/1").json
        target = {
                "id": 1,
                "played_story_id": 1,
                "text": "La storia finisce bene."
            }

        self.assertEqual(target, result)

    def test_get_ending_nonexistent(self):
        """Try to GET a nonexistent ending."""
        result = self.simulate_get("/endings/5").status
        target = falcon.HTTP_404

        self.assertEqual(result, target)