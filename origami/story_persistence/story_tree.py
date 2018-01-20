"""Story tree."""

import json

from sqlalchemy.orm import scoped_session, sessionmaker
from .. import db
from ..main_app import get_engine

class Story(object):

    def __init__(self):
        self.parsed_story = None

    def read_story_tree(self, json_file):
        with open(json_file, "r") as json_story:
            self.parsed_story = json.loads(json_story)

    def insert_story_db(self):
        engine = get_engine(memory=False)
        db.Base.metadata.create_all(engine)
        sess_maker = sessionmaker(bind=engine)
        Session = scoped_session(sess_maker)
        session = Session()

        if self.parsed_story is not None:
            self.insert_nodes_media(self.parsed_story, session)
        else:
            raise StoryNotFoundError("There is no story to insert in the database.")

    def insert_nodes_media(self, parsed_story, session):
        node_name = parsed_story['name']
        node_media = parsed_story['media']
        node_children = parsed_story['children']

        node = db.NodeDao(node_name)
        session.add(node)

        for media in node_media:
            media_name = media['name']
            media_type = media['type']
            found = db.MediaDao.get_by_name_and_type(media_name, media_type, session)
            if found is None:
                raise MediaNotFoundError("The media requested is not present in the database.")
        
        if node_children is not None:
            self.insert_nodes_media(node_children, session)
        
        session.commit()



class MediaNotFoundError(Exception):
    pass

class StoryNotFoundError(Exception):
    pass
