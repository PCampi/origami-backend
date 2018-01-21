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
                "media_type": "audio",
                "media_name": "audio1.mp3",
                "url": None,
                "fs_path": None
            },
            {
                "id": 2,
                "media_type": "video",
                "media_name": "video1.mp4",
                "url": None,
                "fs_path": None
            },
            {
                "id": 3,
                "media_type": "text",
                "media_name": "text1.txt",
                "url": None,
                "fs_path": None
            },
            {
                "id": 4,
                "media_type": "image",
                "media_name": "image1.jpg",
                "url": None,
                "fs_path": None
            },
            {
                "id": 5,
                "media_type": "audio",
                "media_name": "audio2.mp3",
                "url": None,
                "fs_path": None
            },
            {
                "id": 6,
                "media_type": "audio",
                "media_name": "audio3.mp3",
                "url": None,
                "fs_path": None
            },
            {
                "id": 7,
                "media_type": "image",
                "media_name": "image2.jpg",
                "url": None,
                "fs_path": None
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
                "media_type": "image",
                "media_name": "image1.jpg",
                "url": None,
                "fs_path": None
            },
            {
                "id": 7,
                "media_type": "image",
                "media_name": "image2.jpg",
                "url": None,
                "fs_path": None
            }
        ]

        self.assertEqual(target, result)

    def test_get_media(self):
        """Test for GET at /medias/audio/1."""
        result = self.simulate_get("/medias/audio/1",
                                   headers={"Authorization": "Bearer " + self.token}).json
        target = {
            "id": 1,
            "media_type": "audio",
            "media_name": "audio1.mp3",
            "url": None,
            "fs_path": None
        }

        self.assertEqual(target, result)

    def test_get_media_nonexistent(self):
        """Try to GET a nonexistent media."""
        result = self.simulate_get("/media/audio/5",
                                   headers={"Authorization": "Bearer " + self.token}).status
        target = falcon.HTTP_404

        self.assertEqual(result, target)
