"""Module for base test class."""

import jwt
from falcon import testing

from ..main_app import create_app, get_engine


class OrigamiTestCase(testing.TestCase):
    """Base class for all tests."""

    def setUp(self):
        """Default setUp which:

        - creates the app as self.app
        - sets a valid jwt token in self.aut_token
        """
        super(OrigamiTestCase, self).setUp()
        self.secret_key = "fb9eda68-fc64-11e7-9f9b-b8e856411f9c"
        engine = get_engine(memory=False)
        # TODO: finire creazione token jwt
        self.app = create_app(engine, self.secret_key)

    def tearDown(self):
        super(OrigamiTestCase, self).tearDown()
        self.secret_key = None
        self.app = None
