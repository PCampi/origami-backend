"""Unit test for the /authorized_accounts endpoint."""

import logging

import falcon

from .base_test_class import OrigamiTestCase


LOGGER = logging.getLogger("main.accounts_test")
LOGGER.setLevel(logging.DEBUG)


class AccountsTestCase(OrigamiTestCase):
    """Class for testing the /authorized_accounts endpoint."""

    url = "/authorized_accounts"

    def test_get_all_accounts(self):
        """Test for the GET at /authorized_accounts."""
        result = self.simulate_get(
            self.url, headers={"Authorization": "Bearer " + self.token}).json
        target = [
            {
                "id": 1,
                "name": "Pippo",
                "email": "pippo@gmail.com"
            },
            {
                "id": 2,
                "name": "Pluto",
                "email": "pluto@gmail.com"
            },
            {
                "id": 3,
                "name": "Paperino",
                "email": "paperino@gmail.com"
            }
        ]

        self.assertEqual(target, result)

    def test_get_account(self):
        """Test for GET at /players/1."""
        result = self.simulate_get(
            self.url + "/1", headers={"Authorization": "Bearer " + self.token}).json
        target = {
            "id": 1,
            "name": "Pippo",
            "email": "pippo@gmail.com"
        }

        self.assertEqual(target, result)

    def test_get_player_nonexistent(self):
        """Try to GET a nonexistent player."""
        result = self.simulate_get(
            self.url + "/4", headers={"Authorization": "Bearer " + self.token}).status
        target = falcon.HTTP_404

        self.assertEqual(result, target)

    def test_authorization_ok(self):
        """Test that the authorization mechanism works."""
        url = "/authorized_accounts"
        result = self.simulate_get(
            url, headers={"Authorization": "Bearer " + self.token})

        accounts = result.json
        self.assertIsNotNone(accounts)
        self.assertEqual(len(accounts), 3)
        self.assertEqual(result.status, falcon.HTTP_200)

    def test_authorization_failed(self):
        """Test that the authorization mechanism works."""
        url = "/authorized_accounts"
        result = self.simulate_get(
            url, headers={"Authorization": "Bearer 234-ga-324"})
        self.assertEqual(result.status, falcon.HTTP_BAD_REQUEST)

        wrong_token = self.token[:-1] + "A"
        result = self.simulate_get(
            url, headers={"Authorization": "Bearer " + wrong_token})
        self.assertEqual(result.status, falcon.HTTP_BAD_REQUEST)

        wrong_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9." + \
            "eyJlbWFpbCI6InBpcHBvQGdtYXVsLmNvbSIsImlzcyI6InBtYy5vcmlnYW1pLml0In0." + \
            "G1GKJc5B_coyUkiz7SdjoehDKaWnQGaVFzbAEYVG2-4"
        result = self.simulate_get(
            url, headers={"Authorization": "Bearer " + wrong_token})
        self.assertEqual(result.status, falcon.HTTP_UNAUTHORIZED)
