from db_api import db
from sqlalchemy import Column, String, Date, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
import datetime as dt
from sqlalchemy.orm import validates 

def calc_sentiment_score(context):
    # return context.get_current_parameters()['text'] 
    return 0.0


class Author(db.Model):
    __tablename__ = 'authors'

    username = Column('username', String(32), unique=True, primary_key=True)
    id = Column('id', String(32), unique=True, primary_key=False)
    image_url = Column('image_url', Text, nullable=False)
    tweets = relationship('Tweet', back_populates='author')

class User(db.Model):
    __tablename__ = 'users'
    
    username = Column('username', String(32), ForeignKey('authors.username'), unique=True, primary_key=True)
    last_update = Column('last_update', Date, unique=False, nullable=False)
    base = relationship('Author')

    @validates('last_update')
    def validate_registered_date(self, key, value):
        if value:
            try:
                dt.date.fromisoformat(value) # check format as YYYY-MM-DD
            except ValueError:
                raise ValueError('Incorrect date format, should be YYY-MM-DD')
        return value

class Tweet(db.Model):
    __tablename__ = 'tweets' 
    
    id = Column('id', String(32), unique= True, primary_key=True)
    author_id =  Column('author_id', String(32), ForeignKey('authors.username'), unique=False, nullable=False)
    text = Column('text', Text(), nullable=False)
    create_date = Column('create_date', DateTime(), nullable=False)
    sentiment_score = Column('sentiment_score', Float, nullable=False, default=calc_sentiment_score, onupdate=calc_sentiment_score)

    author = relationship('Author', back_populates='tweets')
