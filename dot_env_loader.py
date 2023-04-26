from os import environ
from dotenv import load_dotenv

load_dotenv()
REDDIT_SECRET = environ.get('REDDIT_SECRET')
REDDIT_CLIENT_ID = environ.get('REDDIT_CLIENT_ID')
REDDIT_USER_AGENT = environ.get('REDDIT_USER_AGENT')