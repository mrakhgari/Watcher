from sqlalchemy.orm import Session
from .models import User, Author
from sqlalchemy import or_

def insert_author(args, session: Session):
    '''
        Insert new author into database.
    ''' 
    new_author = Author(
        username = args.get('username'),
        id = args.get('id'),
        image_url = args.get('image_url')
    )

    session.add(new_author)
    session.commit()
    session.refresh(new_author)
    return new_author


def insert_user(args, session: Session):
    '''
        Insert new user into database.
    '''
    new_user = User()
    new_user.username = args.get('username')
    new_user.last_update = args.get('last_update')
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def get_users():
    users = User.query.all()
    return users

def get_author(username):
    author = Author.query.filter(or_(Author.id == username, Author.username == username)).first()
    return author
