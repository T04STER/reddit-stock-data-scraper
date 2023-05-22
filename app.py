from flask import Flask
from flask_mongoengine import MongoEngine
from dot_env_loader import REDDIT_SECRET

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'xd',  # TODO
    'host': 'localhost',
    'port': 1337
}

db = MongoEngine()
db.init_app(app)


@app.route('/')
def hello_world():  # put application's code here
    return f""


if __name__ == '__main__':
    app.run()
