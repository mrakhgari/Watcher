import requests
import snscrape.modules.twitter as sntwitter
import configs
import logging
import utils

class Caller:
    def __init__(self, base_url) -> None:
        self.url = base_url

    def create_user(self, user):
        '''
            call request to create a new user.
        '''
        response = requests.post(self.url+'/users/', json={
            'username': user.username,
            'id': user.id,
            'image_url': user.profileImageUrl,
            'last_update': configs.START_DATE
        })

        return response
    

    def create_tweet(self, tweet):
        '''
            Create new tweet object.
        '''
        pass


    def get_users(self):
        '''
            Get all candidate users.
        '''
        response = requests.get(self.url + '/users/')
        if response.status_code == 200:
            return response.json().get('data')
        return None

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
    for _, tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{user.username} since:{user.last_update} until:{utils.get_today()}').get_items()):
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
            tweet = caller.create_tweet(t)
            if not tweet:
                logging.warning(f'{tweet.id} exists!')
            
            # try:
            #     # TODO: check time of tweet.  
            #     insert_tweet(session, t)

            # except IntegrityError:
            #     logging.warning(f'{t.id} exists!!!')
            #     session.rollback()
            
            # try:            
            #     conversation = Models.Conversation(user_id = t.user.username,
            #                                 conversation_id = t.conversationId)
            #     session.add(conversation)
            #     session.commit()
            # except IntegrityError:
            #     logging.warning(f'{t.id} exists!!!')
            #     session.rollback()



if __name__ == '__main__':
    usernames = configs.USERS.split(',')
    caller = Caller('http://localhost:5000')
    insert_users(usernames, caller)
    users = caller.get_users()
    if not users:
        logging.error("Can't fetch users!")
        exit(-1)
    
    insert_conversations(users, caller)
