"""Unittest."""

import falcon

from .base_test import OrigamiTestCase


class MediasTestCase(OrigamiTestCase):
    """Class for testing medias."""

    def test_get_medias_list(self):
        """Test for the GET at /medias."""
        result = self.simulate_get("/medias",
                                   headers={"Authorization": "Bearer " + self.token}).json
        target = [
            {
                "id": 1,
                "type": "audio",
                "name": "audio1.mp3",
                "url": None,
                "path": None
            },
            {
                "id": 2,
                "type": "video",
                "name": "video1.mp4",
                "url": None,
                "path": None
            },
            {
                "id": 3,
                "type": "text",
                "name": "text1.txt",
                "url": None,
                "path": None
            },
            {
                "id": 4,
                "type": "image",
                "name": "image1.jpg",
                "url": None,
                "path": None
            },
            {
                "id": 5,
                "type": "audio",
                "name": "audio2.mp3",
                "url": None,
                "path": None
            },
            {
                "id": 6,
                "type": "audio",
                "name": "audio3.mp3",
                "url": None,
                "path": None
            },
            {
                "id": 7,
                "type": "image",
                "name": "image2.jpg",
                "url": None,
                "path": None
            }
        ]

        self.assertEqual(target, result)

    def test_get_media_types(self):
        """Test for GET at /medias/image."""
        result = self.simulate_get("/medias/image",
                                   headers={"Authorization": "Bearer " + self.token}).json
        target = [
            {
                "id": 4,
                "type": "image",
                "name": "image1.jpg",
                "url": None,
                "path": None
            },
            {
                "id": 7,
                "type": "image",
                "name": "image2.jpg",
                "url": None,
                "path": None
            }
        ]

        self.assertEqual(target, result)

    def test_get_media(self):
        """Test for GET at /medias/audio/1."""
        result = self.simulate_get("/medias/audio/1",
                                   headers={"Authorization": "Bearer " + self.token}).json
        target = {
            "id": 1,
            "type": "audio",
            "name": "audio1.mp3",
            "url": None,
            "path": None
        }

        self.assertEqual(target, result)

    def test_get_media_nonexistent(self):
        """Try to GET a nonexistent media."""
        result = self.simulate_get("/media/audio/5",
                                   headers={"Authorization": "Bearer " + self.token}).status
        target = falcon.HTTP_404

        self.assertEqual(result, target)
