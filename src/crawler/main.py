# import sched, time
from models import Models
import config 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
import snscrape.modules.twitter as sntwitter
import logging

# def do_something(scheduler): 
#     # schedule the next call first
#     scheduler.enter(60, 1, do_something, (scheduler,))
#     print("Doing stuff...")
#     # then do your stuff


def insert_users(session: Session, users:list):
    '''
        Insert the screen name of users who you want to crawl.
        parameters:
        session: database session. 
        users: list of screen names.  
    '''
    for user_id in users:
        try:
            new_user = Models.User(id=user_id, last_update=config.START_DATE)
            session.add(new_user)
            session.commit()
        except IntegrityError:
            logging.warning(f'{user_id} is already exists!!!')
            session.rollback()
    
def fetch_user_conversation(user):
    print(f'fetching user conversations {user} ')


def insert_users_conversations(users: list, session: Session):
    pass

if __name__ == '__main__':
    # my_scheduler = sched.scheduler(time.time, time.sleep)
    # my_scheduler.enter(60, 1, do_something, (my_scheduler,))
    # my_scheduler.run()
    
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    Models.Base.metadata.create_all(engine, checkfirst=True)

    session = sessionmaker(bind=engine)()

    users = config.USERS.split(',')
    insert_users(session=session, users=users)

    insert_users_conversations(users, session)







