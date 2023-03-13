import os 

from dotenv import load_dotenv

load_dotenv()

DB_API_URL = os.getenv('DB_API_URL')
