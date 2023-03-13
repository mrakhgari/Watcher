from . import tweets
from . import tweet_db
from db_api import db 
from db_api import status
from db_api.utils.request import json_only
from flask import request
from sqlalchemy.exc import IntegrityError, OperationalError


@tweets.route('/conversations/<string:username>', methods=['GET'])
def get_conversations(username):
    '''
        return all of conversations of an user.
    '''

    conversations = tweet_db.get_conversations(username)
    if not conversations:
        return {'message': 'There is no conversation for this user!'}, status.HTTP_404_NOT_FOUND
    
    conversations = [{
        'id': conversation.tweet.id,
        'author_username': conversation.tweet.author_username,
        'text': conversation.tweet.text,
        'create_date': conversation.tweet.create_date,
        'sentiment_score': conversation.tweet.sentiment_score
    } for conversation in conversations]

    return {'data': conversations}, status.HTTP_200_OK

@tweets.route('/conversations/', methods=['POST'])
@json_only
def create_conversation():
    '''
        create new conversation of an user.
    '''
    args = request.get_json()

    try:
        conversation = tweet_db.create_conversation(args, db.session)
    except IntegrityError:
        db.session.rollback()
        return {'message': f'There is a conversation with ID {args.get("conversation_id")}  for user {args.get("username")}.'}, status.HTTP_400_BAD_REQUEST
    except OperationalError as e:
        db.session.rollback()
        return {'message': f'Please enter the full of information! {str(e)}'}, status.HTTP_400_BAD_REQUEST
    except ValueError as e:
        db.session.rollback()
        return {'message': str(e)}

    return {
        'data': {
            'conversation_id': conversation.conversation_id,
            'username': conversation.username,
            'tweet': {
                'id': conversation.tweet.id,
                'text' : conversation.tweet.text,
                'sentiment_score': conversation.tweet.sentiment_score,
                'author': {
                    'id': conversation.tweet.author.id,
                    'username': conversation.tweet.author.username,
                    'image_url': conversation.tweet.author.image_url
                }
            }
        }
    }, status.HTTP_201_CREATED


@tweets.route('/replies', methods=['POST'])
@json_only
def create_reply():
    '''
        create new reply row in table.
    '''
    args = request.get_json()

    try:
        reply = tweet_db.create_reply(args, db.session)
    except IntegrityError:
        db.session.rollback()
        return {'message': f'There is a Reply row with source ID {args.get("source_id")}  and target ID {args.get("target_id")}.'}, status.HTTP_400_BAD_REQUEST
    except OperationalError:
        db.session.rollback()
        return {'message': f'Please enter the full of information!'}, status.HTTP_400_BAD_REQUEST
    except ValueError as e:
        db.session.rollback()
        return {'message': str(e)}
    return {
        'data': {
            'source': reply.source,
            'username': reply.target
        }
    }


@tweets.route('/', methods=['POST'])
@json_only
def create_tweet():
    '''
        create new tweet row in table.
    '''
    args = request.get_json()
    try:
        new_tweet = tweet_db.create_tweet(args, db.session)
    except IntegrityError:
        db.session.rollback()
        return {'message': f'There is a Tweet row with ID {args.get("id")}'}, status.HTTP_400_BAD_REQUEST
    except OperationalError as e:
        db.session.rollback()
        print(str(e))
        return {'message': f'Please enter the full of information!'}, status.HTTP_400_BAD_REQUEST
    except ValueError as e:
        db.session.rollback()
        return {'message': str(e)}

    
    return {
        'data': {
            'id': new_tweet.id,
            'text' : new_tweet.text,
            'sentiment_score': new_tweet.sentiment_score,
            'author': {
                'id': new_tweet.author.id,
                'username': new_tweet.author.username,
                'image_url': new_tweet.author.image_url
            }
        }
    }, status.HTTP_201_CREATED

