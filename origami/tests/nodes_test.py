"""Unittest."""

import falcon

from .base_test_class import OrigamiTestCase


class NodesTestCase(OrigamiTestCase):
    """Class for testing nodes."""

    def test_get_nodes_list(self):
        """Test for the GET at /nodes."""
        result = self.simulate_get("/nodes",
                                   headers={"Authorization": "Bearer " + self.token}).json
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
        result = self.simulate_get("/nodes/1",
                                   headers={"Authorization": "Bearer " + self.token}).json
        target = {
            "id": 1,
            "name": "nodo_prova1"
        }

        self.assertEqual(target, result)

    def test_get_node_nonexistent(self):
        """Try to GET a nonexistent node."""
        result = self.simulate_get("/nodes/4",
                                   headers={"Authorization": "Bearer " + self.token}).status
        target = falcon.HTTP_404

        self.assertEqual(result, target)
