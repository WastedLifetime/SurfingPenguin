""" __init__.py: Initialization of the server """

from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

login_manager = LoginManager()
migrate = Migrate()

Session = sessionmaker()
session = Session()

flask_admin = Admin()


def init_app(app):
    CORS(app, resources={r"/api/*": {"origins": app.config['FRONTEND_URL']}})
    login_manager.init_app(app)
    flask_admin.init_app(app)
    db_engine = create_engine(
        app.config['SQLALCHEMY_DATABASE_URI'],
        echo=False)
    from src.surfing_penguin import models  # noqa: F401
    from src.surfing_penguin.models import User  # noqa: F401
    Base.metadata.create_all(db_engine)
    session.__init__(bind=db_engine)
    migrate.init_app(app, Base, render_as_batch=True)
