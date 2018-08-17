""" __init__.py: Initialization of the server """

from flask_cors import CORS
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

login_manager = LoginManager()

Session = sessionmaker()
session = Session()


def init_app(app):
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    login_manager.init_app(app)
    db_engine = create_engine(
        app.config['SQLALCHEMY_DATABASE_URI'],
        echo=False)
    from src.surfing_penguin import models  # noqa: F401
    from src.surfing_penguin.models import User  # noqa: F401
    Base.metadata.create_all(db_engine)
    session.__init__(bind=db_engine)
    # TODO: change the way to add role and admin
    ADMIN_NAME = app.config['ADMIN_NAME']
    ADMIN_PASSWORD = app.config['ADMIN_PASSWORD']
    if session.query(User).filter_by(username=ADMIN_NAME).first() is None:
        new_user = User(ADMIN_NAME, ADMIN_PASSWORD, 'admin')
        new_user.id = session.query(User).count() + 1
        session.add(new_user)
        session.commit()
