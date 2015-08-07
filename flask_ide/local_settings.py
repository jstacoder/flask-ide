import os

class LocalConfig(object):
    SECRET_KEY = 'A Secret Shhh'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',None) or 'sqlite:///test_ee.db'
