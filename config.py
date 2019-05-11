import os

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or 'hard_to_guess'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
