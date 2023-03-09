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
    '''
        return tomorrow as YYYY-MM-DD format.
    '''
    return (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

# def do_something(scheduler): 
#     # schedule the next call first
#     scheduler.enter(60, 1, do_something, (scheduler,))
#     print("Doing stuff...")
#     # then do your stuff

def tweet_exist(tweet_id: str, session: Session):
    '''
        check whether a tweet exists or not.
    '''
    tweet = session.query(Models.Tweet).filter(Models.Tweet.id == tweet_id ).first()
    return True if tweet else False



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
    '''
        fetch all conversations of user from since_date until until_date.
    '''
    logging.debug(f'fetching user conversations {user} from {since_date} until {until_date}')
    for _, tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{user} since:{since_date} until:{until_date}').get_items()):
        # TODO: quotedTweet should add to the retweet table.
        # TODO: use user_id instead of username.
        # TODO: add media part to table.    
    
        ## check it's conversation root
        if tweet.id == tweet.conversationId:
            yield tweet    


def get_users(session:Session) -> list: 
    '''
        return the list of users with the last update date.
    '''
    return session.query(Models.User).all()

def insert_users_conversations(session: Session):
    '''
        get the conversations of users until today. 
    '''
    users : list(Models.User) = get_users(session=session) 
    for user in users:
        for t in fetch_user_conversation(user.id, user.last_update):
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


def update_last_update(user: Models.User, session: Session, date: str = get_today()):
    '''
        update the last update in users table.
    '''
    user.last_update = date
    session.commit()

def update_users_last_update(session):
    users : list(Models.User) = get_users(session=session)
    for user in users:
        update_last_update(user, session)

def get_all_conversations(session: Session):
    conversations : list(Models.Conversation) = session.query(Models.Conversation).all()
    return conversations

def get_replies_of_conversation(conversation: Models.Conversation , last_update: str, session: Session):

    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'conversation_id:{conversation.conversation_id}  (filter:safe OR -filter:safe) since:{last_update}').get_items()): #declare a username 
        if i > 2:
            break
        if not tweet_exist(tweet.id, session):
            yield tweet

def insert_replies(session: Session):
    # TODO: handle different last update for each user 
    try:
        last_update = get_users(session)[0].last_update
    except Exception as e:
        logging.error(str(e))
        return
    conversations : list(Models.Conversation) = get_all_conversations(session)
    for conversation in conversations:
        for reply in get_replies_of_conversation(conversation, last_update, session):
            tweet = Models.Tweet(
                    id = reply.id,
                    author_id = reply.user.username,
                    text = reply.rawContent,
                    create_date = reply.date,
                )
            session.add(tweet)
            session.commit()

            try:
                target = reply.inReplyToTweetId

                reply_row = Models.Reply(
                    source_id = reply.id,
                    target_id = target
                )

                session.add(reply_row)
                session.commit()
            except IntegrityError:
                session.rollback()
                logging.error(f'Couldn\'t find the target {target} in table !!!')


if __name__ == '__main__':
    # my_scheduler = sched.scheduler(time.time, time.sleep)
    # my_scheduler.enter(60, 1, do_something, (my_scheduler,))
    # my_scheduler.run()
    
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    Models.Base.metadata.create_all(engine, checkfirst=True)

    session = sessionmaker(bind=engine)()

    users = config.USERS.split(',')
    # insert_users(session=session, users=users)

    # insert_users_conversations(session)

    insert_replies(session)

    # update_users_last_update(session)








