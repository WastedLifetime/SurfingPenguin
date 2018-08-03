import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin'
    ADMIN_NAME = os.environ.get('ADMIN_NAME') or 'admin'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL')
                               if os.environ.get('DATABASE_URL') is not None
                               else 'sqlite:///%s' % (
                                   os.path.join(basedir, "example.db")))


class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL')
                               if os.environ.get('DATABASE_URL') is not None
                               else 'sqlite:///%s' % (
                                   os.path.join(basedir, "example.db")))


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL')
                               if os.environ.get('DATABASE_URL') is not None
                               else 'sqlite:///%s' % (
                                   os.path.join(basedir, "example.db")))
    ADMIN_PASSWORD = 'admin'
    ADMIN_NAME = 'admin'


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
