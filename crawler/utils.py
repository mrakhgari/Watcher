import datetime

def get_now():
    return datetime.datetime.now()

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


def get_unknown_user() -> dict:
    return {
        'id': 000000000000000,
        'username': '---unknown----',
        'image_url': 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
    }