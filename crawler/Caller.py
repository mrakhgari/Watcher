import requests
import snscrape.modules.twitter as sntwitter
from utils import get_now, get_unknown_user
import configs

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
        if isinstance(tweet, sntwitter.Tombstone):
            data = {
                'user': get_unknown_user(),
                'id': tweet.id,
                'text': tweet.text,
                'create_date': get_now().strftime('%Y-%m-%d %H:%M:%S'),
                'is_tombstone': True
            }
        else:
            data  = {
                'user': {
                    'id' : tweet.user.id,
                    'username' : tweet.user.username,
                    'image_url' : tweet.user.profileImageUrl
                },
                'id': tweet.id,
                'text': tweet.rawContent,
                'create_date': tweet.date.strftime('%Y-%m-%d %H:%M:%S'),
                'is_tombstone': False
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
    
    def update_last_update(self, date):
        data = {
            'last_update': date
        }
        response = requests.patch(f'{self.url}/users/last_update/', json=data)
        return response

    def create_reply(self, tweet):
    
        if isinstance(tweet, sntwitter.Tombstone):
            data = {
                'tweet': {
                    'id': tweet.id,
                    'text': tweet.text,
                    'create_date': get_now().strftime('%Y-%m-%d %H:%M:%S'),
                    'user': get_unknown_user(),
                    'is_tombstone': True
                },
                'source_id': tweet.id,   
                'target_id': tweet.inReplyToTweetId
            }
        else:
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
                'source_id': tweet.id,   
                'target_id': tweet.inReplyToTweetId
            }

        response = requests.post(f'{self.url}/tweets/replies/', json=data)
        return response
    

    def get_users(self):
        '''
            Get all candidate users.
        '''
        response = requests.get(self.url + '/users/')
        if response.status_code == 200:
            return response.json().get('data')
        return None

    def get_conversations(self, username):
        '''
            Get all conversations of an user.
        '''

        response = requests.get(f'{self.url}/tweets/conversations/{username}/')
        # print(response.content)
        if response.status_code == 200:
            return response.json().get('data')
        return []