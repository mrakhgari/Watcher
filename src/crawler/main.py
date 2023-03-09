# import sched, time
from models import Models
import config 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
import snscrape.modules.twitter as sntwitter
import logging
import datetime


def get_today() -> str:
    '''
        return today date as YYYY-MM-DD format.
    '''
    return datetime.date.today().strftime('%Y-%m-%d')


def get_tomorrow() -> str:

    print(f"tomorrow is {(datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')}")
    return (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
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
    
def fetch_user_conversation(user:str, since_date:str, until_date:str=get_tomorrow()):
    logging.info(f'fetching user conversations {user} from {since_date} until {until_date}')
    for _, tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{user} since:{since_date} until:{until_date}').get_items()):
        # TODO: quotedTweet should add to the retweet table.
        # TODO: use user_id instead of username.
        # TODO: add media part to table.    
    
        ## check it's conversation root
        if tweet.id == tweet.conversationId:
            yield tweet    


def update_last_update(user: Models.User, session: Session, date: str = get_today()):
    user.last_update = date
    session.commit()


def get_users(session:Session) -> list: 
    '''
        return the list of users with the last update date.
    '''
    return session.query(Models.User).all()

def insert_users_conversations(session: Session):
    users : list(Models.User) = get_users(session=session) 
    for user in users:
        for t in fetch_user_conversation(user.id, user.last_update):
            print(f't {t.id}')
            try:
                # TODO: check time of tweet.  
                new_tweet = Models.Tweet(
                    id = t.id,
                    author_id = t.user.username,
                    text = t.rawContent,
                    create_date = t.date,
                )

                session.add(new_tweet)
                session.commit()

            except IntegrityError:
                logging.warning(f'{t.id} exists!!!')
                session.rollback()
            
            try:            
                conversation = Models.Conversation(user_id = t.user.username,
                                            conversation_id = t.conversationId)
                session.add(conversation)
                session.commit()
            except IntegrityError:
                logging.warning(f'{t.id} exists!!!')
                session.rollback()

        update_last_update(user, session)

if __name__ == '__main__':
    # my_scheduler = sched.scheduler(time.time, time.sleep)
    # my_scheduler.enter(60, 1, do_something, (my_scheduler,))
    # my_scheduler.run()
    
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    Models.Base.metadata.create_all(engine, checkfirst=True)

    session = sessionmaker(bind=engine)()

    users = config.USERS.split(',')
    insert_users(session=session, users=users)

    insert_users_conversations(session)
    






