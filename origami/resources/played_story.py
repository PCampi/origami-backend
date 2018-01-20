"""Played Story resource."""

import json

import falcon

from .sessioned_resource import SessionedResource
from ..db import PlayedStoryDao, PlayedChoicesDao, EndingDao

class StoryCollection(SessionedResource):
    """Class to manage REST requests for the Story choices collection."""

    def on_get(self, req, resp, story_id):
        """Called on a GET for the collection."""
        stories_orm = PlayedStoryDao.get_by_id(story_id, self.session)
        stories = [story.as_dict for story in stories_orm]

        choices_orm = PlayedChoicesDao.get_by_id(story_id, self.session)
        choices = [choice.as_dict for choice in choices_orm]
        
        #Non avevo idea di come restituire entrambe le liste insieme
        resp.body = json.dumps(stories, ensure_ascii=False) + json.dumps(choices, ensure_ascii=False)
        resp.status = falcon.HTTP_200

class Collection(SessionedResource):
    """Class to manage REST requests for the Story collection."""

    def on_get(self, req, resp):
        """Called on a GET for the collection."""
        stories_orm = PlayedStoryDao.get_list(self.session)
        stories = [story.as_dict for story in stories_orm]

        choices_orm = PlayedChoicesDao.get_list(self.session)
        choices = [choice.as_dict for choice in choices_orm]

        #Idem come sopra
        resp.body = json.dumps(stories, ensure_ascii=False) + json.dumps(choices, ensure_ascii=False)
        resp.status = falcon.HTTP_200
