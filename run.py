"""Run this module as main."""

from werkzeug.serving import run_simple

# pylint: disable E0611
from origami import APPLICATION

if __name__ == '__main__':
    run_simple("localhost", 5000, APPLICATION)
