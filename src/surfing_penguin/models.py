""" models.py: Classes that tell the content in the database."""

import datetime
from sqlalchemy import Column, Integer, String, DateTime
from surfing_penguin import Base
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    password_hash = Column(String(128))
    register_time = Column(DateTime, default=datetime.datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return "User('{}', registered at '{}',last login:'{}')".format(
                self.username,
                self.register_time,
                self.last_seen
                )

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
