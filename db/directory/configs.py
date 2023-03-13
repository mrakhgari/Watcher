import os 

class Base(object):
    DATABASE_NAME = os.getenv('MARIADB_DATABASE')
    DATABASE_USER = os.getenv('MARIADB_USER')
    DATABASE_PASSWORD = os.getenv('MARIADB_PASSWORD')
    DATABASE_HOST = os.getenv('MARIADB_HOST')
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')


class Development(Base):
    pass


class Production(Base):
    pass
