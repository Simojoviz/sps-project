import os
basedir = os.path.abspath(os.path.dirname(__file__))




class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'rnd-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/films'
    SQLALCHEMY_TRACK_MODIFICATIONS = False




