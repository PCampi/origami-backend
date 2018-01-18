"""Module for base test class."""

from falcon import testing

from ..main_app import create_app, get_engine


class OrigamiTestCase(testing.TestCase):
    """Base class for all tests."""

    def setUp(self):
        super(OrigamiTestCase, self).setUp()
        engine = get_engine(memory=False)
        self.app = create_app(engine)

    def tearDown(self):
        super(OrigamiTestCase, self).tearDown()
        self.secret_key = None
        self.app = None
