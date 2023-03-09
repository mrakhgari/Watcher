import os 

from dotenv import load_dotenv


load_dotenv()


# class Config(object):
DATABASE_NAME = os.getenv('MARIADB_DATABASE')
DATABASE_USER = os.getenv('MARIADB_USER')
DATABASE_PASSWORD = os.getenv('MARIADB_PASSWORD')
DATABASE_HOST = os.getenv('MARIADB_HOST')
DATABASE_PORT = os.getenv('MARIADB_PORT')
SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
USERS = os.getenv('USERS')
START_DATE = os.getenv('START_DATE')
    # def __init__(self) -> None:
