from os import environ
from dotenv import load_dotenv

load_dotenv()
REDDIT_SECRET = environ.get('REDDIT_SECRET')
REDDIT_CLIENT_ID = environ.get('REDDIT_CLIENT_ID')
REDDIT_USER_AGENT = environ.get('REDDIT_USER_AGENT')
MONGODB_USERNAME = environ.get('MONGODB_USERNAME')
MONGODB_PASSWORD = environ.get('MONGODB_PASSWORD')
MONGODB_HOSTNAME = environ.get('MONGODB_HOSTNAME')
MONGODB_DATABASE = environ.get('MONGODB_DATABASE')
