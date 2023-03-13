from db_api import db
from sqlalchemy import Column, String, Date, Text, ForeignKey
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
