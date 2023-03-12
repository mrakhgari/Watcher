from database_api.db.database import Base
from sqlalchemy import Column, String, Date, Text, ForeignKey


class Author(Base):
    __tablename__ = 'authors'

    username = Column('username', String(32), unique=True, primary_key=True)
    id = Column('id', String(32), unique=True, primary_key=False)
    image_url = Column('image_url', Text, unique=True, nullable=False)

class User(Base):
    __tablename__ = 'users'
    
    username = Column('username', String(32), ForeignKey('authors.username'), unique=True, primary_key=True)
    last_update = Column('last_update', Date, unique=False, nullable=False)





