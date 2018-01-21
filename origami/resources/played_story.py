"""Played Story resource."""

import json

import falcon

from .sessioned_resource import SessionedResource
from ..db import PlayerDao, PlayedStoryDao, PlayedChoicesDao, EndingDao


class StoryNotFoundException(Exception):
    """Raised when a Story is not found."""
    pass


def compose_json(story, player, choices, ending):
    """Composes the played story in a json doc."""
    return {
        "played_story": story,
        "player": player,
        "choices": choices,
        "ending": ending
    }


def find_elements(story_id, session):
    """Finds the elements composing a played story."""
    story_orm = PlayedStoryDao.get_by_id(story_id, session)
    if story_orm is None:
        raise StoryNotFoundException(
            "Story with id {} not found".format(story_id))

    story = story_orm.as_dict["id"]

    player_orm = PlayerDao.get_by_id(story_orm.player_id, session)
    player = player_orm.as_dict

    choices_orm = PlayedChoicesDao.get_by_id(story_id, session)
    choices = [choice.as_dict["node_id"] for choice in choices_orm]

    ending_orm = EndingDao.get_by_played_story_id(story_id, session)
    ending = ending_orm.text

    result = compose_json(story, player, choices, ending)

    return result


class Item(SessionedResource):
    """Class to manage REST requests for the Story choices collection."""

    def on_get(self, req, resp, story_id):
        """Called on a GET for the collection."""
        try:
            result = find_elements(story_id, self.session)
            resp.body = json.dumps(result, ensure_ascii=False)
            resp.status = falcon.HTTP_200
        except StoryNotFoundException:
            resp.status = falcon.HTTP_NOT_FOUND


class Collection(SessionedResource):
    """Class to manage REST requests for the Story collection."""

    def on_get(self, req, resp):
        """Called on a GET for the collection."""
        stories_orm = PlayedStoryDao.get_list(self.session)
        stories = [story.as_dict["id"] for story in stories_orm]

        result = [find_elements(story, self.session) for story in stories]

        resp.body = json.dumps(result, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """Called on a POST for a new story in the collection."""
        story = json.load(req.bounded_stream)

        player_info = story["player"]
        choices_nodes = story["choices"]
        ending_text = story["ending"]

        player = PlayerDao.get_by_profile(
            player_info["name"], player_info["age"], player_info["gender"], self.session)
        if player is None:
            player = PlayerDao(
                player_info["name"], player_info["age"], player_info["gender"])
            player.save(self.session)

        played_story = PlayedStoryDao(player.id)
        played_story.save(self.session)

        for index, choices_node in enumerate(choices_nodes):
            choice = PlayedChoicesDao(played_story.id, index + 1, choices_node)
            choice.save(self.session)

        ending = EndingDao(played_story.id, ending_text)
        ending.save(self.session)

        resp.status = falcon.HTTP_200
