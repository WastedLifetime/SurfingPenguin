""" __init__.py: Initialization of the server """

from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

login_manager = LoginManager()

Session = sessionmaker()
session = Session()

def init_app(app):
    login_manager.init_app(app)
    db_engine = create_engine(
        app.config['SQLALCHEMY_DATABASE_URI'],
        echo=False)
    from src.surfing_penguin import models  # noqa: F401
    Base.metadata.create_all(db_engine)
    session.__init__(bind=db_engine)
