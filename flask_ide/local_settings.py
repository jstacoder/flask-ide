import os

class LocalConfig(object):
    SECRET_KEY = 'A Secret Shhh'
    SQLALCHEMY_DATABASE_URI = os.environ.get('HEROKU_POSTGRES_URI',None) or 'sqlite:///test_ee.db'
