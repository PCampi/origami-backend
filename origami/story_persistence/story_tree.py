"""Story tree."""

import json

from sqlalchemy.orm import scoped_session, sessionmaker
from .. import db
from ..main_app import get_engine


class MediaNotFoundError(Exception):
    pass


class StoryNotFoundError(Exception):
    pass


class Story(object):

    def __init__(self):
        self.parsed_story = None

    def read_story_tree(self, json_file_name):
        """Read a story from a JSON file on disk.

        Parameters
        ----------
        json_file_name: str
            name of the JSON file containing the story
        """
        with open(json_file_name, "r") as infile:
            json_story = "".join(infile.readlines())
            self.parsed_story = json.loads(json_story)

    def insert_story_db(self):
        """Save the story in the database."""
        engine = get_engine(memory=False)
        db.Base.metadata.create_all(engine)
        sess_maker = sessionmaker(bind=engine)
        session_factory = scoped_session(sess_maker)
        session = session_factory()

        if self.parsed_story is not None:
            self.insert_nodes_media(self.parsed_story, session)
        else:
            raise StoryNotFoundError(
                "There is no story to insert in the database.")

    def insert_nodes_media(self, parsed_story, session):
        """Insert nodes and medias from the story into the database.

        Parameters
        ----------
        parsed_story: Dict
            a tree structure representing a story (or a subtree of a story)

        session: SQLAlchemy session
            session used to persist instances to database
        """
        node_name = parsed_story['name']
        node_media = parsed_story['media']
        node_children = parsed_story['children']

        node = db.NodeDao(node_name)
        session.add(node)

        # check that the story has existent medias
        for media in node_media:
            media_name = media['name']
            media_type = media['type']
            found = db.MediaDao.get_by_name_and_type(
                media_name, media_type, session)
            if found is None:
                raise MediaNotFoundError(
                    "The requested media\n{}\nis not present in the database."
                    .format(media))

        # recursively save all children to database
        if node_children is not None:
            for child in node_children:
                self.insert_nodes_media(child, session)

        session.commit()
