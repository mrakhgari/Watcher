from . import users 
from . import user_db
from db_api import db 
from db_api import status
from db_api.utils.request import json_only
from flask import request
from sqlalchemy.exc import IntegrityError, OperationalError

import logging


@users.route('/', methods=['POST'])
@json_only
def create_user():
    '''
        Register a new candidate user for crawling. 
    '''
    args = request.get_json()

    try:
        _ = user_db.insert_author(args, db.session)
    except IntegrityError: 
        logging.warning(f'Duplicated author with username {args.get("username")}!') 
        db.session.rollback()

    try:
        new_user = user_db.insert_user(args, db.session)
    except ValueError as e:
        db.session.rollback()
        return {'message': str(e)}, status.HTTP_400_BAD_REQUEST
    except IntegrityError as e:
        db.session.rollback()
        return {'message': f'Duplicated user with username {args.get("username")} and id {args.get("id")}'}, status.HTTP_400_BAD_REQUEST
    except OperationalError:
        db.session.rollback()
        return {'message': f'The username, last_update,id, and image_url couldn\'t  be null!'}, status.HTTP_400_BAD_REQUEST

    return {'data':         
        {
            'id': new_user.base.id,
            'username': new_user.base.username,
            'image_url': new_user.base.image_url
        }
    }, status.HTTP_201_CREATED


@users.route('/', methods=['GET'])
def get_users():
    '''
        Get all of candidates. 
    '''

    users = user_db.get_users()

    users = [{
        'id': user.base.id,
        'username': user.base.username,
        'image_url': user.base.image_url,
        'last_update': user.last_update.isoformat()
    } for user in users]

    return {'data': users}, status.HTTP_200_OK

@users.route('/authors', methods=['POST'])
@json_only
def create_author():
    '''
        Create an author. 
    '''

    args = request.get_json()
    try:
        new_author = user_db.insert_author(args, db.session)
    except IntegrityError:
        ## pass duplicated authors
        db.session.rollback()
        return {'message': f'Duplicated user with username {args.get("username")} and id {args.get("id")}'}, status.HTTP_400_BAD_REQUEST
    except OperationalError:
        db.session.rollback()
        return {'message': f'The username,id, and image_url couldn\'t  be null!'}, status.HTTP_400_BAD_REQUEST
    
    return {
        'data': {
            'id': new_author.id, 
            'username' : new_author.username,
            'image_url': new_author.image_url
        }
    }, status.HTTP_201_CREATED


@users.route('/authors/<string:username>', methods=['GET'])
def get_author(username):
    author = user_db.get_author(username)
    if not author:
        return {'message': f'The author with id/username {username} isn\'t valid!'}, status.HTTP_404_NOT_FOUND
    
    return {
        'data': {
            'id': author.id, 
            'username' : author.username,
            'image_url': author.image_url
        }
    }

@users.route('/last_update/', methods=['PATCH'])
@json_only
def update_last_update():
    args = request.get_json()
    try:
        user_db.update_last_update(args.get("last_update"), db.session)
        return '', status.HTTP_204_NO_CONTENT
    except:
        db.session.rollback()
        return {'message': 'An error occurred in updating last_update'}, status.HTTP_400_BAD_REQUEST