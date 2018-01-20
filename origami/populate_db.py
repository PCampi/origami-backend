"""Module to populate the database with sample data."""

from sqlalchemy.orm import scoped_session, sessionmaker

from . import db
from .main_app import get_engine


def populate():
    """Populate the database with sample data."""
    engine = get_engine(memory=False)
    db.Base.metadata.create_all(engine)
    sess_maker = sessionmaker(bind=engine)
    Session = scoped_session(sess_maker)
    session = Session()

    player1 = db.PlayerDao("Gianni", 9, "male")
    player2 = db.PlayerDao("Federica", 8, "female")
    player3 = db.PlayerDao("Josh", 6, "male")

    admin1 = db.AdministratorDao("Pippo", "pippo@gmail.com", "pippo1")
    admin2 = db.AdministratorDao("Pluto", "pluto@gmail.com", "pluto2")
    admin3 = db.AdministratorDao("Paperino", "paperino@gmail.com", "paperino3")

    media1 = db.MediaDao("audio", "audio1.mp3", None, None)
    media2 = db.MediaDao("video", "video1.mp4", None, None)
    media3 = db.MediaDao("text", "text1.txt", None, None)
    media4 = db.MediaDao("image", "image1.jpg", None, None)
    media5 = db.MediaDao("audio", "audio2.mp3", None, None)
    media6 = db.MediaDao("audio", "audio3.mp3", None, None)
    media7 = db.MediaDao("image", "image2.jpg", None, None)

    node1 = db.NodeDao("nodo_prova1")
    node2 = db.NodeDao("nodo_prova2")
    node3 = db.NodeDao("nodo_prova3")

    played_story1 = db.PlayedStoryDao(1)
    played_story2 = db.PlayedStoryDao(2)
    played_story3 = db.PlayedStoryDao(1)
    played_story4 = db.PlayedStoryDao(3)

    choice11 = db.PlayedChoicesDao(1, 1, 2)
    choice12 = db.PlayedChoicesDao(1, 2, 1)
    choice21 = db.PlayedChoicesDao(2, 1, 2)
    choice22 = db.PlayedChoicesDao(2, 2, 3)
    choice31 = db.PlayedChoicesDao(3, 1, 3)
    choice32 = db.PlayedChoicesDao(3, 2, 2)
    choice41 = db.PlayedChoicesDao(4, 1, 3)
    choice42 = db.PlayedChoicesDao(4, 2, 1)

    ending1 = db.EndingDao(1, "La storia finisce bene.")
    ending2 = db.EndingDao(2, "La storia finisce male.")
    ending3 = db.EndingDao(3, "La storia finisce malissimo.")
    ending4 = db.EndingDao(4, "La storia finisce così così.")

    session.add_all([player1, player2, player3])
    session.add_all([admin1, admin2, admin3])
    session.add_all([media1, media2, media3, media4, media5, media6, media7])
    session.add_all([node1, node2, node3])
    session.add_all([played_story1, played_story2, played_story3, played_story4])
    session.add_all([ending1, ending2, ending3, ending4])
    session.add_all([choice11, choice12, choice21, choice22, choice31, choice32, choice41, choice42])
    session.commit()
