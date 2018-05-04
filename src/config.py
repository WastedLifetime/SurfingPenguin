import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL')
                               if os.environ.get('DATABASE_URL') is not None
                               else 'sqlite:///:memory:')


class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL')
                               if os.environ.get('DATABASE_URL') is not None
                               else 'sqlite:///:memory:')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL')
                               if os.environ.get('DATABASE_URL') is not None
                               else 'sqlite:///:memory:')


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
