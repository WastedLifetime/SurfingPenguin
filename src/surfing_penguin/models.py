""" models.py: Classes that tell the content in the database."""

import datetime
from sqlalchemy import Column, Integer, String, DateTime
from surfing_penguin import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password = Column(String(32))
    register_time = Column(DateTime, default=datetime.datetime.utcnow)
    last_login = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "User('{}','{}',registered at '{}',last login:'{}')".format(
                self.username,
                self.password,
                self.register_time,
                self.last_login
                )
