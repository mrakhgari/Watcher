import os 

from dotenv import load_dotenv

load_dotenv()

USERS = os.getenv('USERS')
START_DATE = os.getenv('START_DATE')
DB_API_URL = os.getenv('DB_API_URL')
