"""Module for base test class."""

import falcon
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
        engine = get_engine(memory=False)

        self.issuer = "pmc-mg.origami.it"
        self.secret_key = "fb9eda68-fc64-11e7-9f9b-b8e856411f9c"
        self.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9." + \
            "eyJlbWFpbCI6InBpcHBvQGdtYWlsLmNvbSIsImlzcyI6InBtYy5vcmlnYW1pLml0In0." + \
            "xiboUkPthBDDonEinSVdiWF0R_WdkmSMWL89c-7xaiE"

        self.app = create_app(engine, self.secret_key)

    def tearDown(self):
        super(OrigamiTestCase, self).tearDown()
        self.secret_key = None
        self.app = None
        self.token = None
