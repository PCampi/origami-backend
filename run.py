"""Run this module as main."""

from werkzeug.serving import run_simple

import origami

if __name__ == '__main__':
    ENGINE = origami.get_engine(memory=False)
    secret = "fb9eda68-fc64-11e7-9f9b-b8e856411f9c"
    run_simple("localhost", 5000, origami.create_app(ENGINE, secret))
