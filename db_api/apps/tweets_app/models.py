from db_api import db
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates 


def calc_sentiment_score(context):
    # return context.get_current_parameters()['text'] 
    return 0.0

class Tweet(db.Model):
    __tablename__ = 'tweets' 
    
    id = Column('id', String(32), unique= True, primary_key=True)
    author_username =  Column('author_username', String(32), ForeignKey('authors.username'), unique=False, nullable=False)
    text = Column('text', Text(), nullable=False)
    create_date = Column('create_date', DateTime(), nullable=False)
    sentiment_score = Column('sentiment_score', Float, nullable=False, default=calc_sentiment_score, onupdate=calc_sentiment_score)
    is_tombstone = Column('is_tombstone', Boolean, default=False)
    author = relationship('Author', back_populates='tweets')

class Conversation(db.Model):    
    __tablename__ = 'conversations'

    username = Column("username", String(32), ForeignKey('users.username'), primary_key=True)
    conversation_id = Column("conversation_id", String(32), ForeignKey('tweets.id'), primary_key=True)
    user = relationship('User')
    tweet = relationship('Tweet')


class Reply(db.Model):
    __tablename__ = 'replies'

    source_id = Column(String(32), ForeignKey('tweets.id'), primary_key=True)
    target_id = Column(String(32), ForeignKey('tweets.id'), primary_key=False)
    source = relationship('Tweet', foreign_keys=[source_id])
    target = relationship('Tweet', foreign_keys=[target_id])
