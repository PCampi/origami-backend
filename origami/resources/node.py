"""Node resource."""

import json

import falcon

from .sessioned_resource import SessionedResource
from ..db import NodeDao

class Item(SessionedResource):
    """Class to manage REST requests for the Node item."""

    def on_get(self, req, resp, node_id):
        """Get a single node."""
        node_orm = NodeDao.get_by_id(node_id, self.session)

        if node_orm:
            node = node_orm.as_dict

            resp.body = json.dumps(node, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_404

class Collection(SessionedResource):
    """Class to manage REST requests for the Node collection."""

    def on_get(self, req, resp):
        """Called on a GET for the collection."""
        nodes_orm = NodeDao.get_list(self.session)
        nodes = [node.as_dict for node in nodes_orm]

        resp.body = json.dumps(nodes, ensure_ascii=False)
        resp.status = falcon.HTTP_200