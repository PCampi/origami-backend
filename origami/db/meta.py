"""Meta module for SQLAlchemy."""

from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

# engine = create_engine(
#     "postgres://user:password@localhost:5342/origami-dev"
# )

# session_factory = sessionmaker(bind=engine)
# Session = scoped_session(session_factory)
