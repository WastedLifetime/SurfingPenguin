""" models.py: Classes that tell the content in the database."""

from surfing_penguin import db_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "User('{}','{}')".format(
                self.username,
                self.password
                )


Base.metadata.create_all(db_engine)
