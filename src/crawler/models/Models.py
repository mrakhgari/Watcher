from sqlalchemy import Column, String, Date, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column('id', String(32), unique=True, primary_key=True )
    last_update = Column('last_update', Date, unique=False, nullable=False)


def calc_sentiment_score(context):
    # return context.get_current_parameters()['text'] 
    return 0.0

class Tweet(Base):
    __tablename__ = 'tweets' 
    
    id = Column('id', String(32), unique= True, primary_key=True)
    author_id =  Column('author_id', String(32), unique=False, nullable=False)
    text = Column('text', Text(), nullable=False)
    create_date = Column('create_date', DateTime(), nullable=False)
    sentiment_score = Column('sentiment_score', Float, nullable=False, default=calc_sentiment_score, onupdate=calc_sentiment_score)



class Conversation(Base):
    __tablename__ = 'conversations'

    user_id = Column(String(32), ForeignKey('users.id'), primary_key=True)
    conversation_id = Column(String(32), ForeignKey('tweets.id'), primary_key=True)
    user = relationship('User')
    tweet = relationship('Tweet')


# class Reply(Base):
#     __tablename__ = 'replies'

#     source_id = Column(String(32), ForeignKey('tweets.id'), primary_key=True)
#     target_id = Column(String(32), ForeignKey('tweets.id'), primary_key=False)
#     source = relationship('Tweet')
#     target = relationship('Tweet')

# class Retweet(Base):
#     __tablename__ = 'retweets'

#     source_id = Column(String(32), ForeignKey('tweets.id'), primary_key=True)
#     target_id = Column(String(32), ForeignKey('tweets.id'), primary_key=False)
#     source = relationship('Tweet')
#     target = relationship('Tweet')

