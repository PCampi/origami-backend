"""Unittest."""

import logging

import falcon

from .base_test_class import OrigamiTestCase


logger = logging.getLogger("main.test_nodes")
logger.setLevel(logging.DEBUG)


class NodesTestCase(OrigamiTestCase):
    """Class for testing nodes."""

    def test_get_nodes_list(self):
        """Test for the GET at /nodes."""
        result = self.simulate_get("/nodes").json
        target = [
            {
                "id": 1,
                "name": "nodo_prova1"
            },
            {
                "id": 2,
                "name": "nodo_prova2"
            },
            {
                "id": 3,
                "name": "nodo_prova3"
            }
        ]

        self.assertEqual(target, result)

    def test_get_node(self):
        """Test for GET at /nodes/1."""
        result = self.simulate_get("/nodes/1").json
        target = {
            "id": 1,
            "name": "nodo_prova1"
        }

        self.assertEqual(target, result)

    def test_get_node_nonexistent(self):
        """Try to GET a nonexistent node."""
        result = self.simulate_get("/nodes/4").status
        target = falcon.HTTP_404

        self.assertEqual(result, target)