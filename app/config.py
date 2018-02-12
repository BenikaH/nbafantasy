import os

from app.utility import getdb

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    dbconfig = getdb(key='nbadb')
    user = dbconfig['user']
    pwd = dbconfig['password']
    host = dbconfig['host']
    db = dbconfig['db']
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(user, pwd, host, db)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

