from Caller import Caller
import snscrape.modules.twitter as sntwitter
import configs
import logging
import utils
from snscrape.base import ScraperException

def fetch_user(username):
    '''
        fetch user profile.
    '''
    user = sntwitter.TwitterUserScraper(username).entity
    return user

def insert_users(usernames: list, caller: Caller): 
    for username in usernames:
        user = fetch_user(username)
        response = caller.create_user(user)
        status_code = response.status_code
        if status_code == 201:
            logging.info(f'User {user.username} created!')
        else:
            logging.warning(response.content)

def fetch_user_conversation(user: dict):
    for _, tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{user.get("username")} since:{user.get("last_update")} until:{utils.get_tomorrow()}').get_items()):
        # TODO: quotedTweet should add to the retweet table.
        # TODO: add media part to table.    
        ## check it's conversation root
        if tweet.id == tweet.conversationId:
            yield tweet    

def insert_conversations(users: list, caller: Caller):
    '''
        get the conversations of users until today. 
    '''
    for user in users:
        for t in fetch_user_conversation(user):
            try:
                response = caller.create_conversation(t)
                if response.status_code != 201:
                    logging.warning(f'Couldn\'t insert conversation, cause {response.content}')
                else: 
                    logging.info(f'conversation inserted! {response.json().get("data").get("conversation_id")}')
            except ScraperException:
                logging.warning(f'ScraperException in inserting conversations {t.id}!')

def get_replies_of_conversation(conversation, last_update):
    try:
        for _,tweet in enumerate(sntwitter.TwitterSearchScraper(f'conversation_id:{conversation.get("conversation_id")}  (filter:safe OR -filter:safe) since:{last_update}').get_items()): #declare a username 
            yield tweet
    except ScraperException:
        logging.warning(f'ScraperEXception in fetching replies of a conversation {conversation.get("conversation_id")}')

def insert_replies(users: list, caller: Caller):
    for user in users:
        last_update = user.get('last_update')
        username = user.get("username")
        print(f'getting conversations of {username}')
        conversations = caller.get_conversations(username) 
        print(f'conversation count {len(conversations)}')
        for conversation in conversations:
            print(f'in conversation {conversation.get("conversation_id")}')
            for reply in get_replies_of_conversation(conversation, last_update):
                try:
                    target_id = reply.inReplyToTweetId
                    items =sntwitter.TwitterTweetScraper(target_id, mode=sntwitter.TwitterTweetScraperMode.SINGLE).get_items()
                    target_tweet = next(items)
                    response = caller.create_tweet(target_tweet)
                    if response.status_code != 201:
                        logging.warning(f'Failed inserting tweet, cause {response.content}')
        
                    response = caller.create_reply(reply)
                    if response.status_code != 201:
                        logging.warning(f'Failed inserting reply, cause {response.content}')
                except ScraperException:
                    logging.warning(f'ScraperException in fetching reply {reply.id}')
                    continue
                except StopIteration: 
                    logging.warning(f'There is no tweet with id {target_id}')

def update_last_update(caller: Caller):
    caller.update_last_update(utils.get_today())
    

if __name__ == '__main__':
    usernames = configs.USERS.split(',')
    caller = Caller('http://localhost:5000')
    print('in insert users!!!')
    # insert_users(usernames, caller)
    print('users inserted!')
    users = caller.get_users()
    print('getting users')
    if not users:
        logging.error("Can't fetch users!")
        exit(-1)
    print('users got')
    # insert_conversations(users, caller)
    print('conversations inserted')
    # insert_replies(users, caller)
    print('replies inserted!')
    update_last_update()

