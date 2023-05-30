import logging

from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from flask_mongoengine import MongoEngine

from configs import reddit_scraper_config, yahoo_scraper_config, aps_scheduler_config
from dot_env_loader import MONGODB_DATABASE, MONGODB_HOSTNAME, MONGODB_USERNAME, MONGODB_PASSWORD
from models import Stock
from services.scrap_service import ScrapService
from services.stock_service import StockService
from views.most_mentioned_stocks_view import MostMentionedStockView
from views.stock_view import StockView

db = MongoEngine()
app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = [
    {
        "db": MONGODB_DATABASE,
        "authentication_source": MONGODB_DATABASE,
        "host": "localhost", #TODO: Change host on docker
        "port": 27017,
        "alias": "default",
        "username": MONGODB_USERNAME,
        "password": MONGODB_PASSWORD
    }
]

reddit_scraper = reddit_scraper_config()
yahoo_scrapper = yahoo_scraper_config()
stock_service = StockService(yahoo_scraper_config())
scrap_service = ScrapService(reddit_scraper, yahoo_scrapper)
aps_scheduler_config(scrap_service)
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

app.add_url_rule('/api/v1/stock/<ticker>', view_func=StockView.as_view('stock_view', stock_service))
app.add_url_rule(
    '/api/v1/stock/',
    view_func=MostMentionedStockView.as_view('most_mentioned_stocks_view', stock_service)
    )

db.init_app(app)

