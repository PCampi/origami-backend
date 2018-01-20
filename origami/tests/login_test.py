"""Test for login."""

import logging

import falcon
import jwt

from .base_test_class import OrigamiTestCase


LOGGER = logging.getLogger("main.test_player")
LOGGER.setLevel(logging.DEBUG)


class LoginTestCase(OrigamiTestCase):
    """Class for testing login with JWT."""

    def setUp(self):
        """Called before every test."""
        super(LoginTestCase, self).setUp()
        self.url = "/login"
        self.user_name = "pippo@gmail.com"
        self.user_password = "pippo1"

    def test_confirm_login(self):
        """Test for the POST at /login."""
        admin_user = {"user": self.user_name, "password": self.user_password}
        result = self.simulate_post(self.url, json=admin_user)

        self.assertEqual(result.status, falcon.HTTP_200)

        result_token_bytes = result.content
        expected_token_bytes = jwt.encode(
            {"user": self.user_name}, self.secret_key)  # type: bytes

        self.assertEqual(result_token_bytes, expected_token_bytes)

        result_token_str = result.text
        expected_token_str = expected_token_bytes.decode("utf-8")  # type: str

        self.assertEqual(result_token_str, expected_token_str)

        result_user = jwt.decode(result_token_bytes, self.secret_key)
        expected_user = {"user": self.user_name}

        self.assertEqual(result_user, expected_user)

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
