"""Run this module as main."""

from werkzeug.serving import run_simple

import origami

if __name__ == '__main__':
    ENGINE = origami.get_engine(memory=False)
    run_simple("localhost", 5000, origami.create_app(ENGINE))
