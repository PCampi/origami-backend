"""Story tree."""

import json

from sqlalchemy.orm import scoped_session, sessionmaker
from .. import db
from ..main_app import get_engine

class Story(object):

    #TODO: metodo per istanziare nodi con figli e media

    def __init__(self):
        self.parsed_story = None

    def read_story_tree(self, json_file):
        json_story = open(json_file, "r")
        parsed_story = json.loads(json_story)
        json_story.close()

    def insert_story_db(self, parsed_story):
        engine = get_engine(memory=False)
        db.Base.metadata.create_all(engine)
        sess_maker = sessionmaker(bind=engine)
        Session = scoped_session(sess_maker)
        session = Session()

        if not(parsed_story is None):
            self.insert_nodes_media(parsed_story, session)
        else:
            print("There is no story to insert in the database.")

    def insert_nodes_media(self, parsed_story, session):
        node_name = parsed_story['name']
        node_media = parsed_story['media']
        node_children = parsed_story['children']

        node = db.NodeDao(node_name)
        session.add(node)

        for resource in node_media:
            resource_name = resource['name']
            resource_type = resource['type']
            found = db.ResourceDao.get_by_name_and_type(resource_name, resource_type, session)
            if found is None:
                raise ValueError("The resource requested is not present in the database.") #Non credo sia proprio un ValueError
        
        if not(node_children is {}):
            self.insert_nodes_media(node_children, session)
        
        session.commit()
