from sqlalchemy.orm import Session
from .models import Conversation, Tweet, Reply
from sqlalchemy import literal
from sqlalchemy.orm import aliased
from directory.apps.users_app.user_db import insert_author
import logging
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy import and_


def get_conversations(username: str):
    conversations = Conversation.query.filter(Conversation.username == username).all()
    return conversations

def get_conversation(username, conversation_id, session: Session):
    # parameters
    start_id = conversation_id
    
    # CTE definition
    starting_replies = (session.query(Reply, literal(0).label("level"))
        .filter(Reply.target_id == start_id)
        .cte(recursive=True)
    )

    parent = aliased(starting_replies, name="parent")
    child = aliased(Reply, name="child")

    joined = (session.query(child, (parent.c.level + 1).label("level"))
        .filter(child.target_id == parent.c.source_id)
    )

    cte = parent.union_all(joined)
    result = {}

    for entry in session.query(cte).order_by(cte.c.target_id, cte.c.source_id, cte.c.level):
        row = result.get(entry[1])
        if not row:
            row = {}
        if not row.get('tweet'):
            tweet = Tweet.query.filter(Tweet.id == entry[1]).first()
            row['tweet'] = {
                'id': tweet.id,
                'author_username': tweet.author_username,
                'text': tweet.text,
                'create_date': tweet.create_date,
                'sentiment_score': tweet.sentiment_score,
                'is_tombstone': tweet.is_tombstone,
                'author': {
                    'id': tweet.author.id,
                    'username': tweet.author.username,
                    'image_url': tweet.author.image_url
                }
            }
        if not row.get('replies'):
            row['replies'] = []
        row['replies'].append(entry[0])
        result[entry[1]] = row

    return result

def create_tweet(args, session: Session):
    try:
        _ = insert_author(args.get("user"), session)
    except IntegrityError:
        session.rollback()
        logging.warning(f'author: {args.get("user")} exists!')
    except OperationalError as e:
        raise e

    new_tweet = Tweet(
        id = args.get('id'),
        author_username = args.get("user").get("username"),
        text = args.get('text'),
        create_date = args.get('create_date') 
    )

    session.add(new_tweet)
    session.commit()
    session.refresh(new_tweet)
    return new_tweet

def create_conversation(args, session: Session ):
    _ = create_tweet(args.get("tweet"), session)
    new_conversation = Conversation(
        username = args.get('username'),
        conversation_id = args.get('conversation_id')
    )

    session.add(new_conversation)
    session.commit()
    session.refresh(new_conversation)
    return new_conversation

def create_reply(args, session: Session):
    try:
        _ = create_tweet(args.get('tweet'), session)
    except IntegrityError:
        session.rollback()
        pass
    new_reply = Reply(
        source_id = args.get('source_id'),
        target_id = args.get('target_id')
    )

    session.add(new_reply)
    session.commit()
    session.refresh(new_reply)
    return new_reply
