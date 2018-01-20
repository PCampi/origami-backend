"""Test for the Story import module."""

import json

from ..story_persistence import Story
from .base_test import OrigamiTestCase


class StoryTestCase(OrigamiTestCase):
    """Class for testing the story analysis."""

    def test_node_insertion(self):
        """Test for the story's nodes registration in db."""

        story_json = json.dumps({
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
                            "name": "audio2.mp3",
                            "type": "audio"
                        }
                    ],
                    "children": {

                    }
                }
            ]
        }, ensure_ascii=False)

        temp_filename = "temp.json"
        with open(temp_filename, "w") as outfile:
            outfile.write(story_json)

        story = Story()
        story.read_story_tree(temp_filename)
        story.insert_story_db()

        result = self.simulate_get(
            "/nodes", headers={"Authorization": "Bearer " + self.token}).json

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

        # FIXME: questo test continua ad aggiungere i nodi,
        # quindi al secondo giro si spacca.
        # Forse si può risolvere con un in-memory database solo per i test?
        self.assertEqual(target, result)
