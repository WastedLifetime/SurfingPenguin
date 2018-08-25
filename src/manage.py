import os
import sys
import pytest
from flask_migrate import MigrateCommand
from flask_script import Manager


parent_path = os.path.dirname(os.getcwd())
sys.path.append(parent_path)


from src.config import TestConfig  # NOQA
from src.surfing_penguin import create_app  # NOQA
from src.surfing_penguin.extensions import session #NOQA
from src.surfing_penguin.models import User  # NOQA
from src.config import ProductionConfig, DevelopmentConfig, StagingConfig #NOQA

def get_config():
    ENV = os.environ.get('ENV')

    if ENV == "Staging":
        config = StagingConfig
    elif ENV == "Production":
        config = ProductionConfig
    else:
        config = DevelopmentConfig

    return config

config = get_config()
app = create_app(config)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def initrole():
    name = app.config['ADMIN_NAME']
    pwd = app.config['ADMIN_PASSWORD'] or input("Pls input Flask admin pwd:")
    if session.query(User).filter_by(username=name).first() is None:
        new_user = User(name, pwd, 'admin')
        new_user.id = session.query(User).count() + 1
        session.add(new_user)
        session.commit()
        print("Roles added!")
    else:
        print("Name has been used.")


if __name__ == "__main__":
    manager.run()
