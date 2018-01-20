"""Unittest."""

import logging

import falcon

from .base_test_class import OrigamiTestCase
from ..story_persistence import Story


logger = logging.getLogger("main.test_story")
logger.setLevel(logging.DEBUG)


class StoryTestCase(OrigamiTestCase):
    """Class for testing the story analysis."""

    def test_node_insertion(self):
        """Test for the story's nodes registration in db."""

        story_json = {
            "name": "node1",
            "media": [
                {
                    "name": "text1.txt",
                    "type": "text"
                },
                {
                    "name": "video1.mp4",
                    "type": "video"
                }
            ],
            "children": [
                {
                    "name": "node2",
                    "media": [
                        {
                            "name": "audio1.mp3",
                            "type": "audio"
                        }
                    ],
                    "children": {

                    }
                },
                {
                    "name": "node3",
                    "media": [
                        {
                            "name": "audio2",
                            "type": "audio"
                        }
                    ],
                    "children": {

                    }
                }
            ]
        }

        story = Story()
        story.read_story_tree(story_json)
        story.insert_story_db()

        result = self.simulate_get("/nodes").json

        target = [
            {
                "id": 1,
                "name": "node_prova1"
            },
            {
                "id": 2,
                "name": "node_prova2"
            },
            {
                "id": 3,
                "name": "node_prova3"
            },
            {
                "id": 4,
                "name": "node1"
            },
            {
                "id": 5,
                "name": "node2"
            },
            {
                "id": 6,
                "name": "node3"
            }
        ]

        self.assertEqual(target, result)
        