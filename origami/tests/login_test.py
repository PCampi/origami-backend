"""Test for login."""

import logging

import falcon

from .base_test_class import OrigamiTestCase


logger = logging.getLogger("main.test_player")
logger.setLevel(logging.DEBUG)


class LoginTestCase(OrigamiTestCase):
    """Class for testing login with JWT."""

    def test_confirm_login(self):
        """Test for the POST at /login."""
        admin_user = {"user": "pippo@gmail.com", "password": "pippo1"}
        result = self.simulate_post("/login", json=admin_user)

        self.assertEqual(result.status, falcon.HTTP_200)
