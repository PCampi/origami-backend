"""Module for base test class."""

from falcon import testing

from ..main_app import create_app, get_engine
from .. import db_utils


class OrigamiTestCase(testing.TestCase):
    """Base class for all tests."""

    @classmethod
    def setUpClass(cls):
        """Called whenever a test class is instantiated."""
        cls.engine = get_engine(memory=False)
        cls.clean_test_db(cls, cls.engine)

    @classmethod
    def tearDownClass(cls):
        """Called upon object destruction."""
        cls.clean_test_db(cls, cls.engine)

    def setUp(self):
        """Default setUp which:

        - creates a test database
        - creates the app as self.app
        - sets a valid jwt token in self.aut_token
        """
        super(OrigamiTestCase, self).setUp()
        self.clean_test_db(self.engine)
        self.create_test_db(self.engine)

        self.issuer = "pmc-mg.origami.it"
        self.secret_key = "fb9eda68-fc64-11e7-9f9b-b8e856411f9c"
        self.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9." + \
            "eyJlbWFpbCI6InBpcHBvQGdtYWlsLmNvbSIsImlzcyI6InBtYy5vcmlnYW1pLml0In0." + \
            "xiboUkPthBDDonEinSVdiWF0R_WdkmSMWL89c-7xaiE"

        self.app = create_app(self.engine, self.secret_key)

    def tearDown(self):
        """Cleans after each test is run.

        - deletes all members
        - cleans the database
        """
        super(OrigamiTestCase, self).tearDown()
        self.secret_key = None
        self.app = None
        self.token = None
        self.clean_test_db(self.engine)

    def create_test_db(self, engine=None):
        """Set up dummy data in the database."""
        db_utils.insert_dummy_data(engine)

    def clean_test_db(self, engine=None):
        """Clean the database by dropping all tables."""
        db_utils.clean_database(engine)
