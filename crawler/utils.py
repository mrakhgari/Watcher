import datetime

def get_today() -> str:
    '''
        return today date as YYYY-MM-DD format.
    '''
    return datetime.date.today().strftime('%Y-%m-%d')