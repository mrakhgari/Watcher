from sqlalchemy.orm import Session
from .models import Conversation, Tweet, Reply
from db_api.apps.users_app.user_db import insert_author
import logging

def get_conversations(username: str):
    conversations = Conversation.query.filter(Conversation.username == username).all()
    return conversations

def create_tweet(args, session: Session):
    try:
        _ = insert_author(args, session)
    except:
        session.rollback()
        logging.warning(f'author: {args.get("username")} exists!')
        pass

    new_tweet = Tweet(
        id = args.get('id'),
        author_username = args.get('author_username'),
        text = args.get('text'),
        create_date = args.get('create_date') 
    )

    session.add(new_tweet)
    session.commit()
    session.refresh(new_tweet)
    return new_tweet

def create_conversation(args, session: Session ):
    # tweet = create_tweet(args, session)
    new_conversation = Conversation(
        username = args.get('author_username'),
        conversation_id = args.get('id')
    )

    session.add(new_conversation)
    session.commit()
    session.refresh(new_conversation)
    return new_conversation

def create_reply(args, session: Session):
    new_reply = Reply(
        source_id = args.get('source_id'),
        target_id = args.get('target_id')
    )

    session.add(new_reply)
    session.commit()
    session.refresh(new_reply)
    return new_reply
