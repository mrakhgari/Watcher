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
        data  = {
            'user': {
                'id' : tweet.user.id,
                'username' : tweet.user.username,
                'image_url' : tweet.user.profileImageUrl
            },
            'id': tweet.id,
            'text': tweet.rawContent,
            'create_date': tweet.date.strftime('%Y-%m-%d %H:%M:%S')
        }

        response = requests.post(f'{self.url}/tweets/', json=data)

        return response

    def create_conversation(self, tweet):
        data = {
            'tweet': {
                'id': tweet.id,
                'text': tweet.rawContent,
                'create_date': tweet.date.strftime('%Y-%m-%d %H:%M:%S'),
                'user': {
                    'id' : tweet.user.id,
                    'username' : tweet.user.username,
                    'image_url' : tweet.user.profileImageUrl
                }
            }, 
            'conversation_id': tweet.conversationId,
            'username': tweet.user.username
        }
        response = requests.post(f'{self.url}/tweets/conversations/', json=data)
        return response

    def insert_conversation(self, tweet):
        '''
            Create new conversation. 
        '''

        data = {
            'conversation_id': tweet.conversationId,
            'username': tweet.user.username
        }

        response = requests.post(f'{self.url}/tweets/conversations', json=data)
        return response

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
    for _, tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{user.get("username")} since:{user.get("last_update")} until:{utils.get_today()}').get_items()):
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
            response = caller.create_conversation(t)
            if response.status_code != 201:
                logging.warning(f'Couldn\'t insert conversation, cause {response.content}')
            else: 
                logging.info(f'conversation inserted! {response.json().get("data").get("conversation_id")}')


if __name__ == '__main__':
    usernames = configs.USERS.split(',')
    caller = Caller('http://localhost:5000')
    print('in insert users!!!')
    insert_users(usernames, caller)
    print('users inserted!')
    users = caller.get_users()
    print('getting users')
    if not users:
        logging.error("Can't fetch users!")
        exit(-1)
    print('users got')
    insert_conversations(users, caller)
