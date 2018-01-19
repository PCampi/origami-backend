"""Test for login."""

import logging

import falcon

from .base_test_class import OrigamiTestCase


logger = logging.getLogger("main.test_player")
logger.setLevel(logging.DEBUG)


class LoginTestCase(OrigamiTestCase):
    """Class for testing login with JWT."""

    def setUp(self):
        """Called before every test."""
        super(LoginTestCase, self).setUp()
        self.url = "/login"

    def test_confirm_login(self):
        """Test for the POST at /login."""
        admin_user = {"user": "pippo@gmail.com", "password": "pippo1"}
        result = self.simulate_post(self.url, json=admin_user)

        self.assertEqual(result.status, falcon.HTTP_200)

    def test_refuse_login(self):
        """Test that it refuses login with incorrect credential."""
        non_existent_user = {"user": "pippauz@gmail.com", "password": "pluto2"}
        result_nonexistent_user = self.simulate_post(
            self.url, json=non_existent_user)

        self.assertEqual(result_nonexistent_user.status, falcon.HTTP_403)

        incorrect_password = {"user": "pippo@gmail.com",
                              "password": "wrong_password"}
        result_incorrect_password = self.simulate_post(
            self.url, json=incorrect_password)

        self.assertEqual(result_incorrect_password.status, falcon.HTTP_403)
