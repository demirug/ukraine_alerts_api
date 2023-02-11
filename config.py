import os


class Config:
    DEBUG = os.getenv("DEBUG")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask.db'
