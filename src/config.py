import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://tirbevwnotwfvq:504b36902c0cb58897c0e04ffd10af7384fd480949927d3e40d3b0108f53dfba@ec2-54-163-240-54.compute-1.amazonaws.com:5432/d7t8l4b4r9adoj'

class StagingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://tirbevwnotwfvq:504b36902c0cb58897c0e04ffd10af7384fd480949927d3e40d3b0108f53dfba@ec2-54-163-240-54.compute-1.amazonaws.com:5432/d7t8l4b4r9adoj'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') if os.environ.get('DATABASE_URL')is not None else 'sqlite:///:memory:'
